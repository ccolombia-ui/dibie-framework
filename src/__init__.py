"""
DIBIE Package Initialization
"""

__version__ = "1.0.0"
__author__ = "DIBIE Team"
__description__ = "Data Intelligence Business Intelligence Engine"

from .ingestion.google_drive_connector import GoogleDriveConnector
from .ingestion.table_loader import TableLoader
from .ingestion.document_processor import DocumentProcessor
from .analysis.kusto_analyzer import KustoAnalyzer
from .analysis.eventstream_manager import EventStreamManager
from .analysis.data_quality_analyzer import DataQualityAnalyzer
from .dashboard.dashboard_generator import DashboardGenerator
from .dibie_main import DIBIEOrchestrator

__all__ = [
    'GoogleDriveConnector',
    'TableLoader',
    'DocumentProcessor',
    'KustoAnalyzer',
    'EventStreamManager',
    'DataQualityAnalyzer',
    'DashboardGenerator',
    'DIBIEOrchestrator'
]
