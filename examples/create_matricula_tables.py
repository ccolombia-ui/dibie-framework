"""
DIBIE - Extraer y Normalizar Datos de Matrícula por Grado
Crear tabla paramétrica dim_grados y tabla de hechos hechos_matricula
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import json


def extract_matricula_data():
    """
    Extraer datos de matrícula por grado y crear tablas normalizadas
    """
    print("=" * 70)
    print("DIBIE - Extracción de Datos de Matrícula por Grado")
    print("=" * 70)
    
    # 1. Autenticar
    credentials_path = Path("config/credentials_google.json")
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # 2. Leer datos
    print("\n1. Leyendo datos de Google Sheets...")
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet("maestro")
    
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    print(f"   ✓ {len(df)} filas, {len(df.columns)} columnas")
    
    # 3. Mostrar todas las columnas para identificar las de matrícula
    print("\n2. Buscando columnas numeradas (1, 2, 3, etc.)...")
    
    # Buscar columnas que sean solo números o terminen en número
    numeric_columns = []
    for col in df.columns:
        col_stripped = str(col).strip()
        # Buscar columnas que sean exactamente un número del 1-11
        if col_stripped in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            numeric_columns.append(col)
            print(f"   ✓ Encontrada: '{col}'")
    
    if len(numeric_columns) == 0:
        print("\n   No se encontraron columnas con números exactos.")
        print("\n   Mostrando primeras 30 columnas para análisis manual:")
        for i, col in enumerate(df.columns[:30], 1):
            print(f"   {i}. '{col}'")
        return
    
    print(f"\n   Total columnas de matrícula encontradas: {len(numeric_columns)}")
    
    # 4. Crear tabla paramétrica dim_grados
    print("\n3. Creando tabla paramétrica: dim_grados")
    
    dim_grados = pd.DataFrame([
        {
            'grado_codigo': 'T',
            'grado_nombre': 'Transición',
            'grado_numero': 0,
            'nivel_educativo': 'Preescolar',
            'orden': 0,
            'descripcion': 'Grado de transición o jardín'
        },
        {
            'grado_codigo': '1',
            'grado_nombre': 'Primero',
            'grado_numero': 1,
            'nivel_educativo': 'Primaria',
            'orden': 1,
            'descripcion': 'Primer grado de primaria'
        },
        {
            'grado_codigo': '2',
            'grado_nombre': 'Segundo',
            'grado_numero': 2,
            'nivel_educativo': 'Primaria',
            'orden': 2,
            'descripcion': 'Segundo grado de primaria'
        },
        {
            'grado_codigo': '3',
            'grado_nombre': 'Tercero',
            'grado_numero': 3,
            'nivel_educativo': 'Primaria',
            'orden': 3,
            'descripcion': 'Tercer grado de primaria'
        },
        {
            'grado_codigo': '4',
            'grado_nombre': 'Cuarto',
            'grado_numero': 4,
            'nivel_educativo': 'Primaria',
            'orden': 4,
            'descripcion': 'Cuarto grado de primaria'
        },
        {
            'grado_codigo': '5',
            'grado_nombre': 'Quinto',
            'grado_numero': 5,
            'nivel_educativo': 'Primaria',
            'orden': 5,
            'descripcion': 'Quinto grado de primaria'
        },
        {
            'grado_codigo': '6',
            'grado_nombre': 'Sexto',
            'grado_numero': 6,
            'nivel_educativo': 'Secundaria',
            'orden': 6,
            'descripcion': 'Sexto grado - primer año de secundaria'
        },
        {
            'grado_codigo': '7',
            'grado_nombre': 'Séptimo',
            'grado_numero': 7,
            'nivel_educativo': 'Secundaria',
            'orden': 7,
            'descripcion': 'Séptimo grado - segundo año de secundaria'
        },
        {
            'grado_codigo': '8',
            'grado_nombre': 'Octavo',
            'grado_numero': 8,
            'nivel_educativo': 'Secundaria',
            'orden': 8,
            'descripcion': 'Octavo grado - tercer año de secundaria'
        },
        {
            'grado_codigo': '9',
            'grado_nombre': 'Noveno',
            'grado_numero': 9,
            'nivel_educativo': 'Secundaria',
            'orden': 9,
            'descripcion': 'Noveno grado - cuarto año de secundaria'
        },
        {
            'grado_codigo': '10',
            'grado_nombre': 'Décimo',
            'grado_numero': 10,
            'nivel_educativo': 'Media',
            'orden': 10,
            'descripcion': 'Décimo grado - primer año de media'
        },
        {
            'grado_codigo': '11',
            'grado_nombre': 'Once',
            'grado_numero': 11,
            'nivel_educativo': 'Media',
            'orden': 11,
            'descripcion': 'Once grado - último año de bachillerato'
        }
    ])
    
    print(f"   ✓ {len(dim_grados)} grados definidos")
    
    # 5. Crear tabla de hechos hechos_matricula
    print("\n4. Creando tabla de hechos: hechos_matricula")
    
    hechos_matricula_rows = []
    
    # Obtener columna de DANE
    dane_col = None
    for col in df.columns:
        if 'dane' in str(col).lower() and 'instituci' in str(col).lower():
            dane_col = col
            break
    
    if not dane_col:
        print("   ⚠ No se encontró columna DANE, usando índice")
    
    # Obtener columna de año
    anio = 2024  # Default
    
    for idx, row in df.iterrows():
        dane = row[dane_col] if dane_col else f"INST_{idx+1}"
        
        for col in numeric_columns:
            grado_codigo = col.strip()
            cantidad_str = row[col]
            
            # Convertir a número
            try:
                if cantidad_str and str(cantidad_str).strip() and str(cantidad_str).strip() != '-':
                    cantidad = int(str(cantidad_str).replace(',', '').replace('.', ''))
                else:
                    cantidad = 0
            except:
                cantidad = 0
            
            # Buscar información del grado
            grado_info = dim_grados[dim_grados['grado_codigo'] == grado_codigo]
            
            if len(grado_info) > 0:
                hechos_matricula_rows.append({
                    'dane_institucion': dane,
                    'anio': anio,
                    'grado_codigo': grado_codigo,
                    'grado_nombre': grado_info.iloc[0]['grado_nombre'],
                    'nivel_educativo': grado_info.iloc[0]['nivel_educativo'],
                    'cantidad_estudiantes': cantidad
                })
    
    hechos_matricula = pd.DataFrame(hechos_matricula_rows)
    
    print(f"   ✓ {len(hechos_matricula)} registros de matrícula creados")
    print(f"   ✓ Instituciones: {hechos_matricula['dane_institucion'].nunique()}")
    print(f"   ✓ Grados: {hechos_matricula['grado_codigo'].nunique()}")
    print(f"   ✓ Total estudiantes: {hechos_matricula['cantidad_estudiantes'].sum():,}")
    
    # 6. Guardar archivos
    print("\n5. Guardando archivos...")
    
    output_dir = Path("data/normalized")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV y Parquet
    dim_grados.to_csv(output_dir / "dim_grados.csv", index=False, encoding='utf-8')
    dim_grados.to_parquet(output_dir / "dim_grados.parquet", index=False)
    print(f"   ✓ dim_grados.csv")
    print(f"   ✓ dim_grados.parquet")
    
    hechos_matricula.to_csv(output_dir / "hechos_matricula.csv", index=False, encoding='utf-8')
    hechos_matricula.to_parquet(output_dir / "hechos_matricula.parquet", index=False)
    print(f"   ✓ hechos_matricula.csv")
    print(f"   ✓ hechos_matricula.parquet")
    
    # TSV
    tsv_dir = Path("data/tsv")
    tsv_dir.mkdir(parents=True, exist_ok=True)
    
    dim_grados.to_csv(tsv_dir / "dim_grados.tsv", sep='\t', index=False, encoding='utf-8')
    hechos_matricula.to_csv(tsv_dir / "hechos_matricula.tsv", sep='\t', index=False, encoding='utf-8')
    print(f"   ✓ dim_grados.tsv")
    print(f"   ✓ hechos_matricula.tsv")
    
    # 7. Mostrar muestra
    print("\n6. Muestra de datos:")
    print("\n   dim_grados (primeros 5):")
    print(dim_grados.head().to_string(index=False))
    
    print("\n   hechos_matricula (primeros 10):")
    print(hechos_matricula.head(10).to_string(index=False))
    
    # 8. Estadísticas por nivel
    print("\n7. Estadísticas por nivel educativo:")
    stats = hechos_matricula.groupby('nivel_educativo').agg({
        'cantidad_estudiantes': ['sum', 'mean', 'count']
    }).round(0)
    print(stats)
    
    print("\n✅ Tablas de matrícula creadas exitosamente!")
    
    return dim_grados, hechos_matricula


if __name__ == "__main__":
    extract_matricula_data()
