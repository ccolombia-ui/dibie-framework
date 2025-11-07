"""
DIBIE - Main Orchestrator
Main entry point for the DIBIE framework
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.google_drive_connector import GoogleDriveConnector
from ingestion.table_loader import TableLoader
from ingestion.document_processor import DocumentProcessor
from analysis.kusto_analyzer import KustoAnalyzer
from analysis.eventstream_manager import EventStreamManager
from analysis.data_quality_analyzer import DataQualityAnalyzer
from dashboard.dashboard_generator import DashboardGenerator


class DIBIEOrchestrator:
    """Main orchestrator for DIBIE framework"""
    
    def __init__(self):
        """Initialize DIBIE orchestrator"""
        self.logger = self._setup_logger()
        self.initialize_components()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup main logger"""
        logger = logging.getLogger('DIBIE')
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('logs/dibie_main.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def initialize_components(self):
        """Initialize all DIBIE components"""
        self.logger.info("Initializing DIBIE components...")
        
        try:
            self.drive_connector = GoogleDriveConnector()
            self.table_loader = TableLoader()
            self.document_processor = DocumentProcessor()
            self.kusto_analyzer = KustoAnalyzer()
            self.eventstream_manager = EventStreamManager()
            self.quality_analyzer = DataQualityAnalyzer()
            self.dashboard_generator = DashboardGenerator()
            
            self.logger.info("All components initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing components: {str(e)}")
            raise
    
    def process_data_pipeline(self, file_pattern: str = "*.csv") -> Dict:
        """Run complete data pipeline
        
        Args:
            file_pattern: Pattern for files to process
            
        Returns:
            Pipeline results
        """
        self.logger.info(f"Starting data pipeline for pattern: {file_pattern}")
        
        results = {
            "files_processed": 0,
            "tables_loaded": [],
            "quality_reports": [],
            "dashboard_path": None,
            "status": "started"
        }
        
        try:
            # 1. Check Google Drive access
            if not self.drive_connector.is_drive_accessible():
                self.logger.warning("Google Drive not accessible, using local data directory")
                data_dir = "data/tables"
            else:
                data_dir = self.drive_connector.get_drive_path()
            
            # 2. List files
            files = self.drive_connector.list_files(pattern=file_pattern)
            self.logger.info(f"Found {len(files)} files matching pattern")
            
            # 3. Process each file
            for file_path in files[:5]:  # Limit to 5 files for demo
                try:
                    # Load table
                    df = self.table_loader.load_table(file_path)
                    table_info = self.table_loader.get_table_info(df)
                    
                    # Analyze quality
                    quality_report = self.quality_analyzer.generate_quality_report(
                        df, 
                        Path(file_path).stem
                    )
                    
                    results["tables_loaded"].append({
                        "file": file_path,
                        "info": table_info
                    })
                    results["quality_reports"].append(quality_report)
                    results["files_processed"] += 1
                    
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {str(e)}")
            
            # 4. Generate dashboard
            if results["quality_reports"]:
                dashboard = self.dashboard_generator.create_dashboard(
                    "DIBIE Data Analysis Dashboard",
                    []
                )
                
                # Add quality metrics from first report
                dashboard = self.dashboard_generator.add_quality_metrics(
                    dashboard,
                    results["quality_reports"][0]
                )
                
                # Save dashboard
                results["dashboard_path"] = self.dashboard_generator.save_dashboard(
                    dashboard,
                    f"dashboard_{Path(files[0]).stem}",
                    format='html'
                )
            
            results["status"] = "completed"
            self.logger.info("Data pipeline completed successfully")
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            self.logger.error(f"Pipeline failed: {str(e)}")
        
        return results
    
    def generate_summary_dashboard(self) -> str:
        """Generate a summary dashboard of all processed data
        
        Returns:
            Path to generated dashboard
        """
        self.logger.info("Generating summary dashboard...")
        
        dashboard = self.dashboard_generator.create_dashboard(
            "DIBIE - Overview Dashboard",
            [
                self.dashboard_generator.create_kpi_card(
                    "Framework Status",
                    "Active",
                    "",
                    "up"
                ),
                self.dashboard_generator.create_kpi_card(
                    "Data Sources",
                    "Google Drive Connected",
                    ""
                )
            ]
        )
        
        output_path = self.dashboard_generator.save_dashboard(
            dashboard,
            "overview_dashboard",
            format='html'
        )
        
        self.logger.info(f"Summary dashboard generated: {output_path}")
        return output_path
    
    def get_system_status(self) -> Dict:
        """Get status of all DIBIE components
        
        Returns:
            System status dictionary
        """
        return {
            "google_drive_accessible": self.drive_connector.is_drive_accessible(),
            "google_drive_path": self.drive_connector.get_drive_path(),
            "components": {
                "drive_connector": "active",
                "table_loader": "active",
                "document_processor": "active",
                "kusto_analyzer": "configured",
                "eventstream_manager": "configured",
                "quality_analyzer": "active",
                "dashboard_generator": "active"
            },
            "framework_version": "1.0.0"
        }


def main():
    """Main entry point"""
    print("=" * 60)
    print("DIBIE - Data Intelligence Business Intelligence Engine")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = DIBIEOrchestrator()
    
    # Get system status
    status = orchestrator.get_system_status()
    print(f"\nGoogle Drive Accessible: {status['google_drive_accessible']}")
    print(f"Google Drive Path: {status['google_drive_path']}")
    
    # Generate overview dashboard
    print("\nGenerating overview dashboard...")
    dashboard_path = orchestrator.generate_summary_dashboard()
    print(f"Dashboard generated: {dashboard_path}")
    
    print("\n" + "=" * 60)
    print("DIBIE initialized successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
