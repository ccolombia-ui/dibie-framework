"""
DIBIE - Analizador de Tabla Maestra (versión CSV)
Para usar: Exporta tu Google Sheet como CSV y colócalo en data/tables/
"""
import sys
from pathlib import Path
import pandas as pd
import json

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.table_loader import TableLoader


def analyze_csv_master_table(csv_path: str):
    """Analizar tabla maestra desde CSV
    
    Args:
        csv_path: Ruta al archivo CSV
    """
    print("=" * 70)
    print("DIBIE - Análisis de Tabla Maestra de Datos Financieros (CSV)")
    print("=" * 70)
    
    # Cargar datos
    print(f"\n1. Cargando datos desde: {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"   ✓ Datos cargados: {df.shape[0]:,} filas, {df.shape[1]} columnas")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(csv_path, encoding='latin-1')
            print(f"   ✓ Datos cargados (latin-1): {df.shape[0]:,} filas, {df.shape[1]} columnas")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Mostrar primeras columnas
    print(f"\n2. Columnas detectadas ({len(df.columns)} total):")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        unique = df[col].nunique()
        print(f"   {i:2d}. {col}")
        print(f"       Tipo: {dtype} | No nulos: {non_null:,} | Únicos: {unique:,}")
    
    # Agrupar por categorías
    print("\n3. Agrupación por categorías:")
    
    categories = {
        "Identificadores": [],
        "Ubicación": [],
        "Financiero": [],
        "Temporal": [],
        "Categorías": [],
        "Otros": []
    }
    
    for col in df.columns:
        col_lower = col.lower()
        
        if any(x in col_lower for x in ['id', 'codigo', 'dane', 'nit', 'iebm']):
            categories["Identificadores"].append(col)
        elif any(x in col_lower for x in ['direccion', 'municipio', 'departamento', 'ciudad', 'lat', 'lon']):
            categories["Ubicación"].append(col)
        elif any(x in col_lower for x in ['monto', 'valor', 'presupuesto', 'ingresos', 'egresos', 'saldo', 'asignacion']):
            categories["Financiero"].append(col)
        elif any(x in col_lower for x in ['fecha', 'vigencia', 'año', 'mes', 'periodo']):
            categories["Temporal"].append(col)
        elif any(x in col_lower for x in ['tipo', 'categoria', 'clasificacion', 'sector', 'nivel', 'estado']):
            categories["Categorías"].append(col)
        else:
            categories["Otros"].append(col)
    
    for cat, cols in categories.items():
        if cols:
            print(f"\n   {cat}: {len(cols)} columnas")
            for col in cols[:3]:
                print(f"      - {col}")
            if len(cols) > 3:
                print(f"      ... y {len(cols) - 3} más")
    
    # Proponer tablas
    print("\n4. Tablas atómicas propuestas:")
    
    print("\n   📊 MAESTRO_INSTITUCIONES")
    print("      Columnas ID y nombres de instituciones")
    if categories["Identificadores"]:
        print(f"      - {', '.join(categories['Identificadores'][:3])}")
    
    print("\n   📊 UBICACION_GEOGRAFICA")
    print("      Información geográfica y direcciones")
    if categories["Ubicación"]:
        print(f"      - {', '.join(categories['Ubicación'][:3])}")
    
    print("\n   📊 HECHOS_FINANCIEROS")
    print("      Transacciones y valores financieros (tabla de hechos)")
    if categories["Financiero"]:
        print(f"      - {', '.join(categories['Financiero'][:3])}")
    
    print("\n   📊 DIM_TIEMPO")
    print("      Dimensión temporal")
    if categories["Temporal"]:
        print(f"      - {', '.join(categories['Temporal'][:3])}")
    
    # Guardar resultados
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar análisis
    analysis = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": df.columns.tolist(),
        "categories": {k: v for k, v in categories.items() if v},
        "data_types": df.dtypes.astype(str).to_dict()
    }
    
    analysis_path = output_dir / "analisis_tabla_maestra.json"
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n5. Análisis guardado en: {analysis_path}")
    
    # Guardar en parquet
    parquet_path = output_dir / "maestro_financiero.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"   Datos guardados en: {parquet_path}")
    
    # Mostrar muestra de datos
    print("\n6. Muestra de datos (primeras 3 filas):")
    print(df.head(3).to_string())
    
    print("\n" + "=" * 70)
    print("Análisis completado!")
    print("=" * 70)


if __name__ == "__main__":
    # Buscar archivos CSV en data/tables
    csv_files = list(Path("data/tables").glob("*.csv"))
    
    if not csv_files:
        print("No se encontraron archivos CSV en data/tables/")
        print("\nPor favor:")
        print("1. Abre tu Google Sheet")
        print("2. Archivo → Descargar → CSV")
        print("3. Guarda el archivo en: data/tables/maestro_financiero.csv")
        print("4. Ejecuta este script nuevamente")
    else:
        print(f"Archivos CSV encontrados: {len(csv_files)}")
        for csv_file in csv_files:
            print(f"  - {csv_file.name}")
        
        # Usar el primer CSV encontrado
        analyze_csv_master_table(str(csv_files[0]))
