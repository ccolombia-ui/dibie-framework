"""
DIBIE - Sincronizar datos de Google Sheets a SQLite para Superset
Carga datos de matrícula desde Google Sheets a base de datos local
"""
import sqlite3
import pandas as pd
from pathlib import Path
from google.oauth2.service_account import Credentials
import gspread
import json


def sync_sheets_to_sqlite():
    """
    Sincronizar datos de Google Sheets a SQLite para uso en Superset
    """
    print("=" * 70)
    print("DIBIE - Sincronización Google Sheets → SQLite")
    print("=" * 70)
    
    # Configuración Google Sheets
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc'
    
    # Autenticación
    print("\n1. Conectando a Google Sheets...")
    creds = Credentials.from_service_account_file(
        'config/credentials_google.json',
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    print("   ✓ Conectado a: maestro__dibie")
    
    # Crear/abrir base de datos SQLite
    db_path = Path("data/database/dibie_financiero.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"\n2. Base de datos: {db_path}")
    
    # ========================================================================
    # TABLA 1: dim_grados
    # ========================================================================
    print("\n3. Cargando dim_grados...")
    try:
        sheet = spreadsheet.worksheet('dim_grados')
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        df.to_sql('dim_grados', conn, if_exists='replace', index=False)
        print(f"   ✓ {len(df)} grados cargados")
        print(f"     Columnas: {', '.join(df.columns.tolist())}")
    except Exception as e:
        print(f"   ⚠ No se pudo cargar dim_grados: {e}")
    
    # ========================================================================
    # TABLA 2: hechos_matricula
    # ========================================================================
    print("\n4. Cargando hechos_matricula...")
    try:
        sheet = spreadsheet.worksheet('hechos_matricula')
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        df.to_sql('hechos_matricula', conn, if_exists='replace', index=False)
        print(f"   ✓ {len(df)} registros de matrícula cargados")
        print(f"     Total estudiantes: {df['cantidad_estudiantes'].sum():,.0f}")
    except Exception as e:
        print(f"   ⚠ No se pudo cargar hechos_matricula: {e}")
    
    # ========================================================================
    # TABLA 3: maestro_instituciones (desde CSV local)
    # ========================================================================
    print("\n5. Cargando maestro_instituciones...")
    try:
        csv_path = Path("data/normalized/maestro_instituciones.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_sql('maestro_instituciones', conn, if_exists='replace', index=False)
            print(f"   ✓ {len(df)} instituciones cargadas")
        else:
            print(f"   ⚠ No se encontró: {csv_path}")
    except Exception as e:
        print(f"   ⚠ Error: {e}")
    
    # ========================================================================
    # TABLA 4: ubicacion_geografica (desde CSV local)
    # ========================================================================
    print("\n6. Cargando ubicacion_geografica...")
    try:
        csv_path = Path("data/normalized/ubicacion_geografica.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_sql('ubicacion_geografica', conn, if_exists='replace', index=False)
            print(f"   ✓ {len(df)} ubicaciones cargadas")
        else:
            print(f"   ⚠ No se encontró: {csv_path}")
    except Exception as e:
        print(f"   ⚠ Error: {e}")
    
    # ========================================================================
    # TABLA 5: hechos_financieros (desde CSV local)
    # ========================================================================
    print("\n7. Cargando hechos_financieros...")
    try:
        csv_path = Path("data/normalized/hechos_financieros.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_sql('hechos_financieros', conn, if_exists='replace', index=False)
            print(f"   ✓ {len(df)} registros financieros cargados")
        else:
            print(f"   ⚠ No se encontró: {csv_path}")
    except Exception as e:
        print(f"   ⚠ Error: {e}")
    
    # ========================================================================
    # CREAR TABLAS DE COSTOS (vacías, se llenarán desde Google Sheets)
    # ========================================================================
    print("\n8. Creando tablas de costos...")
    
    # Estructura para costos_personal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS costos_personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institucion_id TEXT,
            dane_institucion TEXT,
            anio INTEGER,
            mes INTEGER,
            tipo_personal TEXT,
            numero_personas INTEGER,
            salario_promedio REAL,
            prestaciones_sociales REAL,
            bonificaciones REAL,
            otros_beneficios REAL,
            costo_total_mensual REAL,
            observaciones TEXT,
            fecha_registro TEXT
        );
    """)
    print("   ✓ costos_personal")
    
    # Estructura para servicios_publicos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios_publicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institucion_id TEXT,
            dane_institucion TEXT,
            anio INTEGER,
            mes INTEGER,
            tipo_servicio TEXT,
            proveedor TEXT,
            valor_base REAL,
            valor_consumo REAL,
            valor_otros_cargos REAL,
            valor_total REAL,
            observaciones TEXT,
            fecha_registro TEXT
        );
    """)
    print("   ✓ servicios_publicos")
    
    # Más tablas de costos...
    for tabla in ['servicios_contratados', 'materiales_suministros', 
                  'mantenimiento', 'gastos_administrativos', 'tecnologia_equipamiento']:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabla} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                institucion_id TEXT,
                dane_institucion TEXT,
                anio INTEGER,
                mes INTEGER,
                descripcion TEXT,
                valor_total REAL,
                observaciones TEXT,
                fecha_registro TEXT
            );
        """)
        print(f"   ✓ {tabla}")
    
    conn.commit()
    
    # ========================================================================
    # VERIFICAR DATOS CARGADOS
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 VERIFICACIÓN DE DATOS")
    print("=" * 70)
    
    tablas = ['dim_grados', 'hechos_matricula', 'maestro_instituciones', 
              'ubicacion_geografica', 'hechos_financieros']
    
    for tabla in tablas:
        try:
            result = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()
            print(f"  • {tabla:30s}: {result[0]:>6,} registros")
        except Exception as e:
            print(f"  • {tabla:30s}: ⚠ No disponible")
    
    # Guardar metadata
    metadata = {
        "database": str(db_path.absolute()),
        "created": pd.Timestamp.now().isoformat(),
        "source": "Google Sheets + CSV local",
        "spreadsheet_id": SPREADSHEET_ID,
        "tables": {}
    }
    
    for tabla in tablas:
        try:
            count = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
            metadata["tables"][tabla] = {"records": count}
        except:
            pass
    
    metadata_path = Path("data/database/metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n   ✓ Metadata guardada: {metadata_path}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ SINCRONIZACIÓN COMPLETADA")
    print("=" * 70)
    print(f"\n📂 Base de datos lista: {db_path}")
    print(f"   SQLite URI: sqlite:///{db_path.absolute()}")
    print("\n🚀 Siguiente paso: python examples\\create_superset_dashboard_views.py")


if __name__ == "__main__":
    sync_sheets_to_sqlite()
