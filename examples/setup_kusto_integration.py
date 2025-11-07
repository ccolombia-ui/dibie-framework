"""
DIBIE - Integración con Microsoft Fabric Kusto
Generar scripts KQL para crear tablas e ingestar datos
"""
import pandas as pd
from pathlib import Path
import json


def generate_kusto_integration():
    """
    Generar scripts KQL y datos para Microsoft Fabric Kusto
    """
    print("=" * 70)
    print("DIBIE - Integración con Microsoft Fabric Kusto")
    print("=" * 70)
    
    # 1. Crear directorio de salida
    kusto_dir = Path("data/kusto")
    kusto_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n1. Generando scripts KQL...")
    
    # 2. Script de creación de tablas
    create_tables_kql = """
// ============================================================
// DIBIE - Microsoft Fabric Kusto Database Schema
// ============================================================
// Fecha: 2025-11-07
// Descripción: Esquema para análisis de datos financieros
//              de instituciones educativas
// ============================================================

// 1. Tabla: MaestroInstituciones
.create table MaestroInstituciones (
    iebm_id: int,
    dane_institucion: string,
    nombre: string
)

// 2. Tabla: UbicacionGeografica
.create table UbicacionGeografica (
    institucion_id: int,
    direccion: string,
    municipio: string,
    departamento: string,
    latitud: real,
    longitud: real
)

// 3. Tabla: HechosFinancieros
.create table HechosFinancieros (
    hecho_id: int,
    institucion_id: int,
    fecha_id: int,
    valor_lote: real,
    ingresos: real,
    egresos: real,
    total_ingresos: real,
    ingresos_operacion: real,
    valor_servicio_educativo: real,
    ingresos_otros_cobros: real,
    ingresos_no_operacionales: real
)

// 4. Tabla: DimTiempo
.create table DimTiempo (
    fecha_id: int,
    institucion_id: int,
    ano: int,
    periodo: string,
    numero_estudiantes: int,
    costo_por_estudiante: real
)

// ============================================================
// Políticas de Retención y Caché
// ============================================================

// Retención de 365 días
.alter table MaestroInstituciones policy retention softdelete = 365d
.alter table UbicacionGeografica policy retention softdelete = 365d
.alter table HechosFinancieros policy retention softdelete = 365d
.alter table DimTiempo policy retention softdelete = 365d

// Caché activo de 30 días
.alter table HechosFinancieros policy caching hot = 30d
.alter table DimTiempo policy caching hot = 30d
"""
    
    create_tables_path = kusto_dir / "01_create_tables.kql"
    with open(create_tables_path, 'w', encoding='utf-8') as f:
        f.write(create_tables_kql)
    
    print(f"   ✓ {create_tables_path.name}")
    
    # 3. Script de ingesta desde CSV
    ingest_kql = """
// ============================================================
// DIBIE - Ingesta de Datos desde CSV
// ============================================================

// Opción 1: Ingesta desde Azure Blob Storage
// ----------------------------------------------------------
.ingest into table MaestroInstituciones (
    h'https://yourstorageaccount.blob.core.windows.net/dibie/maestro_instituciones.csv'
) with (ignoreFirstRecord=true)

.ingest into table UbicacionGeografica (
    h'https://yourstorageaccount.blob.core.windows.net/dibie/ubicacion_geografica.csv'
) with (ignoreFirstRecord=true)

.ingest into table HechosFinancieros (
    h'https://yourstorageaccount.blob.core.windows.net/dibie/hechos_financieros.csv'
) with (ignoreFirstRecord=true)

.ingest into table DimTiempo (
    h'https://yourstorageaccount.blob.core.windows.net/dibie/dim_tiempo.csv'
) with (ignoreFirstRecord=true)


// Opción 2: Ingesta Inline (datos pequeños)
// ----------------------------------------------------------
// Ver archivo: 02_ingest_inline.kql


// Opción 3: Ingesta desde local (Kusto Explorer)
// ----------------------------------------------------------
// 1. Abrir Kusto Explorer
// 2. Conectar a tu cluster
// 3. Click derecho en tabla → Ingest data
// 4. Seleccionar archivo CSV
// 5. Mapear columnas
// 6. Ingerir
"""
    
    ingest_path = kusto_dir / "02_ingest_data.kql"
    with open(ingest_path, 'w', encoding='utf-8') as f:
        f.write(ingest_kql)
    
    print(f"   ✓ {ingest_path.name}")
    
    # 4. Queries de análisis
    queries_kql = """
// ============================================================
// DIBIE - Queries de Análisis KQL
// ============================================================

// 1. Vista consolidada de instituciones con ubicación
// ----------------------------------------------------------
MaestroInstituciones
| join kind=leftouter UbicacionGeografica on $left.iebm_id == $right.institucion_id
| project iebm_id, dane_institucion, nombre, direccion, municipio, 
          departamento, latitud, longitud


// 2. Análisis financiero completo
// ----------------------------------------------------------
MaestroInstituciones
| join kind=leftouter UbicacionGeografica on $left.iebm_id == $right.institucion_id
| join kind=leftouter HechosFinancieros on $left.iebm_id == $right.institucion_id
| join kind=leftouter DimTiempo on $left.iebm_id == $right.institucion_id
| project nombre, municipio, ingresos, egresos, total_ingresos, 
          balance = ingresos - egresos,
          numero_estudiantes, costo_por_estudiante
| order by ingresos desc


// 3. Top 10 instituciones por ingresos
// ----------------------------------------------------------
HechosFinancieros
| join kind=inner MaestroInstituciones on $left.institucion_id == $right.iebm_id
| join kind=inner UbicacionGeografica on $left.institucion_id == $right.institucion_id
| project nombre, municipio, ingresos, total_ingresos
| top 10 by ingresos desc


// 4. Distribución geográfica de instituciones
// ----------------------------------------------------------
UbicacionGeografica
| summarize count() by municipio, departamento
| order by count_ desc


// 5. Análisis de costo por estudiante
// ----------------------------------------------------------
DimTiempo
| join kind=inner MaestroInstituciones on $left.institucion_id == $right.iebm_id
| where numero_estudiantes > 0
| project nombre, numero_estudiantes, costo_por_estudiante
| extend categoria = case(
    costo_por_estudiante < 1000000, "Bajo",
    costo_por_estudiante < 5000000, "Medio",
    "Alto"
)
| summarize count() by categoria


// 6. Mapa de calor - Instituciones por municipio
// ----------------------------------------------------------
UbicacionGeografica
| where isnotempty(latitud) and isnotempty(longitud)
| project municipio, latitud, longitud
| render scatterchart with (kind=map)


// 7. Tendencia financiera (si hubiera datos históricos)
// ----------------------------------------------------------
HechosFinancieros
| join kind=inner DimTiempo on $left.institucion_id == $right.institucion_id
| summarize 
    avg_ingresos = avg(ingresos),
    avg_egresos = avg(egresos),
    total_instituciones = dcount(institucion_id)
    by ano
| order by ano asc


// 8. Balance financiero por institución
// ----------------------------------------------------------
HechosFinancieros
| join kind=inner MaestroInstituciones on $left.institucion_id == $right.iebm_id
| extend balance = ingresos - egresos
| extend estado = case(
    balance > 0, "Superávit",
    balance < 0, "Déficit",
    "Equilibrio"
)
| project nombre, ingresos, egresos, balance, estado
| order by balance desc


// 9. Instituciones sin datos geográficos
// ----------------------------------------------------------
UbicacionGeografica
| where isempty(latitud) or isempty(longitud)
| join kind=inner MaestroInstituciones on $left.institucion_id == $right.iebm_id
| project nombre, municipio, direccion


// 10. Dashboard ejecutivo
// ----------------------------------------------------------
let total_ingresos = toscalar(HechosFinancieros | summarize sum(ingresos));
let total_egresos = toscalar(HechosFinancieros | summarize sum(egresos));
let total_instituciones = toscalar(MaestroInstituciones | count);
let total_estudiantes = toscalar(DimTiempo | summarize sum(numero_estudiantes));

print 
    TotalInstituciones = total_instituciones,
    TotalIngresos = total_ingresos,
    TotalEgresos = total_egresos,
    Balance = total_ingresos - total_egresos,
    TotalEstudiantes = total_estudiantes,
    CostoPromedioEstudiante = total_egresos / total_estudiantes
"""
    
    queries_path = kusto_dir / "03_queries_analisis.kql"
    with open(queries_path, 'w', encoding='utf-8') as f:
        f.write(queries_kql)
    
    print(f"   ✓ {queries_path.name}")
    
    # 5. Generar archivo de configuración
    print("\n2. Generando configuración de Kusto...")
    
    kusto_config = {
        "cluster_uri": "https://your-cluster.kusto.windows.net",
        "database": "dibie_financiero",
        "tables": [
            {
                "name": "MaestroInstituciones",
                "file": "maestro_instituciones.csv",
                "rows": 22
            },
            {
                "name": "UbicacionGeografica",
                "file": "ubicacion_geografica.csv",
                "rows": 22
            },
            {
                "name": "HechosFinancieros",
                "file": "hechos_financieros.csv",
                "rows": 22
            },
            {
                "name": "DimTiempo",
                "file": "dim_tiempo.csv",
                "rows": 22
            }
        ],
        "authentication": {
            "method": "AAD",
            "tenant_id": "your-tenant-id",
            "client_id": "your-client-id"
        }
    }
    
    config_path = kusto_dir / "kusto_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(kusto_config, f, indent=2, ensure_ascii=False)
    
    print(f"   ✓ {config_path.name}")
    
    # 6. Copiar archivos CSV al directorio Kusto
    print("\n3. Copiando archivos CSV...")
    normalized_dir = Path("data/normalized")
    
    csv_files = [
        "maestro_instituciones.csv",
        "ubicacion_geografica.csv",
        "hechos_financieros.csv",
        "dim_tiempo.csv"
    ]
    
    for csv_file in csv_files:
        source = normalized_dir / csv_file
        dest = kusto_dir / csv_file
        
        if source.exists():
            df = pd.read_csv(source)
            df.to_csv(dest, index=False, encoding='utf-8')
            print(f"   ✓ {csv_file} ({len(df)} registros)")
    
    # 7. Instrucciones
    print("\n" + "=" * 70)
    print("Integración con Kusto configurada!")
    print("=" * 70)
    print(f"\nArchivos generados en: {kusto_dir}")
    
    print("\n" + "=" * 70)
    print("INSTRUCCIONES PARA MICROSOFT FABRIC KUSTO")
    print("=" * 70)
    
    print("\n1. Crear KQL Database en Microsoft Fabric:")
    print("   - Ir a Microsoft Fabric portal")
    print("   - Create → More options → Real-Time Intelligence")
    print("   - KQL Database → Nombre: dibie_financiero")
    
    print("\n2. Ejecutar Scripts de Creación:")
    print(f"   - Abrir: {create_tables_path}")
    print("   - Copiar contenido al Query Editor")
    print("   - Ejecutar todas las declaraciones .create table")
    
    print("\n3. Ingestar Datos:")
    print("   Opción A - One-click ingestion:")
    print("     1. Click en tabla → Ingest data")
    print("     2. Source: Local files")
    print("     3. Seleccionar CSV correspondiente")
    print("     4. Mapear columnas")
    print("     5. Start ingestion")
    
    print("\n   Opción B - Blob Storage:")
    print("     1. Subir CSVs a Azure Blob Storage")
    print(f"     2. Editar script: {ingest_path}")
    print("     3. Reemplazar URLs con tus blobs")
    print("     4. Ejecutar script de ingesta")
    
    print("\n4. Ejecutar Queries de Análisis:")
    print(f"   - Abrir: {queries_path}")
    print("   - Ejecutar queries según necesidad")
    print("   - Crear dashboards visuales")
    
    print("\n5. Crear Dashboard Real-Time:")
    print("   - Crear nuevo Dashboard en Fabric")
    print("   - Agregar tiles con queries KQL")
    print("   - Configurar auto-refresh")
    
    print("\n✓ ¡Configuración completada!")
    print("\nArchivos listos para ingesta:")
    for csv_file in csv_files:
        print(f"  - {kusto_dir / csv_file}")


if __name__ == "__main__":
    generate_kusto_integration()
