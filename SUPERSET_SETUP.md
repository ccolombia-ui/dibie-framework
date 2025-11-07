# DIBIE - Guía de Instalación y Configuración de Superset

## 🚀 Instalación Rápida de Apache Superset

### Opción 1: Instalación Automática (Recomendado)

```bash
python examples\superset_setup.py
```

Este script:
1. Verifica si Superset está instalado
2. Instala Superset si es necesario
3. Inicializa la base de datos
4. Crea un usuario administrador
5. Inicia el servidor

### Opción 2: Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variable de entorno
set SUPERSET_CONFIG_PATH=c:\aguila\dibie\config\superset_config.py

# 3. Inicializar base de datos
superset db upgrade

# 4. Crear usuario admin
superset fab create-admin

# 5. Inicializar Superset
superset init

# 6. Ejecutar servidor
superset run -p 8088 --with-threads --reload --debugger
```

## 📊 Acceso a Superset

Una vez instalado, accede a:
- **URL**: http://localhost:8088
- **Usuario**: admin (o el que configuraste)
- **Password**: admin (o el que configuraste)

## 🔧 Configuración DIBIE

El archivo de configuración está en: `config/superset_config.py`

### Configuraciones clave:

```python
# Base de datos (SQLite por defecto)
SQLALCHEMY_DATABASE_URI = 'sqlite:///c:/aguila/dibie/data/superset.db'

# Puerto del servidor
SUPERSET_WEBSERVER_PORT = 8088

# Idioma
BABEL_DEFAULT_LOCALE = 'es'

# Carpetas de datos DIBIE
DIBIE_DATA_DIR = 'c:/aguila/dibie/data'
DIBIE_GOOGLE_DRIVE = 'c:/aguila/dibie/data/google_drive'
```

## 📈 Crear un Dashboard con datos de Google Drive

### 1. Conectar fuente de datos

En Superset:
1. Ir a **Data** → **Databases**
2. Click en **+ Database**
3. Seleccionar tipo de base de datos o usar CSV/Excel

### 2. Subir CSV desde Google Drive

```python
import pandas as pd
from dashboard.superset_manager import SupersetManager

# Cargar datos desde Google Drive
df = pd.read_csv('data/google_drive/tu_archivo.csv')

# Guardar en formato compatible con Superset
df.to_parquet('data/processed/superset_data.parquet')
```

### 3. Crear Dataset

1. En Superset: **Data** → **Datasets**
2. Click **+ Dataset**
3. Seleccionar la tabla/archivo cargado
4. Configurar columnas y tipos de datos

### 4. Crear Chart

1. Ir a **Charts** → **+ Chart**
2. Seleccionar dataset
3. Elegir tipo de visualización:
   - Time Series (líneas)
   - Bar Chart (barras)
   - Pie Chart (torta)
   - Table (tabla)
   - Big Number (KPI)
   - Etc.

### 5. Crear Dashboard

1. Ir a **Dashboards** → **+ Dashboard**
2. Arrastrar charts creados
3. Configurar filtros y layout
4. Guardar y publicar

## 🔄 Sincronización con Google Drive

Para mantener los datos actualizados:

```python
# Script de sincronización automática
from ingestion.google_drive_connector import GoogleDriveConnector
from ingestion.table_loader import TableLoader

connector = GoogleDriveConnector()
loader = TableLoader()

# Listar archivos CSV en Google Drive
files = connector.list_files(pattern="*.csv")

for file in files:
    # Cargar y procesar
    df = loader.load_table(file)
    
    # Guardar para Superset
    output_name = Path(file).stem
    loader.save_to_cache(df, output_name, format='parquet')
    print(f"Procesado: {output_name}")
```

## 🎨 Personalización de Dashboards

### Temas
Editar `config/superset_config.py`:

```python
# Custom theme colors
THEME_OVERRIDES = {
    'colors': {
        'primary': {'base': '#667eea'},
        'secondary': {'base': '#764ba2'},
    }
}
```

### Filtros Nativos

Habilitar en `FEATURE_FLAGS`:
```python
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
}
```

## 🔐 Seguridad

### Cambiar Secret Key

En producción, cambiar en `config/superset_config.py`:

```python
SECRET_KEY = 'your-very-secure-secret-key-here'
```

### Base de datos en producción

Para producción, usar PostgreSQL:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/superset'
```

## 📝 Comandos Útiles

```bash
# Ver versión
superset version

# Listar usuarios
superset fab list-users

# Crear backup de base de datos
copy data\superset.db data\superset_backup.db

# Reiniciar servidor
# Presionar Ctrl+C y volver a ejecutar:
superset run -p 8088 --with-threads --reload
```

## 🐛 Troubleshooting

### Error: "superset: command not found"
```bash
# Asegurarse de que está instalado
pip install apache-superset

# Verificar PATH
where superset
```

### Error de base de datos
```bash
# Eliminar y recrear base de datos
del data\superset.db
superset db upgrade
superset fab create-admin
superset init
```

### Puerto 8088 en uso
```bash
# Cambiar puerto en config/superset_config.py
SUPERSET_WEBSERVER_PORT = 8089

# O especificar al ejecutar
superset run -p 8089
```

## 📚 Recursos

- [Documentación Oficial de Superset](https://superset.apache.org/docs/intro)
- [Galería de Visualizaciones](https://superset.apache.org/docs/creating-charts-dashboards/exploring-data)
- [API de Superset](https://superset.apache.org/docs/api)

## 🤝 Integración con DIBIE

Usar el orquestador principal:

```python
from dibie_main import DIBIEOrchestrator

# Inicializar DIBIE
dibie = DIBIEOrchestrator()

# Procesar datos y preparar para Superset
results = dibie.process_data_pipeline(file_pattern="*.csv")

# Los datos procesados estarán en data/processed/
# Listos para importar en Superset
```
