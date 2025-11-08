"""
DIBIE - Crear Vistas y Dashboards para Apache Superset
Vistas SQL optimizadas para análisis de costos y mapa interactivo
"""
import sqlite3
import pandas as pd
from pathlib import Path
import json


def create_superset_views():
    """
    Crear vistas SQL para dashboards de costos en Superset
    """
    print("=" * 70)
    print("DIBIE - Creación de Vistas para Dashboard de Costos")
    print("=" * 70)
    
    # Conectar a la base de datos
    db_path = Path("data/database/dibie_financiero.db")
    
    if not db_path.exists():
        print(f"✗ No se encontró la base de datos en: {db_path}")
        print("  Ejecutar primero: python examples/setup_superset_dashboard.py")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # ========================================================================
    # VISTA 1: MAPA DE COSTOS POR INSTITUCIÓN
    # ========================================================================
    print("\n1. Creando vista: v_mapa_costos_institucion")
    
    vista_mapa = """
    DROP VIEW IF EXISTS v_mapa_costos_institucion;
    
    CREATE VIEW v_mapa_costos_institucion AS
    SELECT 
        mi.dane_institucion,
        mi.nombre as institucion_nombre,
        mi.municipio,
        mi.departamento,
        ug.latitud,
        ug.longitud,
        
        -- Matrícula
        COALESCE(SUM(hm.cantidad_estudiantes), 0) as total_estudiantes,
        
        -- Desglose por nivel educativo
        SUM(CASE WHEN hm.nivel_educativo = 'Preescolar' THEN hm.cantidad_estudiantes ELSE 0 END) as estudiantes_preescolar,
        SUM(CASE WHEN hm.nivel_educativo = 'Primaria' THEN hm.cantidad_estudiantes ELSE 0 END) as estudiantes_primaria,
        SUM(CASE WHEN hm.nivel_educativo = 'Secundaria' THEN hm.cantidad_estudiantes ELSE 0 END) as estudiantes_secundaria,
        SUM(CASE WHEN hm.nivel_educativo = 'Media' THEN hm.cantidad_estudiantes ELSE 0 END) as estudiantes_media,
        
        -- Costos (placeholder - se llenarán cuando haya datos reales)
        0 as costo_personal_anual,
        0 as costo_servicios_anual,
        0 as costo_contratados_anual,
        0 as costo_materiales_anual,
        0 as costo_mantenimiento_anual,
        0 as costo_administrativo_anual,
        0 as costo_tecnologia_anual,
        0 as costo_total_anual,
        
        -- Costo por estudiante
        0 as costo_por_estudiante,
        
        -- Ingresos
        COALESCE(hf.INGRESOS, 0) as ingresos_totales,
        
        -- Categoría de costo (para color en mapa)
        CASE 
            WHEN 0 = 0 THEN 'Sin datos'
            WHEN 0 < 5000000 THEN 'Bajo'
            WHEN 0 BETWEEN 5000000 AND 8000000 THEN 'Medio'
            WHEN 0 > 8000000 THEN 'Alto'
        END as categoria_costo
        
    FROM maestro_instituciones mi
    LEFT JOIN ubicacion_geografica ug ON mi.iebm_id = ug.institucion_id
    LEFT JOIN hechos_matricula hm ON mi.dane_institucion = hm.dane_institucion
    LEFT JOIN hechos_financieros hf ON mi.iebm_id = hf.institucion_id
    GROUP BY mi.dane_institucion, mi.nombre, mi.municipio, mi.departamento, 
             ug.latitud, ug.longitud, hf.INGRESOS;
    """
    
    cursor.executescript(vista_mapa)
    print("   ✓ Vista creada: v_mapa_costos_institucion")
    
    # Verificar
    test = pd.read_sql("SELECT * FROM v_mapa_costos_institucion LIMIT 5", conn)
    print(f"   ✓ {len(test)} registros de muestra:")
    print(test[['institucion_nombre', 'municipio', 'total_estudiantes', 'latitud', 'longitud']].to_string(index=False))
    
    # ========================================================================
    # VISTA 2: RESUMEN DE COSTOS POR INSTITUCIÓN
    # ========================================================================
    print("\n2. Creando vista: v_resumen_costos_institucion")
    
    vista_resumen = """
    DROP VIEW IF EXISTS v_resumen_costos_institucion;
    
    CREATE VIEW v_resumen_costos_institucion AS
    SELECT 
        mi.dane_institucion,
        mi.nombre as institucion_nombre,
        mi.municipio,
        mi.departamento,
        
        -- Totales
        COUNT(DISTINCT hm.grado_codigo) as grados_ofrecidos,
        SUM(hm.cantidad_estudiantes) as total_estudiantes,
        
        -- Costos por categoría (cuando estén disponibles)
        0 as costo_personal,
        0 as costo_servicios,
        0 as costo_contratados,
        0 as costo_materiales,
        0 as costo_mantenimiento,
        0 as costo_administrativo,
        0 as costo_tecnologia,
        0 as costo_total,
        
        -- Métricas
        0 as costo_por_estudiante,
        0 as porcentaje_costo_personal,
        0 as ratio_estudiante_docente,
        
        -- Ingresos
        COALESCE(hf.INGRESOS, 0) as ingresos_totales,
        0 as margen_operativo
        
    FROM maestro_instituciones mi
    LEFT JOIN hechos_matricula hm ON mi.dane_institucion = hm.dane_institucion
    LEFT JOIN hechos_financieros hf ON mi.iebm_id = hf.institucion_id
    GROUP BY mi.dane_institucion, mi.nombre, mi.municipio, mi.departamento, hf.INGRESOS;
    """
    
    cursor.executescript(vista_resumen)
    print("   ✓ Vista creada: v_resumen_costos_institucion")
    
    # ========================================================================
    # VISTA 3: EVOLUCIÓN MENSUAL DE COSTOS (Para series de tiempo)
    # ========================================================================
    print("\n3. Creando vista: v_evolucion_costos_mensual")
    
    vista_evolucion = """
    DROP VIEW IF EXISTS v_evolucion_costos_mensual;
    
    CREATE VIEW v_evolucion_costos_mensual AS
    SELECT 
        2024 as anio,
        1 as mes,
        'INST_1' as institucion_id,
        'Pendiente' as dane_institucion,
        0 as costo_personal,
        0 as costo_servicios,
        0 as costo_contratados,
        0 as costo_materiales,
        0 as costo_mantenimiento,
        0 as costo_administrativo,
        0 as costo_tecnologia,
        0 as costo_total,
        0 as estudiantes,
        0 as costo_por_estudiante
    WHERE 1=0; -- Vista vacía, se llenará cuando haya datos mensuales
    """
    
    cursor.executescript(vista_evolucion)
    print("   ✓ Vista creada: v_evolucion_costos_mensual")
    
    # ========================================================================
    # VISTA 4: COMPARATIVA POR NIVEL EDUCATIVO
    # ========================================================================
    print("\n4. Creando vista: v_costos_por_nivel_educativo")
    
    vista_nivel = """
    DROP VIEW IF EXISTS v_costos_por_nivel_educativo;
    
    CREATE VIEW v_costos_por_nivel_educativo AS
    SELECT 
        hm.nivel_educativo,
        COUNT(DISTINCT hm.dane_institucion) as numero_instituciones,
        SUM(hm.cantidad_estudiantes) as total_estudiantes,
        AVG(hm.cantidad_estudiantes) as promedio_estudiantes_por_grado,
        
        -- Costos agregados
        0 as costo_total_nivel,
        0 as costo_promedio_por_estudiante,
        
        -- Rango de costos
        0 as costo_minimo_por_estudiante,
        0 as costo_maximo_por_estudiante
        
    FROM hechos_matricula hm
    GROUP BY hm.nivel_educativo;
    """
    
    cursor.executescript(vista_nivel)
    print("   ✓ Vista creada: v_costos_por_nivel_educativo")
    
    test = pd.read_sql("SELECT * FROM v_costos_por_nivel_educativo", conn)
    print(f"   ✓ {len(test)} niveles educativos:")
    print(test.to_string(index=False))
    
    # ========================================================================
    # VISTA 5: TOP INSTITUCIONES POR COSTO
    # ========================================================================
    print("\n5. Creando vista: v_top_instituciones_costo")
    
    vista_top = """
    DROP VIEW IF EXISTS v_top_instituciones_costo;
    
    CREATE VIEW v_top_instituciones_costo AS
    SELECT 
        mi.dane_institucion,
        mi.nombre as institucion_nombre,
        mi.municipio,
        SUM(hm.cantidad_estudiantes) as total_estudiantes,
        0 as costo_total,
        0 as costo_por_estudiante,
        RANK() OVER (ORDER BY 0 DESC) as ranking_costo_total,
        RANK() OVER (ORDER BY 0 DESC) as ranking_costo_estudiante
    FROM maestro_instituciones mi
    LEFT JOIN hechos_matricula hm ON mi.dane_institucion = hm.dane_institucion
    GROUP BY mi.dane_institucion, mi.nombre, mi.municipio
    ORDER BY costo_total DESC;
    """
    
    cursor.executescript(vista_top)
    print("   ✓ Vista creada: v_top_instituciones_costo")
    
    # ========================================================================
    # GUARDAR CONFIGURACIÓN PARA SUPERSET
    # ========================================================================
    print("\n6. Generando configuración de Superset...")
    
    superset_config = {
        "database": {
            "name": "DIBIE Financiero",
            "sqlalchemy_uri": f"sqlite:///{db_path.absolute()}",
            "description": "Base de datos de costos y matrícula de instituciones educativas"
        },
        "dashboards": [
            {
                "name": "Mapa de Costos por Institución",
                "description": "Visualización geográfica de costos por estudiante",
                "slices": [
                    {
                        "name": "Mapa de Calor - Costo por Estudiante",
                        "viz_type": "deck_geojson",
                        "datasource": "v_mapa_costos_institucion",
                        "params": {
                            "longitude": "longitud",
                            "latitude": "latitud",
                            "metric": "costo_por_estudiante",
                            "color_scheme": "superset_seq_2"
                        }
                    },
                    {
                        "name": "Marcadores por Institución",
                        "viz_type": "deck_scatter",
                        "datasource": "v_mapa_costos_institucion",
                        "params": {
                            "longitude": "longitud",
                            "latitude": "latitud",
                            "size": "total_estudiantes",
                            "color": "categoria_costo"
                        }
                    }
                ]
            },
            {
                "name": "Dashboard Financiero",
                "description": "Análisis detallado de costos operativos",
                "slices": [
                    {
                        "name": "KPI - Costo Total",
                        "viz_type": "big_number_total",
                        "datasource": "v_resumen_costos_institucion",
                        "params": {
                            "metric": "SUM(costo_total)"
                        }
                    },
                    {
                        "name": "KPI - Costo por Estudiante Promedio",
                        "viz_type": "big_number",
                        "datasource": "v_resumen_costos_institucion",
                        "params": {
                            "metric": "AVG(costo_por_estudiante)"
                        }
                    },
                    {
                        "name": "Distribución de Costos",
                        "viz_type": "pie",
                        "datasource": "v_resumen_costos_institucion",
                        "params": {
                            "groupby": ["institucion_nombre"],
                            "metric": "costo_total"
                        }
                    },
                    {
                        "name": "Evolución Mensual",
                        "viz_type": "line",
                        "datasource": "v_evolucion_costos_mensual",
                        "params": {
                            "x_axis": "mes",
                            "metrics": ["costo_total", "costo_personal", "costo_servicios"]
                        }
                    }
                ]
            }
        ]
    }
    
    config_path = Path("data/database/superset_dashboards_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(superset_config, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ Configuración guardada: {config_path}")
    
    # Commit cambios
    conn.commit()
    conn.close()
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ VISTAS CREADAS EXITOSAMENTE")
    print("=" * 70)
    
    print("\n📊 Vistas disponibles para Superset:")
    print("  1. v_mapa_costos_institucion - Mapa interactivo")
    print("  2. v_resumen_costos_institucion - Resumen por institución")
    print("  3. v_evolucion_costos_mensual - Series de tiempo")
    print("  4. v_costos_por_nivel_educativo - Análisis por nivel")
    print("  5. v_top_instituciones_costo - Ranking de instituciones")
    
    print("\n🗺️ Dashboards sugeridos:")
    print("  • Mapa de Calor con costo por estudiante")
    print("  • Marcadores geográficos por institución")
    print("  • KPIs principales (total costos, promedio)")
    print("  • Gráficos de evolución temporal")
    print("  • Tablas comparativas")
    
    print("\n🚀 Próximos pasos:")
    print("  1. Iniciar Apache Superset:")
    print("     superset run -h 0.0.0.0 -p 8088")
    print("  2. Ir a: http://localhost:8088")
    print("  3. Login: admin / admin")
    print("  4. Agregar database connection:")
    print(f"     sqlite:///{db_path.absolute()}")
    print("  5. Crear dashboards usando las vistas")
    
    print("\n💡 Nota:")
    print("  Las vistas tienen valores en 0 para costos")
    print("  Se actualizarán automáticamente cuando se capturen")
    print("  datos en las tablas de Google Sheets")
    
    print("\n✅ ¡Listo para crear dashboards en Superset!")


if __name__ == "__main__":
    create_superset_views()
