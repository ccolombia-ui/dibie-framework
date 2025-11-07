# DIBIE - Data Intelligence Business Intelligence Engine

Framework para gestión de espacio de trabajo de Google con análisis de datos y dashboard.

## Estructura del Proyecto

```
dibie/
├── config/           # Configuración del framework
│   └── paths.json   # Rutas de Google Drive y directorios
├── data/            # Datos de entrada y procesados
│   ├── tables/      # Datasets en formato tabla
│   ├── documents/   # Documentos de Google
│   ├── processed/   # Datos procesados
│   └── cache/       # Caché temporal
├── src/             # Código fuente del framework
│   ├── ingestion/   # Módulos de ingesta de datos
│   ├── analysis/    # Módulos de análisis
│   └── dashboard/   # Generación de dashboard
├── dashboard/       # Dashboard y visualizaciones
│   ├── output/      # Resultados del dashboard
│   └── templates/   # Plantillas de visualización
└── logs/            # Archivos de log
```

## Configuración de Google Drive

### Ruta Local
La carpeta de Google Drive está ubicada en:
```
G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud
```

### URL de Drive
https://drive.google.com/drive/folders/12cMgVfMlNvFFAPmHpHg1JENw7k7iDQzD

### Crear Enlace Simbólico (Requiere permisos de administrador)

**Opción 1: PowerShell como Administrador**
```powershell
New-Item -ItemType SymbolicLink -Path "c:\aguila\dibie\data\google_drive" -Target "G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud"
```

**Opción 2: CMD como Administrador**
```cmd
mklink /D "c:\aguila\dibie\data\google_drive" "G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud"
```

## Componentes del Framework

### 1. Ingesta de Datos
- Lectura de tablas (CSV, Excel, Google Sheets)
- Procesamiento de documentos (Google Docs, PDF)
- Sincronización con Google Drive

### 2. Análisis de Datos
- Integración con Microsoft Fabric Kusto
- Procesamiento con EventStreams
- Queries KQL para análisis avanzado

### 3. Dashboard
- Visualización de resultados
- Métricas y KPIs
- Reportes automáticos

## Próximos Pasos

1. Ejecutar el comando de enlace simbólico como administrador
2. Implementar módulos de ingesta de datos
3. Configurar conexión con servicios de análisis
4. Desarrollar dashboard de visualización
