"""
DIBIE - Analizador y Normalizador de Datos
Lee la tabla maestra, crea diccionario de datos y propone tablas atómicas
"""
import sys
from pathlib import Path
import pandas as pd
import json
from typing import Dict, List, Set, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.google_sheets_reader import GoogleSheetsReader


class DataNormalizer:
    """Normalizar tablas a formas atómicas"""
    
    def __init__(self):
        """Initialize normalizer"""
        self.reader = GoogleSheetsReader()
    
    def group_columns_by_entity(self, columns: List[str]) -> Dict[str, List[str]]:
        """Agrupar columnas por entidad/tabla
        
        Args:
            columns: Lista de nombres de columnas
            
        Returns:
            Diccionario con entidades y sus columnas
        """
        entities = {
            "instituciones": [],
            "ubicacion": [],
            "financiero": [],
            "temporal": [],
            "categorias": [],
            "otros": []
        }
        
        for col in columns:
            col_lower = col.lower()
            
            # Instituciones - IDs, nombres, tipos
            if any(x in col_lower for x in [
                'institucion', 'colegio', 'iebm', 'dane', 'establecimiento',
                'nombre_ie', 'razon_social', 'tipo_institucion'
            ]):
                entities["instituciones"].append(col)
            
            # Ubicación geográfica
            elif any(x in col_lower for x in [
                'direccion', 'municipio', 'departamento', 'ciudad', 'vereda',
                'latitud', 'longitud', 'zona', 'barrio', 'localidad'
            ]):
                entities["ubicacion"].append(col)
            
            # Datos financieros
            elif any(x in col_lower for x in [
                'monto', 'valor', 'presupuesto', 'ingresos', 'egresos',
                'asignacion', 'ejecutado', 'saldo', 'recurso', 'transferencia'
            ]):
                entities["financiero"].append(col)
            
            # Información temporal
            elif any(x in col_lower for x in [
                'fecha', 'vigencia', 'año', 'mes', 'periodo', 'trimestre'
            ]):
                entities["temporal"].append(col)
            
            # Categorías/clasificaciones
            elif any(x in col_lower for x in [
                'tipo', 'categoria', 'clasificacion', 'sector', 'nivel',
                'estado', 'fuente', 'rubro', 'concepto'
            ]):
                entities["categorias"].append(col)
            
            # Otros
            else:
                entities["otros"].append(col)
        
        # Remove empty groups
        return {k: v for k, v in entities.items() if v}
    
    def propose_atomic_tables(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """Proponer estructura de tablas atómicas
        
        Args:
            df: DataFrame original
            
        Returns:
            Diccionario con propuestas de tablas
        """
        grouped = self.group_columns_by_entity(df.columns.tolist())
        
        tables = {}
        
        # 1. Tabla de Instituciones (maestro)
        if "instituciones" in grouped:
            inst_cols = grouped["instituciones"]
            
            # Find primary key candidates
            pk_candidates = []
            for col in inst_cols:
                if any(x in col.lower() for x in ['id', 'codigo', 'dane']):
                    pk_candidates.append(col)
            
            tables["maestro_instituciones"] = {
                "description": "Tabla maestra de instituciones educativas",
                "columns": inst_cols,
                "primary_key_candidates": pk_candidates,
                "estimated_rows": df[inst_cols].drop_duplicates().shape[0] if inst_cols else 0
            }
        
        # 2. Tabla de Ubicación
        if "ubicacion" in grouped:
            ubic_cols = grouped["ubicacion"]
            
            tables["ubicacion_geografica"] = {
                "description": "Información geográfica de las instituciones",
                "columns": ubic_cols,
                "foreign_key": "institucion_id (referencia a maestro_instituciones)",
                "estimated_rows": df[ubic_cols].drop_duplicates().shape[0] if ubic_cols else 0
            }
        
        # 3. Tabla de Datos Financieros (hechos)
        if "financiero" in grouped:
            fin_cols = grouped["financiero"]
            
            tables["hechos_financieros"] = {
                "description": "Registros de transacciones/asignaciones financieras",
                "columns": fin_cols,
                "foreign_keys": [
                    "institucion_id (referencia a maestro_instituciones)",
                    "fecha_id (referencia a dim_tiempo)"
                ],
                "type": "fact_table",
                "estimated_rows": len(df)
            }
        
        # 4. Dimensión Tiempo
        if "temporal" in grouped:
            temp_cols = grouped["temporal"]
            
            tables["dim_tiempo"] = {
                "description": "Dimensión de tiempo para análisis temporal",
                "columns": temp_cols,
                "type": "dimension",
                "estimated_rows": df[temp_cols].drop_duplicates().shape[0] if temp_cols else 0
            }
        
        # 5. Dimensiones de Categorías
        if "categorias" in grouped:
            cat_cols = grouped["categorias"]
            
            # Agrupar por tipo de categoría
            for col in cat_cols:
                table_name = f"dim_{col.lower().replace(' ', '_')}"
                tables[table_name] = {
                    "description": f"Dimensión de {col}",
                    "columns": [col],
                    "type": "dimension",
                    "unique_values": df[col].nunique()
                }
        
        return tables
    
    def generate_sql_schema(self, tables: Dict[str, Dict], base_table_name: str) -> str:
        """Generar SQL DDL para las tablas propuestas
        
        Args:
            tables: Diccionario de tablas
            base_table_name: Nombre base de la fuente
            
        Returns:
            SQL DDL script
        """
        sql_lines = [
            "-- DIBIE - Esquema de Base de Datos",
            f"-- Generado desde: {base_table_name}",
            "-- " + "=" * 60,
            ""
        ]
        
        for table_name, info in tables.items():
            sql_lines.append(f"-- {info['description']}")
            sql_lines.append(f"CREATE TABLE {table_name} (")
            
            # Add columns
            for i, col in enumerate(info['columns']):
                col_def = f"    {col.replace(' ', '_').lower()} VARCHAR(255)"
                if i < len(info['columns']) - 1:
                    col_def += ","
                sql_lines.append(col_def)
            
            sql_lines.append(");")
            sql_lines.append("")
        
        return "\n".join(sql_lines)


def main():
    print("=" * 70)
    print("DIBIE - Análisis de Tabla Maestra de Datos Financieros")
    print("=" * 70)
    
    # URL de la hoja de Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc/edit?gid=1897725171#gid=1897725171"
    
    # Inicializar
    normalizer = DataNormalizer()
    
    # 1. Leer datos
    print("\n1. Leyendo datos de Google Sheets...")
    try:
        df = normalizer.reader.read_sheet(url)
        print(f"   ✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    except Exception as e:
        print(f"   ✗ Error al leer datos: {e}")
        return
    
    # 2. Crear diccionario de datos
    print("\n2. Creando diccionario de datos...")
    data_dict = normalizer.reader.create_data_dictionary(df, "maestro_financiero")
    
    # Guardar diccionario
    dict_path = Path("data/processed/diccionario_datos.json")
    dict_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Diccionario guardado en: {dict_path}")
    
    # 3. Mostrar resumen del diccionario
    print("\n3. Resumen del Diccionario de Datos:")
    print(f"   - Tabla: {data_dict['table_name']}")
    print(f"   - Filas: {data_dict['total_rows']:,}")
    print(f"   - Columnas: {data_dict['total_columns']}")
    
    print("\n   Primeras 10 columnas:")
    for i, col in enumerate(data_dict['columns'][:10], 1):
        print(f"   {i}. {col['column_name']}")
        print(f"      Tipo: {col['data_type']} | Tipo negocio: {col['business_type']}")
        print(f"      Cardinalidad: {col['cardinality']} | Únicos: {col['unique_values']}")
        print(f"      Nulos: {col['null_percentage']:.1f}%")
    
    if data_dict['total_columns'] > 10:
        print(f"   ... y {data_dict['total_columns'] - 10} columnas más")
    
    # 4. Agrupar columnas por entidad
    print("\n4. Agrupando columnas por entidad...")
    grouped = normalizer.group_columns_by_entity(df.columns.tolist())
    
    for entity, cols in grouped.items():
        print(f"\n   {entity.upper()}: {len(cols)} columnas")
        for col in cols[:5]:
            print(f"      - {col}")
        if len(cols) > 5:
            print(f"      ... y {len(cols) - 5} más")
    
    # 5. Proponer tablas atómicas
    print("\n5. Proponiendo estructura de tablas atómicas...")
    tables = normalizer.propose_atomic_tables(df)
    
    print(f"\n   Se proponen {len(tables)} tablas:")
    for table_name, info in tables.items():
        print(f"\n   📊 {table_name}")
        print(f"      {info['description']}")
        print(f"      Columnas: {len(info['columns'])}")
        if 'estimated_rows' in info:
            print(f"      Filas estimadas: {info['estimated_rows']:,}")
        if 'primary_key_candidates' in info:
            print(f"      Candidatos PK: {', '.join(info['primary_key_candidates'])}")
    
    # 6. Guardar propuesta de tablas
    tables_path = Path("data/processed/propuesta_tablas_atomicas.json")
    with open(tables_path, 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)
    
    print(f"\n   ✓ Propuesta guardada en: {tables_path}")
    
    # 7. Generar SQL schema
    print("\n6. Generando esquema SQL...")
    sql_schema = normalizer.generate_sql_schema(tables, "maestro_financiero")
    
    sql_path = Path("data/processed/schema_sql.sql")
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write(sql_schema)
    
    print(f"   ✓ Esquema SQL guardado en: {sql_path}")
    
    # 8. Guardar los datos en formato parquet
    print("\n7. Guardando datos en formato Parquet...")
    parquet_path = Path("data/processed/maestro_financiero.parquet")
    
    try:
        # Fix duplicate column names before saving
        df_clean = df.copy()
        cols = pd.Series(df_clean.columns)
        
        # Rename duplicate columns
        for dup in cols[cols.duplicated()].unique():
            indices = [i for i, x in enumerate(df_clean.columns) if x == dup]
            for i, idx in enumerate(indices[1:], start=1):
                df_clean.columns.values[idx] = f"{dup}_{i}"
        
        df_clean.to_parquet(parquet_path, index=False)
        print(f"   ✓ Datos guardados en: {parquet_path}")
        
        if len(cols[cols.duplicated()]) > 0:
            print(f"   ⚠ Se renombraron {len(cols[cols.duplicated()])} columnas duplicadas")
            
    except Exception as e:
        print(f"   ⚠ Error al guardar Parquet: {e}")
        # Fallback to CSV
        csv_path = Path("data/processed/maestro_financiero.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"   ✓ Datos guardados en CSV: {csv_path}")
        parquet_path = csv_path
    
    print("\n" + "=" * 70)
    print("Análisis completado exitosamente!")
    print("=" * 70)
    print(f"\nArchivos generados:")
    print(f"  1. {dict_path}")
    print(f"  2. {tables_path}")
    print(f"  3. {sql_path}")
    print(f"  4. {parquet_path}")


if __name__ == "__main__":
    main()
