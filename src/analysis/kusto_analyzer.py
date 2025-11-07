"""
DIBIE - Kusto Data Analyzer
Analyze data using Microsoft Fabric Kusto (KQL)
"""
import json
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime


class KustoAnalyzer:
    """Analyze data using Kusto Query Language (KQL)"""
    
    def __init__(self, cluster_uri: str = "", database: str = "", config_path: str = "config/analysis.json"):
        """Initialize Kusto analyzer
        
        Args:
            cluster_uri: Kusto cluster URI
            database: Database name
            config_path: Path to analysis configuration
        """
        self.cluster_uri = cluster_uri
        self.database = database
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        
        # Load from config if not provided
        if not self.cluster_uri:
            self.cluster_uri = self.config.get("kusto", {}).get("cluster_uri", "")
        if not self.database:
            self.database = self.config.get("kusto", {}).get("database", "")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the analyzer"""
        logger = logging.getLogger('KustoAnalyzer')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/kusto_analyzer.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_analysis_query(self, table_name: str, analysis_type: str) -> str:
        """Create KQL query for different analysis types
        
        Args:
            table_name: Name of the table to analyze
            analysis_type: Type of analysis (descriptive_statistics, time_series, etc.)
            
        Returns:
            KQL query string
        """
        queries = {
            "descriptive_statistics": f"""
                {table_name}
                | summarize 
                    count(),
                    dcount(*),
                    percentiles(*, 25, 50, 75, 95)
            """,
            "time_series": f"""
                {table_name}
                | where isnotempty(timestamp)
                | summarize count() by bin(timestamp, 1h)
                | render timechart
            """,
            "correlation_analysis": f"""
                {table_name}
                | project-away timestamp
                | evaluate python(typeof(*), ```
                    import pandas as pd
                    result = df.corr()
                ```)
            """,
            "data_quality": f"""
                {table_name}
                | summarize 
                    total_rows = count(),
                    null_counts = countif(isnull(*)),
                    completeness = (1.0 - todouble(countif(isnull(*))) / count()) * 100
            """
        }
        
        query = queries.get(analysis_type, f"{table_name} | take 100")
        self.logger.info(f"Created {analysis_type} query for {table_name}")
        return query
    
    def prepare_data_for_ingestion(self, data: List[Dict]) -> str:
        """Prepare data for Kusto ingestion
        
        Args:
            data: List of dictionaries representing rows
            
        Returns:
            CSV formatted string for inline ingestion
        """
        if not data:
            return ""
        
        # Get column names from first row
        columns = list(data[0].keys())
        
        # Create CSV
        lines = [",".join(columns)]
        for row in data:
            values = [str(row.get(col, "")) for col in columns]
            lines.append(",".join(values))
        
        return "\n".join(lines)
    
    def get_query_template(self, template_name: str) -> str:
        """Get predefined query templates
        
        Args:
            template_name: Name of the template
            
        Returns:
            Query template string
        """
        templates = {
            "top_records": "{table_name} | top 100 by {column} desc",
            "group_by": "{table_name} | summarize count() by {column}",
            "filter": "{table_name} | where {column} {operator} {value}",
            "join": "{table1} | join kind=inner ({table2}) on {key}",
            "aggregate": "{table_name} | summarize {agg_function}({column}) by {group_column}"
        }
        
        return templates.get(template_name, "{table_name} | take 100")
    
    def create_table_schema(self, table_name: str, columns: Dict[str, str]) -> str:
        """Create KQL command for creating a table
        
        Args:
            table_name: Name of the table
            columns: Dictionary of column names and types
            
        Returns:
            KQL create table command
        """
        column_defs = [f"{name}:{dtype}" for name, dtype in columns.items()]
        schema = f".create table {table_name} ({', '.join(column_defs)})"
        
        self.logger.info(f"Created schema for table: {table_name}")
        return schema
    
    def generate_analysis_report(self, results: List[Dict], analysis_type: str) -> Dict:
        """Generate analysis report from query results
        
        Args:
            results: Query results
            analysis_type: Type of analysis performed
            
        Returns:
            Analysis report dictionary
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "record_count": len(results),
            "results": results,
            "summary": {
                "status": "completed",
                "data_points": len(results)
            }
        }
        
        return report


if __name__ == "__main__":
    # Example usage
    analyzer = KustoAnalyzer()
    print(f"Kusto Analyzer initialized")
    print(f"Sample query: {analyzer.create_analysis_query('MyTable', 'descriptive_statistics')}")
