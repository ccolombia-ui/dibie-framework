"""
DIBIE - Normalización de Datos Financieros
Crear tablas normalizadas según propuesta generada
"""
import pandas as pd
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.google_sheets_reader import GoogleSheetsReader


def normalize_financial_data():
    """
    Normalizar datos financieros en tablas atómicas
    """
    print("=" * 70)
    print("DIBIE - Normalización de Datos Financieros")
    print("=" * 70)
    
    # 1. Cargar datos maestros
    print("\n1. Cargando datos maestros...")
    
    source_url = "https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc/edit?gid=1897725171"
    reader = GoogleSheetsReader()
    df_raw = reader.read_sheet(source_url)
    
    if df_raw is None or df_raw.empty:
        print("✗ No se pudieron cargar datos")
        return
    
    # Cargar maestro de instituciones
    maestro_path = Path("data/processed/maestro_instituciones.csv")
    df_maestro = pd.read_csv(maestro_path)
    
    print(f"   ✓ Datos maestros: {df_raw.shape[0]} filas, {df_raw.shape[1]} columnas")
    print(f"   ✓ Maestro instituciones: {df_maestro.shape[0]} instituciones")
    
    # 2. Cargar propuesta de tablas
    print("\n2. Cargando propuesta de tablas atómicas...")
    propuesta_path = Path("data/processed/propuesta_tablas_atomicas.json")
    
    with open(propuesta_path, 'r', encoding='utf-8') as f:
        propuesta = json.load(f)
    
    print(f"   ✓ {len(propuesta)} tablas propuestas")
    
    # 3. Crear directorio de salida
    output_dir = Path("data/normalized")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. Tabla 1: maestro_instituciones (ya existe, copiar)
    print("\n3. Creando tablas normalizadas...")
    print("\n   Tabla 1: maestro_instituciones")
    df_maestro.to_csv(output_dir / "maestro_instituciones.csv", index=False, encoding='utf-8')
    df_maestro.to_parquet(output_dir / "maestro_instituciones.parquet", index=False)
    print(f"      ✓ {len(df_maestro)} registros")
    
    # 5. Tabla 2: ubicacion_geografica
    print("\n   Tabla 2: ubicacion_geografica")
    df_ubicacion = df_maestro[['iebm_id', 'direccion', 'municipio', 'departamento', 'latitud', 'longitud']].copy()
    df_ubicacion.rename(columns={'iebm_id': 'institucion_id'}, inplace=True)
    df_ubicacion.to_csv(output_dir / "ubicacion_geografica.csv", index=False, encoding='utf-8')
    df_ubicacion.to_parquet(output_dir / "ubicacion_geografica.parquet", index=False)
    print(f"      ✓ {len(df_ubicacion)} registros")
    
    # 6. Tabla 3: hechos_financieros
    print("\n   Tabla 3: hechos_financieros")
    
    # Identificar columnas financieras
    columnas_financieras = propuesta.get('hechos_financieros', {}).get('columns', [])
    
    # Crear tabla de hechos
    hechos_data = []
    
    for idx, row in df_raw.iterrows():
        # Obtener id de institución del maestro
        cod_colegio = row.get('cod_colegio', '')
        institucion_match = df_maestro[df_maestro['dane_institucion'] == cod_colegio]
        
        if not institucion_match.empty:
            institucion_id = institucion_match.iloc[0]['iebm_id']
        else:
            institucion_id = idx + 1
        
        hecho = {
            'hecho_id': idx + 1,
            'institucion_id': institucion_id,
            'fecha_id': 2024  # Año actual, ajustar según datos reales
        }
        
        # Agregar columnas financieras disponibles
        for col in columnas_financieras:
            if col in df_raw.columns:
                valor = row.get(col, '')
                # Limpiar y convertir valores
                if pd.notna(valor) and str(valor).strip():
                    try:
                        # Intentar convertir a numérico
                        valor_limpio = str(valor).replace('$', '').replace(',', '').replace('.', '').strip()
                        hecho[col] = float(valor_limpio) if valor_limpio else 0
                    except:
                        hecho[col] = str(valor)
                else:
                    hecho[col] = 0
        
        hechos_data.append(hecho)
    
    df_hechos = pd.DataFrame(hechos_data)
    
    # Convertir columnas numéricas, manejando errores
    for col in df_hechos.columns:
        if col not in ['hecho_id', 'institucion_id', 'fecha_id']:
            df_hechos[col] = pd.to_numeric(df_hechos[col], errors='coerce').fillna(0)
    
    df_hechos.to_csv(output_dir / "hechos_financieros.csv", index=False, encoding='utf-8')
    df_hechos.to_parquet(output_dir / "hechos_financieros.parquet", index=False)
    print(f"      ✓ {len(df_hechos)} registros")
    print(f"      Columnas: {list(df_hechos.columns)}")
    
    # 7. Tabla 4: dim_tiempo
    print("\n   Tabla 4: dim_tiempo")
    
    columnas_tiempo = propuesta.get('dim_tiempo', {}).get('columns', [])
    
    tiempo_data = []
    for idx, row in df_raw.iterrows():
        cod_colegio = row.get('cod_colegio', '')
        institucion_match = df_maestro[df_maestro['dane_institucion'] == cod_colegio]
        
        if not institucion_match.empty:
            institucion_id = institucion_match.iloc[0]['iebm_id']
        else:
            institucion_id = idx + 1
        
        tiempo = {
            'fecha_id': 2024,
            'institucion_id': institucion_id,
            'ano': 2024,
            'periodo': 'Anual'
        }
        
        # Agregar columnas temporales
        for col in columnas_tiempo:
            if col in df_raw.columns:
                valor = row.get(col, '')
                if pd.notna(valor):
                    try:
                        tiempo[col] = float(str(valor).replace(',', '').replace('.', ''))
                    except:
                        tiempo[col] = str(valor)
                else:
                    tiempo[col] = 0
        
        tiempo_data.append(tiempo)
    
    df_tiempo = pd.DataFrame(tiempo_data)
    
    # Convertir columnas numéricas
    for col in df_tiempo.columns:
        if col not in ['fecha_id', 'institucion_id', 'ano', 'periodo']:
            df_tiempo[col] = pd.to_numeric(df_tiempo[col], errors='coerce').fillna(0)
    
    df_tiempo.to_csv(output_dir / "dim_tiempo.csv", index=False, encoding='utf-8')
    df_tiempo.to_parquet(output_dir / "dim_tiempo.parquet", index=False)
    print(f"      ✓ {len(df_tiempo)} registros")
    
    # 8. Resumen de archivos generados
    print("\n" + "=" * 70)
    print("Normalización completada!")
    print("=" * 70)
    print(f"\nArchivos generados en: {output_dir}")
    
    archivos = list(output_dir.glob("*.csv"))
    for archivo in archivos:
        size_kb = archivo.stat().st_size / 1024
        print(f"  - {archivo.name} ({size_kb:.1f} KB)")
    
    # 9. Crear metadata
    metadata = {
        "created_at": pd.Timestamp.now().isoformat(),
        "source": "Google Sheets - Maestro Financiero",
        "tables": {
            "maestro_instituciones": {
                "rows": len(df_maestro),
                "columns": list(df_maestro.columns),
                "file": "maestro_instituciones.csv"
            },
            "ubicacion_geografica": {
                "rows": len(df_ubicacion),
                "columns": list(df_ubicacion.columns),
                "file": "ubicacion_geografica.csv"
            },
            "hechos_financieros": {
                "rows": len(df_hechos),
                "columns": list(df_hechos.columns),
                "file": "hechos_financieros.csv"
            },
            "dim_tiempo": {
                "rows": len(df_tiempo),
                "columns": list(df_tiempo.columns),
                "file": "dim_tiempo.csv"
            }
        }
    }
    
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n  - metadata.json")
    print("\n✓ Datos listos para análisis y dashboards!")


if __name__ == "__main__":
    normalize_financial_data()
