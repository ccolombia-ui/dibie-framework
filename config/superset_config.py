# Superset configuration file for DIBIE

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Flask App Builder configuration
# Your App secret key
SECRET_KEY = 'YOUR_SECRET_KEY_CHANGE_THIS'

# The SQLAlchemy connection string to your database backend
SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/data/superset.db'

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''

# DIBIE specific configurations
DIBIE_DATA_DIR = BASE_DIR / 'data'
DIBIE_GOOGLE_DRIVE = DIBIE_DATA_DIR / 'google_drive'
DIBIE_PROCESSED_DIR = DIBIE_DATA_DIR / 'processed'

# Enable scheduled queries
SCHEDULED_QUERIES = {
    'ENABLE_SCHEDULED_QUERIES': True,
}

# Superset specific config
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088

# Set the default language
BABEL_DEFAULT_LOCALE = 'es'

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
}

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
}

# Upload folder
UPLOAD_FOLDER = str(BASE_DIR / 'data' / 'uploads')

# Image and file upload
UPLOAD_EXTENSIONS = {'csv', 'xlsx', 'xls', 'parquet', 'json'}
UPLOAD_ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'parquet', 'json'}
