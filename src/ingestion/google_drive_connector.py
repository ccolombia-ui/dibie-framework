"""
DIBIE - Data Intelligence Business Intelligence Engine
Google Drive Data Connector
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class GoogleDriveConnector:
    """Connector for accessing Google Drive data"""
    
    def __init__(self, config_path: str = "config/paths.json"):
        """Initialize the Google Drive connector
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.google_drive_path = self.config["google_drive"]["local_path"]
        self.drive_url = self.config["google_drive"]["drive_url"]
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_drive_path(self) -> str:
        """Get the local path to Google Drive folder"""
        return self.google_drive_path
    
    def is_drive_accessible(self) -> bool:
        """Check if Google Drive folder is accessible"""
        return os.path.exists(self.google_drive_path)
    
    def list_files(self, pattern: str = "*", recursive: bool = True) -> List[str]:
        """List files in Google Drive folder
        
        Args:
            pattern: File pattern to match (e.g., "*.csv", "*.xlsx")
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        if not self.is_drive_accessible():
            raise FileNotFoundError(f"Google Drive path not accessible: {self.google_drive_path}")
        
        drive_path = Path(self.google_drive_path)
        
        if recursive:
            files = list(drive_path.rglob(pattern))
        else:
            files = list(drive_path.glob(pattern))
        
        return [str(f) for f in files if f.is_file()]
    
    def get_file_info(self, file_path: str) -> Dict:
        """Get information about a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "path": str(path),
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": path.suffix,
            "is_file": path.is_file()
        }
    
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Read text file content
        
        Args:
            file_path: Path to the file
            encoding: File encoding
            
        Returns:
            File content as string
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()


if __name__ == "__main__":
    # Example usage
    connector = GoogleDriveConnector()
    print(f"Google Drive Path: {connector.get_drive_path()}")
    print(f"Drive Accessible: {connector.is_drive_accessible()}")
