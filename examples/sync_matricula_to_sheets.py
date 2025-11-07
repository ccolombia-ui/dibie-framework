"""
DIBIE - Sincronizar Tablas de Matrícula a Google Sheets
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import time


def sync_matricula_to_sheets():
    """
    Sincronizar dim_grados y hechos_matricula a Google Sheets
    """
    print("=" * 70)
    print("DIBIE - Sincronización de Tablas de Matrícula")
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
    
    # 2. Abrir spreadsheet
    print("\n1. Conectando a Google Sheets...")
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    spreadsheet = client.open_by_key(spreadsheet_id)
    print(f"   ✓ {spreadsheet.title}")
    
    # 3. Cargar datos
    print("\n2. Cargando datos locales...")
    normalized_dir = Path("data/normalized")
    
    dim_grados = pd.read_csv(normalized_dir / "dim_grados.csv")
    hechos_matricula = pd.read_csv(normalized_dir / "hechos_matricula.csv")
    
    print(f"   ✓ dim_grados: {len(dim_grados)} registros")
    print(f"   ✓ hechos_matricula: {len(hechos_matricula)} registros")
    
    # 4. Sincronizar dim_grados
    print("\n3. Sincronizando dim_grados...")
    
    try:
        worksheet = spreadsheet.worksheet("dim_grados")
        worksheet.clear()
        print("   ⚠ Hoja existente limpiada")
    except:
        worksheet = spreadsheet.add_worksheet(
            title="dim_grados",
            rows=20,
            cols=7
        )
        print("   ✓ Hoja creada")
    
    # Escribir datos
    headers = dim_grados.columns.tolist()
    worksheet.update(values=[headers], range_name='A1')
    
    data_rows = dim_grados.astype(str).values.tolist()
    if len(data_rows) > 0:
        end_col = chr(65 + len(headers) - 1)
        worksheet.update(
            values=data_rows,
            range_name=f'A2:{end_col}{len(data_rows) + 1}'
        )
    
    # Formato
    worksheet.format('A1:Z1', {
        'backgroundColor': {'red': 0.4, 'green': 0.2, 'blue': 0.8},
        'textFormat': {
            'bold': True,
            'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
        },
        'horizontalAlignment': 'CENTER'
    })
    worksheet.freeze(rows=1)
    
    print(f"   ✓ {len(dim_grados)} registros sincronizados")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={worksheet.id}")
    
    time.sleep(1)
    
    # 5. Sincronizar hechos_matricula
    print("\n4. Sincronizando hechos_matricula...")
    
    try:
        worksheet = spreadsheet.worksheet("hechos_matricula")
        worksheet.clear()
        print("   ⚠ Hoja existente limpiada")
    except:
        worksheet = spreadsheet.add_worksheet(
            title="hechos_matricula",
            rows=max(300, len(hechos_matricula) + 10),
            cols=7
        )
        print("   ✓ Hoja creada")
    
    # Escribir datos
    headers = hechos_matricula.columns.tolist()
    worksheet.update(values=[headers], range_name='A1')
    
    data_rows = hechos_matricula.astype(str).values.tolist()
    if len(data_rows) > 0:
        end_col = chr(65 + len(headers) - 1)
        worksheet.update(
            values=data_rows,
            range_name=f'A2:{end_col}{len(data_rows) + 1}'
        )
    
    # Formato
    worksheet.format('A1:Z1', {
        'backgroundColor': {'red': 0.4, 'green': 0.2, 'blue': 0.8},
        'textFormat': {
            'bold': True,
            'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
        },
        'horizontalAlignment': 'CENTER'
    })
    worksheet.freeze(rows=1)
    
    print(f"   ✓ {len(hechos_matricula)} registros sincronizados")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={worksheet.id}")
    
    # 6. Resumen
    print("\n" + "=" * 70)
    print("✅ Sincronización completada!")
    print("=" * 70)
    
    print("\nTablas creadas:")
    print("  1. dim_grados (tabla paramétrica de grados educativos)")
    print(f"     - {len(dim_grados)} grados (Transición a Once)")
    print("     - Niveles: Preescolar, Primaria, Secundaria, Media")
    
    print("\n  2. hechos_matricula (tabla de hechos)")
    print(f"     - {len(hechos_matricula)} registros")
    print(f"     - {hechos_matricula['dane_institucion'].nunique()} instituciones")
    print(f"     - {hechos_matricula['cantidad_estudiantes'].sum():,} estudiantes totales")
    
    print(f"\n📊 Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")


if __name__ == "__main__":
    sync_matricula_to_sheets()
