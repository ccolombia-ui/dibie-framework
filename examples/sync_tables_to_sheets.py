"""
DIBIE - Sincronizar Tablas Normalizadas con Google Sheets
Crear hojas individuales para cada tabla normalizada
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import time


def sync_normalized_tables_to_sheets():
    """
    Sincronizar todas las tablas normalizadas a Google Sheets
    """
    print("=" * 70)
    print("DIBIE - Sincronización de Tablas Normalizadas a Google Sheets")
    print("=" * 70)
    
    # 1. Configuración
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    credentials_path = Path("config/credentials_google.json")
    normalized_dir = Path("data/normalized")
    
    if not credentials_path.exists():
        print("✗ No se encontró config/credentials_google.json")
        return
    
    # 2. Autenticar
    print("\n1. Autenticando con Google Sheets...")
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # 3. Abrir spreadsheet
    print(f"   Abriendo spreadsheet: {spreadsheet_id}")
    spreadsheet = client.open_by_key(spreadsheet_id)
    print(f"   ✓ Conectado a: {spreadsheet.title}")
    
    # 4. Definir tablas a sincronizar
    tables_to_sync = [
        {
            "csv_file": "maestro_instituciones.csv",
            "sheet_name": "maestro_instituciones",
            "description": "Catálogo de instituciones educativas"
        },
        {
            "csv_file": "ubicacion_geografica.csv",
            "sheet_name": "ubicacion_geografica",
            "description": "Información geográfica y coordenadas"
        },
        {
            "csv_file": "hechos_financieros.csv",
            "sheet_name": "hechos_financieros",
            "description": "Datos financieros (ingresos, egresos)"
        },
        {
            "csv_file": "dim_tiempo.csv",
            "sheet_name": "dim_tiempo",
            "description": "Dimensión temporal y estudiantes"
        },
        {
            "csv_file": "dim_grados.csv",
            "sheet_name": "dim_grados",
            "description": "Tabla paramétrica de grados educativos (T-11)"
        },
        {
            "csv_file": "hechos_matricula.csv",
            "sheet_name": "hechos_matricula",
            "description": "Matrícula por institución y grado"
        }
    ]
    
    # 5. Guardar en formato TSV (tab-separated)
    print("\n2. Convirtiendo CSV a TSV (evita problemas con comas)...")
    tsv_dir = Path("data/tsv")
    tsv_dir.mkdir(parents=True, exist_ok=True)
    
    for table in tables_to_sync:
        csv_path = normalized_dir / table["csv_file"]
        tsv_path = tsv_dir / table["csv_file"].replace(".csv", ".tsv")
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_csv(tsv_path, sep='\t', index=False, encoding='utf-8')
            print(f"   ✓ {table['csv_file']} → {tsv_path.name}")
        else:
            print(f"   ⚠ No se encontró {csv_path}")
    
    # 6. Sincronizar cada tabla
    print("\n3. Sincronizando tablas con Google Sheets...")
    
    for i, table in enumerate(tables_to_sync, 1):
        print(f"\n   Tabla {i}/{len(tables_to_sync)}: {table['sheet_name']}")
        
        csv_path = normalized_dir / table["csv_file"]
        
        if not csv_path.exists():
            print(f"      ✗ No se encontró {csv_path}")
            continue
        
        # Leer datos
        df = pd.read_csv(csv_path)
        print(f"      Datos: {len(df)} filas, {len(df.columns)} columnas")
        
        # Verificar si la hoja ya existe
        try:
            worksheet = spreadsheet.worksheet(table["sheet_name"])
            print(f"      ⚠ La hoja ya existe, limpiando...")
            worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            # Crear nueva hoja
            worksheet = spreadsheet.add_worksheet(
                title=table["sheet_name"],
                rows=max(100, len(df) + 10),
                cols=len(df.columns) + 2
            )
            print(f"      ✓ Hoja creada")
        
        # Escribir encabezados
        headers = df.columns.tolist()
        worksheet.update(values=[headers], range_name='A1')
        
        # Escribir datos
        data_rows = df.astype(str).values.tolist()  # Convertir todo a string
        if len(data_rows) > 0:
            end_col = chr(65 + len(headers) - 1)  # A=65
            worksheet.update(
                values=data_rows,
                range_name=f'A2:{end_col}{len(data_rows) + 1}'
            )
        
        print(f"      ✓ {len(df)} registros escritos")
        
        # Aplicar formato al encabezado
        worksheet.format('A1:Z1', {
            'backgroundColor': {'red': 0.2, 'green': 0.5, 'blue': 0.8},
            'textFormat': {
                'bold': True,
                'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
            },
            'horizontalAlignment': 'CENTER'
        })
        
        # Congelar fila de encabezados
        worksheet.freeze(rows=1)
        
        # Agregar nota con descripción
        worksheet.update_note('A1', table['description'])
        
        print(f"      ✓ Formato aplicado")
        
        # URL de la hoja
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={worksheet.id}"
        print(f"      URL: {sheet_url}")
        
        # Pausa para evitar límites de tasa
        if i < len(tables_to_sync):
            time.sleep(1)
    
    # 7. Crear hoja de metadata
    print(f"\n4. Creando hoja de metadata...")
    
    # Leer metadata
    metadata_path = normalized_dir / "metadata.json"
    if metadata_path.exists():
        import json
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Crear o limpiar hoja de metadata
        try:
            meta_worksheet = spreadsheet.worksheet("_metadata")
            meta_worksheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            meta_worksheet = spreadsheet.add_worksheet(
                title="_metadata",
                rows=50,
                cols=5
            )
        
        # Preparar datos de metadata
        meta_data = [
            ["DIBIE - Metadata de Tablas Normalizadas"],
            [""],
            ["Fecha de Creación:", metadata.get("created_at", "N/A")],
            ["Fuente:", metadata.get("source", "N/A")],
            [""],
            ["Tabla", "Archivo", "Filas", "Columnas", "Descripción"]
        ]
        
        for table_name, table_info in metadata.get("tables", {}).items():
            meta_data.append([
                table_name,
                table_info.get("file", ""),
                table_info.get("rows", 0),
                len(table_info.get("columns", [])),
                ", ".join(table_info.get("columns", [])[:5]) + "..."
            ])
        
        # Escribir metadata
        meta_worksheet.update(values=meta_data, range_name='A1')
        
        # Formato
        meta_worksheet.format('A1', {
            'textFormat': {'bold': True, 'fontSize': 14},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        meta_worksheet.format('A6:E6', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}
        })
        
        print(f"   ✓ Metadata creada")
    
    # 8. Resumen
    print("\n" + "=" * 70)
    print("Sincronización completada!")
    print("=" * 70)
    
    print(f"\nSpreadsheet: {spreadsheet.title}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    
    print("\nHojas creadas/actualizadas:")
    for table in tables_to_sync:
        print(f"  ✓ {table['sheet_name']}")
    print(f"  ✓ _metadata")
    
    print("\n📁 Archivos TSV generados en: data/tsv/")
    print("   (Formato separado por tabuladores, sin problemas con comas)")
    
    print("\n💡 Nota:")
    print("   Las coordenadas geográficas ahora están en formato TSV")
    print("   No habrá conflictos con las comas decimales")
    
    print("\n✅ ¡Todas las tablas sincronizadas con Google Sheets!")


if __name__ == "__main__":
    sync_normalized_tables_to_sheets()
