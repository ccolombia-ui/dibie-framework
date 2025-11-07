"""
DIBIE - Configurar Dashboards en Apache Superset
Crear base de datos SQLite y configurar Superset con datos normalizados
"""
import pandas as pd
import sqlite3
from pathlib import Path
import json


def create_sqlite_database():
    """
    Crear base de datos SQLite con datos normalizados
    """
    print("=" * 70)
    print("DIBIE - Configuración de Dashboards Apache Superset")
    print("=" * 70)
    
    # 1. Crear directorio de base de datos
    db_dir = Path("data/database")
    db_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = db_dir / "dibie_financiero.db"
    
    print(f"\n1. Creando base de datos SQLite...")
    print(f"   Ruta: {db_path}")
    
    # Conectar a SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Cargar datos normalizados
    print("\n2. Cargando datos normalizados...")
    normalized_dir = Path("data/normalized")
    
    # Tabla 1: maestro_instituciones
    print("\n   Tabla: maestro_instituciones")
    df_maestro = pd.read_csv(normalized_dir / "maestro_instituciones.csv")
    df_maestro.to_sql('maestro_instituciones', conn, if_exists='replace', index=False)
    print(f"      ✓ {len(df_maestro)} registros cargados")
    
    # Tabla 2: ubicacion_geografica
    print("\n   Tabla: ubicacion_geografica")
    df_ubicacion = pd.read_csv(normalized_dir / "ubicacion_geografica.csv")
    df_ubicacion.to_sql('ubicacion_geografica', conn, if_exists='replace', index=False)
    print(f"      ✓ {len(df_ubicacion)} registros cargados")
    
    # Tabla 3: hechos_financieros
    print("\n   Tabla: hechos_financieros")
    df_hechos = pd.read_csv(normalized_dir / "hechos_financieros.csv")
    df_hechos.to_sql('hechos_financieros', conn, if_exists='replace', index=False)
    print(f"      ✓ {len(df_hechos)} registros cargados")
    
    # Tabla 4: dim_tiempo
    print("\n   Tabla: dim_tiempo")
    df_tiempo = pd.read_csv(normalized_dir / "dim_tiempo.csv")
    df_tiempo.to_sql('dim_tiempo', conn, if_exists='replace', index=False)
    print(f"      ✓ {len(df_tiempo)} registros cargados")
    
    # 3. Crear vistas para análisis
    print("\n3. Creando vistas SQL para análisis...")
    
    # Vista 1: Instituciones con ubicación
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_instituciones_ubicacion AS
        SELECT 
            m.iebm_id,
            m.dane_institucion,
            m.nombre,
            u.direccion,
            u.municipio,
            u.departamento,
            u.latitud,
            u.longitud
        FROM maestro_instituciones m
        LEFT JOIN ubicacion_geografica u ON m.iebm_id = u.institucion_id
    """)
    print("      ✓ v_instituciones_ubicacion")
    
    # Vista 2: Análisis financiero completo
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_analisis_financiero AS
        SELECT 
            m.iebm_id,
            m.nombre,
            u.municipio,
            h.INGRESOS,
            h.EGRESOS,
            h."TOTAL INGRESOS (1+9)" as total_ingresos,
            (h.INGRESOS - h.EGRESOS) as balance,
            t."Numero de estudiantes (Total estudiantes matriculados el año anterior, incluyendo contratados con la secretaria)" as num_estudiantes,
            t."Costo por estudiante año anterior (en pesos) (Subtotal costo / Número de estudiantes)" as costo_por_estudiante
        FROM maestro_instituciones m
        LEFT JOIN ubicacion_geografica u ON m.iebm_id = u.institucion_id
        LEFT JOIN hechos_financieros h ON m.iebm_id = h.institucion_id
        LEFT JOIN dim_tiempo t ON m.iebm_id = t.institucion_id
    """)
    print("      ✓ v_analisis_financiero")
    
    # Vista 3: Top instituciones por ingresos
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_top_ingresos AS
        SELECT 
            m.nombre,
            u.municipio,
            h.INGRESOS,
            h."TOTAL INGRESOS (1+9)" as total_ingresos
        FROM maestro_instituciones m
        LEFT JOIN ubicacion_geografica u ON m.iebm_id = u.institucion_id
        LEFT JOIN hechos_financieros h ON m.iebm_id = h.institucion_id
        ORDER BY h.INGRESOS DESC
    """)
    print("      ✓ v_top_ingresos")
    
    conn.commit()
    
    # 4. Verificar tablas
    print("\n4. Verificando base de datos...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("   Tablas creadas:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"      - {table[0]}: {count} registros")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = cursor.fetchall()
    print("\n   Vistas creadas:")
    for view in views:
        print(f"      - {view[0]}")
    
    conn.close()
    
    # 5. Crear archivo de configuración para Superset
    print("\n5. Generando configuración de Superset...")
    
    superset_config = {
        "database_name": "DIBIE Financiero",
        "sqlalchemy_uri": f"sqlite:///{db_path.absolute()}",
        "dashboards": [
            {
                "name": "Análisis Financiero Instituciones",
                "charts": [
                    {
                        "name": "Mapa de Instituciones",
                        "type": "deck_polygon",
                        "dataset": "v_instituciones_ubicacion",
                        "metrics": ["COUNT(*)"],
                        "group_by": ["municipio"]
                    },
                    {
                        "name": "Ingresos vs Egresos",
                        "type": "bar",
                        "dataset": "v_analisis_financiero",
                        "metrics": ["SUM(INGRESOS)", "SUM(EGRESOS)"],
                        "group_by": ["nombre"]
                    },
                    {
                        "name": "Costo por Estudiante",
                        "type": "big_number",
                        "dataset": "v_analisis_financiero",
                        "metrics": ["AVG(costo_por_estudiante)"]
                    },
                    {
                        "name": "Top 10 Instituciones por Ingresos",
                        "type": "table",
                        "dataset": "v_top_ingresos",
                        "metrics": ["INGRESOS", "total_ingresos"],
                        "group_by": ["nombre", "municipio"],
                        "limit": 10
                    }
                ]
            }
        ]
    }
    
    config_path = db_dir / "superset_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(superset_config, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Configuración guardada en: {config_path}")
    
    # 6. Instrucciones
    print("\n" + "=" * 70)
    print("Base de datos SQLite creada exitosamente!")
    print("=" * 70)
    print(f"\nRuta de la base de datos: {db_path.absolute()}")
    print(f"\nURI de conexión para Superset:")
    print(f"  sqlite:///{db_path.absolute()}")
    
    print("\n" + "=" * 70)
    print("INSTRUCCIONES PARA APACHE SUPERSET")
    print("=" * 70)
    
    print("\n1. Iniciar Apache Superset:")
    print("   cd C:\\aguila\\dibie")
    print("   superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger")
    
    print("\n2. Acceder a Superset:")
    print("   http://localhost:8088")
    print("   Usuario: admin")
    print("   Contraseña: admin")
    
    print("\n3. Agregar Base de Datos:")
    print("   - Data → Databases → + Database")
    print(f"   - SQLALCHEMY URI: sqlite:///{db_path.absolute()}")
    print("   - Database Name: DIBIE Financiero")
    print("   - Test Connection → Connect")
    
    print("\n4. Agregar Datasets:")
    print("   - Data → Datasets → + Dataset")
    print("   - Database: DIBIE Financiero")
    print("   - Schema: main")
    print("   - Table: Seleccionar cada vista/tabla")
    print("     • v_instituciones_ubicacion")
    print("     • v_analisis_financiero")
    print("     • v_top_ingresos")
    
    print("\n5. Crear Charts:")
    print("   - Charts → + Chart")
    print("   - Seleccionar dataset y tipo de visualización")
    print("   - Configurar métricas y dimensiones")
    
    print("\n6. Crear Dashboard:")
    print("   - Dashboards → + Dashboard")
    print("   - Nombre: Análisis Financiero Instituciones")
    print("   - Arrastrar charts al dashboard")
    
    print("\n✓ ¡Configuración completada!")


if __name__ == "__main__":
    create_sqlite_database()
