"""
DIBIE - Table Data Loader
Load and process tabular data from various formats
"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging


class TableLoader:
    """Load tabular data from various file formats"""
    
    SUPPORTED_FORMATS = {
        '.csv': 'csv',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.json': 'json',
        '.parquet': 'parquet',
        '.txt': 'text'
    }
    
    def __init__(self, cache_dir: str = "data/cache"):
        """Initialize table loader
        
        Args:
            cache_dir: Directory for caching processed data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the table loader"""
        logger = logging.getLogger('TableLoader')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/table_loader.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_table(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Load table from file
        
        Args:
            file_path: Path to the file
            **kwargs: Additional parameters for pandas readers
            
        Returns:
            DataFrame with the loaded data
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {extension}")
        
        self.logger.info(f"Loading table from: {file_path}")
        
        try:
            if extension == '.csv':
                df = pd.read_csv(file_path, **kwargs)
            elif extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, **kwargs)
            elif extension == '.json':
                df = pd.read_json(file_path, **kwargs)
            elif extension == '.parquet':
                df = pd.read_parquet(file_path, **kwargs)
            elif extension == '.txt':
                # Assume tab-separated
                df = pd.read_csv(file_path, sep='\t', **kwargs)
            
            self.logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading table: {str(e)}")
            raise
    
    def get_table_info(self, df: pd.DataFrame) -> Dict:
        """Get information about a DataFrame
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with table information
        """
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
        }
    
    def save_to_cache(self, df: pd.DataFrame, name: str, format: str = 'parquet') -> str:
        """Save DataFrame to cache
        
        Args:
            df: DataFrame to save
            name: Name for the cached file
            format: Format to save (parquet, csv, json)
            
        Returns:
            Path to cached file
        """
        cache_path = self.cache_dir / f"{name}.{format}"
        
        if format == 'parquet':
            df.to_parquet(cache_path, index=False)
        elif format == 'csv':
            df.to_csv(cache_path, index=False)
        elif format == 'json':
            df.to_json(cache_path, orient='records')
        
        self.logger.info(f"Saved to cache: {cache_path}")
        return str(cache_path)
    
    def load_from_cache(self, name: str, format: str = 'parquet') -> pd.DataFrame:
        """Load DataFrame from cache
        
        Args:
            name: Name of the cached file
            format: Format of the cached file
            
        Returns:
            Loaded DataFrame
        """
        cache_path = self.cache_dir / f"{name}.{format}"
        
        if not cache_path.exists():
            raise FileNotFoundError(f"Cache file not found: {cache_path}")
        
        return self.load_table(str(cache_path))


if __name__ == "__main__":
    # Example usage
    loader = TableLoader()
    print(f"Supported formats: {list(loader.SUPPORTED_FORMATS.keys())}")
