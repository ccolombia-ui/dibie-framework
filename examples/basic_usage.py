"""
Example: Basic Usage of DIBIE Framework
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from dibie_main import DIBIEOrchestrator

def main():
    # Initialize DIBIE
    dibie = DIBIEOrchestrator()
    
    # Get system status
    status = dibie.get_system_status()
    print("System Status:")
    print(f"  Google Drive: {status['google_drive_accessible']}")
    print(f"  Path: {status['google_drive_path']}")
    print(f"  Version: {status['framework_version']}")
    
    # Generate overview dashboard
    dashboard_path = dibie.generate_summary_dashboard()
    print(f"\nDashboard created: {dashboard_path}")

if __name__ == "__main__":
    main()
