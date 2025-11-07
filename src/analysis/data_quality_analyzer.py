"""
DIBIE - Data Quality Analyzer
Analyze data quality and generate quality reports
"""
import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime


class DataQualityAnalyzer:
    """Analyze data quality metrics"""
    
    def __init__(self):
        """Initialize data quality analyzer"""
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the analyzer"""
        logger = logging.getLogger('DataQualityAnalyzer')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/data_quality.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def analyze_completeness(self, df: pd.DataFrame) -> Dict:
        """Analyze data completeness
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with completeness metrics
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness_pct = ((total_cells - missing_cells) / total_cells) * 100
        
        column_completeness = {}
        for col in df.columns:
            missing = df[col].isnull().sum()
            total = len(df)
            column_completeness[col] = {
                "missing_count": int(missing),
                "completeness_pct": float(((total - missing) / total) * 100)
            }
        
        return {
            "overall_completeness_pct": float(completeness_pct),
            "total_cells": int(total_cells),
            "missing_cells": int(missing_cells),
            "column_completeness": column_completeness
        }
    
    def analyze_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict:
        """Analyze duplicate records
        
        Args:
            df: DataFrame to analyze
            subset: Columns to check for duplicates
            
        Returns:
            Dictionary with duplicate metrics
        """
        duplicate_count = df.duplicated(subset=subset).sum()
        duplicate_pct = (duplicate_count / len(df)) * 100
        
        return {
            "duplicate_count": int(duplicate_count),
            "duplicate_pct": float(duplicate_pct),
            "unique_count": int(len(df) - duplicate_count),
            "total_records": int(len(df))
        }
    
    def analyze_data_types(self, df: pd.DataFrame) -> Dict:
        """Analyze data types and potential issues
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with data type analysis
        """
        type_analysis = {}
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            unique_count = df[col].nunique()
            
            type_analysis[col] = {
                "dtype": dtype,
                "unique_values": int(unique_count),
                "sample_values": df[col].dropna().head(5).tolist()
            }
        
        return type_analysis
    
    def calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate overall data quality score
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Quality score (0-100)
        """
        completeness = self.analyze_completeness(df)
        duplicates = self.analyze_duplicates(df)
        
        # Weighted scoring
        completeness_score = completeness["overall_completeness_pct"] * 0.6
        uniqueness_score = (100 - duplicates["duplicate_pct"]) * 0.4
        
        quality_score = completeness_score + uniqueness_score
        
        self.logger.info(f"Calculated quality score: {quality_score:.2f}")
        return round(quality_score, 2)
    
    def generate_quality_report(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """Generate comprehensive quality report
        
        Args:
            df: DataFrame to analyze
            dataset_name: Name of the dataset
            
        Returns:
            Complete quality report
        """
        self.logger.info(f"Generating quality report for: {dataset_name}")
        
        report = {
            "dataset_name": dataset_name,
            "timestamp": datetime.now().isoformat(),
            "record_count": len(df),
            "column_count": len(df.columns),
            "quality_score": self.calculate_quality_score(df),
            "completeness": self.analyze_completeness(df),
            "duplicates": self.analyze_duplicates(df),
            "data_types": self.analyze_data_types(df),
            "recommendations": self._generate_recommendations(df)
        }
        
        return report
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate recommendations based on data quality issues
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for high missing values
        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            if missing_pct > 20:
                recommendations.append(f"Column '{col}' has {missing_pct:.1f}% missing values - consider imputation or removal")
        
        # Check for duplicates
        duplicate_pct = (df.duplicated().sum() / len(df)) * 100
        if duplicate_pct > 5:
            recommendations.append(f"Dataset contains {duplicate_pct:.1f}% duplicates - consider deduplication")
        
        # Check for low cardinality
        for col in df.columns:
            unique_pct = (df[col].nunique() / len(df)) * 100
            if unique_pct < 1 and len(df) > 100:
                recommendations.append(f"Column '{col}' has very low cardinality - may not be useful for analysis")
        
        return recommendations


if __name__ == "__main__":
    # Example usage
    analyzer = DataQualityAnalyzer()
    print("Data Quality Analyzer initialized")
