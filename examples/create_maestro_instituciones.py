"""
DIBIE - Crear Tabla Maestro de Instituciones (Hoja 3)
Extrae datos de la tabla maestra y crea hoja maestro_instituciones
"""
import sys
from pathlib import Path
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.google_sheets_reader import GoogleSheetsReader


def create_maestro_instituciones_sheet(source_url: str, target_sheet_name: str = "maestro_instituciones"):
    """
    Crear hoja maestro_instituciones con estructura normalizada
    
    Columnas:
    - iebm_id (auto-incremental)
    - dane_institucion (código DANE)
    - nombre (nombre del colegio)
    - direccion
    - municipio
    - departamento
    - latitud (a completar)
    - longitud (a completar)
    """
    print("=" * 70)
    print("DIBIE - Creación de Tabla Maestro de Instituciones")
    print("=" * 70)
    
    # 1. Leer datos de la hoja maestro
    print("\n1. Leyendo datos de Google Sheets...")
    reader = GoogleSheetsReader()
    df = reader.read_sheet(source_url)
    
    if df is None or df.empty:
        print("✗ No se pudieron leer los datos")
        return
    
    # 2. Extraer columnas relevantes
    print("\n2. Extrayendo datos para maestro_instituciones...")
    
    # Identificar columnas disponibles
    cols_mapping = {
        'dane_institucion': None,
        'nombre': None,
        'direccion': None,
        'municipio': None
    }
    
    # Buscar columnas por nombre (case-insensitive)
    for col in df.columns:
        col_lower = str(col).lower()
        if 'cod' in col_lower and 'colegio' in col_lower:
            cols_mapping['dane_institucion'] = col
        elif 'nombre' in col_lower and 'colegio' in col_lower:
            cols_mapping['nombre'] = col
        elif 'direccion' in col_lower:
            cols_mapping['direccion'] = col
        elif 'municipio' in col_lower:
            cols_mapping['municipio'] = col
    
    print("   Columnas identificadas:")
    for key, value in cols_mapping.items():
        print(f"   - {key}: {value}")
    
    # 3. Crear DataFrame del maestro
    maestro_data = []
    for idx, row in df.iterrows():
        institucion = {
            'iebm_id': idx + 1,  # Auto-incremental
            'dane_institucion': row.get(cols_mapping['dane_institucion'], ''),
            'nombre': row.get(cols_mapping['nombre'], ''),
            'direccion': row.get(cols_mapping['direccion'], ''),
            'municipio': row.get(cols_mapping['municipio'], ''),
            'departamento': '',  # A completar manualmente o con geocoding
            'latitud': '',  # A completar con geocoding
            'longitud': ''  # A completar con geocoding
        }
        maestro_data.append(institucion)
    
    df_maestro = pd.DataFrame(maestro_data)
    
    print(f"\n   ✓ Maestro creado con {len(df_maestro)} instituciones")
    print("\n   Primeras 3 filas:")
    print(df_maestro.head(3).to_string(index=False))
    
    # 4. Autenticar con Google Sheets
    print("\n3. Conectando con Google Sheets...")
    credentials_path = Path("config/credentials_google.json")
    
    if not credentials_path.exists():
        print("✗ No se encontró config/credentials_google.json")
        print("\n   Guardando en CSV local...")
        csv_path = Path("data/processed/maestro_instituciones.csv")
        df_maestro.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"   ✓ Guardado en: {csv_path}")
        return
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # 5. Extraer spreadsheet ID de la URL
    sheet_id = reader.extract_sheet_id(source_url)
    print(f"   Spreadsheet ID: {sheet_id}")
    
    # 6. Abrir spreadsheet
    print(f"\n4. Creando hoja '{target_sheet_name}'...")
    try:
        spreadsheet = client.open_by_key(sheet_id)
        
        # Verificar si ya existe la hoja
        try:
            worksheet = spreadsheet.worksheet(target_sheet_name)
            print(f"   ⚠ La hoja '{target_sheet_name}' ya existe")
            response = input("   ¿Sobrescribir? (s/n): ")
            if response.lower() != 's':
                print("   Operación cancelada")
                return
            # Limpiar hoja existente
            worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            # Crear nueva hoja
            worksheet = spreadsheet.add_worksheet(
                title=target_sheet_name,
                rows=100,
                cols=8
            )
            print(f"   ✓ Hoja '{target_sheet_name}' creada")
        
        # 7. Escribir datos
        print("\n5. Escribiendo datos en Google Sheets...")
        
        # Escribir encabezados
        headers = df_maestro.columns.tolist()
        worksheet.update('A1', [headers])
        
        # Escribir datos
        data_rows = df_maestro.values.tolist()
        worksheet.update(f'A2:H{len(data_rows) + 1}', data_rows)
        
        print(f"   ✓ {len(df_maestro)} instituciones escritas exitosamente")
        
        # 8. Formatear encabezados
        print("\n6. Aplicando formato...")
        worksheet.format('A1:H1', {
            'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
            'horizontalAlignment': 'CENTER'
        })
        
        # Congelar fila de encabezados
        worksheet.freeze(rows=1)
        
        print("   ✓ Formato aplicado")
        
        # 9. URL de la hoja creada
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={worksheet.id}"
        print(f"\n✓ Hoja creada exitosamente!")
        print(f"   URL: {sheet_url}")
        
        # 10. Guardar también en CSV local
        csv_path = Path("data/processed/maestro_instituciones.csv")
        df_maestro.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"   CSV guardado en: {csv_path}")
        
    except Exception as e:
        print(f"✗ Error al crear hoja: {e}")
        print("\n   Guardando en CSV local...")
        csv_path = Path("data/processed/maestro_instituciones.csv")
        df_maestro.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"   ✓ Guardado en: {csv_path}")
    
    print("\n" + "=" * 70)
    print("Proceso completado!")
    print("=" * 70)
    print("\nPróximos pasos:")
    print("1. Revisar datos en Google Sheets")
    print("2. Completar columna 'departamento' manualmente")
    print("3. Ejecutar geocoding para obtener latitud/longitud")


if __name__ == "__main__":
    source_url = "https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc/edit?gid=1897725171"
    create_maestro_instituciones_sheet(source_url)
