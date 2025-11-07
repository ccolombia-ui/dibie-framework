# DIBIE - Data Intelligence Business Intelligence Engine

**Framework para gestión de espacio de trabajo de Google Drive con análisis de datos, Kusto, EventStreams y dashboards con Apache Superset**

[![GitHub](https://img.shields.io/badge/GitHub-dibie--framework-blue)](https://github.com/ccolombia-ui/dibie-framework)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Características

- ✅ **Sincronización con Google Drive** - Conexión directa con carpetas de Google Drive
- 📊 **Análisis de Datos** - Integración con Microsoft Fabric Kusto (KQL) y EventStreams
- 📈 **Dashboards Avanzados** - Generación de visualizaciones con Apache Superset
- 🔍 **Calidad de Datos** - Análisis automático de calidad y completitud
- 🚀 **Procesamiento en Tiempo Real** - Soporte para streaming de datos

## 📁 Estructura del Proyecto

```
dibie/
├── config/           # Configuración del framework
│   ├── paths.json              # Rutas de Google Drive
│   ├── google_workspace.json   # Config Google Workspace
│   ├── analysis.json           # Config Kusto/EventStreams
│   └── dashboard.json          # Config dashboards
├── data/            # Datos de entrada y procesados
│   ├── google_drive/  # Enlace a Google Drive (symlink)
│   ├── tables/        # Datasets en formato tabla
│   ├── documents/     # Documentos procesados
│   ├── processed/     # Datos procesados
│   └── cache/         # Caché temporal
├── src/             # Código fuente del framework
│   ├── ingestion/     # Módulos de ingesta de datos
│   ├── analysis/      # Módulos de análisis
│   └── dashboard/     # Generación de dashboard
├── dashboard/       # Dashboard y visualizaciones
│   ├── output/        # Resultados del dashboard
│   └── templates/     # Plantillas de visualización
├── examples/        # Ejemplos de uso
└── logs/            # Archivos de log
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/ccolombia-ui/dibie-framework.git
cd dibie-framework
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Google Drive
Ejecutar como **Administrador**:

**PowerShell:**
```powershell
.\setup_symlink.ps1
```

**CMD:**
```cmd
setup_symlink.bat
```

### 4. Ejecutar ejemplo básico
```bash
python examples\basic_usage.py
```

## 🔗 Configuración de Google Drive

### URL de Drive
https://drive.google.com/drive/folders/12cMgVfMlNvFFAPmHpHg1JENw7k7iDQzD

### Ruta Local
```
G:\.shortcut-targets-by-id\1fENbpuTdON265HSA0icoN8nHYS4gWJHF\_rafEl\aktriel\10_calidad_educativa_ud
```

El enlace simbólico se crea automáticamente con los scripts `setup_symlink.ps1` o `setup_symlink.bat`.

## 📊 Componentes del Framework

### 1. Ingesta de Datos
- Lectura de tablas (CSV, Excel, Google Sheets, Parquet)
- Procesamiento de documentos (Google Docs, PDF, DOCX)
- Sincronización automática con Google Drive

### 2. Análisis de Datos
- **Microsoft Fabric Kusto** - Queries KQL para análisis avanzado
- **EventStreams** - Procesamiento de datos en tiempo real
- **Análisis de Calidad** - Métricas automáticas de calidad de datos

### 3. Dashboards
- **Apache Superset** - Dashboards interactivos avanzados
- **Generación HTML** - Dashboards estáticos personalizables
- **KPIs y Métricas** - Visualización de indicadores clave

## 🛠️ Instalación de Apache Superset

```bash
# Instalar Superset
pip install apache-superset

# Inicializar base de datos
superset db upgrade

# Crear usuario admin
superset fab create-admin

# Cargar ejemplos (opcional)
superset load_examples

# Inicializar Superset
superset init

# Ejecutar servidor
superset run -p 8088 --with-threads --reload --debugger
```

Acceder a: http://localhost:8088

## 📖 Ejemplos de Uso

### Cargar y Analizar Tablas
```python
from ingestion.table_loader import TableLoader
from analysis.data_quality_analyzer import DataQualityAnalyzer

# Cargar tabla
loader = TableLoader()
df = loader.load_table("data/google_drive/data.csv")

# Analizar calidad
analyzer = DataQualityAnalyzer()
report = analyzer.generate_quality_report(df, "dataset_name")
print(f"Quality Score: {report['quality_score']}")
```

### Queries KQL
```python
from analysis.kusto_analyzer import KustoAnalyzer

analyzer = KustoAnalyzer()
query = analyzer.create_analysis_query("MyTable", "descriptive_statistics")
# Ejecutar query con MCP tools
```

### Generar Dashboard
```python
from dashboard.dashboard_generator import DashboardGenerator

generator = DashboardGenerator()
dashboard = generator.create_dashboard("Mi Dashboard", [])
generator.save_dashboard(dashboard, "output_name", format='html')
```

## 🔧 Configuración Avanzada

### Kusto/EventStreams
Editar `config/analysis.json`:
```json
{
  "kusto": {
    "cluster_uri": "https://your-cluster.kusto.windows.net",
    "database": "your_database"
  },
  "eventstream": {
    "workspace_id": "your-workspace-id"
  }
}
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **DIBIE Team** - *Trabajo Inicial* - [ccolombia-ui](https://github.com/ccolombia-ui)

## 🙏 Agradecimientos

- Microsoft Fabric Kusto
- Apache Superset
- Google Drive API
- Pandas & NumPy
