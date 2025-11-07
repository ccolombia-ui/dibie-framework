"""
Example: Load and Analyze Tables from Google Drive
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.google_drive_connector import GoogleDriveConnector
from ingestion.table_loader import TableLoader
from analysis.data_quality_analyzer import DataQualityAnalyzer
from dashboard.dashboard_generator import DashboardGenerator

def main():
    # Initialize components
    drive = GoogleDriveConnector()
    loader = TableLoader()
    quality = DataQualityAnalyzer()
    dashboard_gen = DashboardGenerator()
    
    print("DIBIE - Table Analysis Example")
    print("=" * 60)
    
    # Check Google Drive access
    if drive.is_drive_accessible():
        print(f"✓ Google Drive accessible at: {drive.get_drive_path()}")
        
        # List CSV files
        csv_files = drive.list_files(pattern="*.csv")
        print(f"✓ Found {len(csv_files)} CSV files")
        
        if csv_files:
            # Load first CSV file
            first_file = csv_files[0]
            print(f"\nLoading: {Path(first_file).name}")
            
            df = loader.load_table(first_file)
            table_info = loader.get_table_info(df)
            
            print(f"  Rows: {table_info['rows']}")
            print(f"  Columns: {table_info['columns']}")
            print(f"  Column names: {', '.join(table_info['column_names'][:5])}")
            
            # Analyze quality
            quality_report = quality.generate_quality_report(df, Path(first_file).stem)
            print(f"\n  Quality Score: {quality_report['quality_score']:.1f}/100")
            print(f"  Completeness: {quality_report['completeness']['overall_completeness_pct']:.1f}%")
            
            # Generate dashboard
            dashboard = dashboard_gen.create_dashboard(
                f"Analysis: {Path(first_file).stem}",
                []
            )
            dashboard = dashboard_gen.add_quality_metrics(dashboard, quality_report)
            
            output_path = dashboard_gen.save_dashboard(
                dashboard,
                f"analysis_{Path(first_file).stem}",
                format='html'
            )
            print(f"\n✓ Dashboard saved: {output_path}")
    else:
        print("✗ Google Drive not accessible")
        print(f"  Expected path: {drive.get_drive_path()}")

if __name__ == "__main__":
    main()
