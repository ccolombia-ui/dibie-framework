"""
Example: Kusto Integration
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analysis.kusto_analyzer import KustoAnalyzer

def main():
    # Initialize Kusto analyzer
    analyzer = KustoAnalyzer()
    
    print("DIBIE - Kusto Integration Example")
    print("=" * 60)
    
    # Example: Create analysis queries
    table_name = "EducationData"
    
    print(f"\nGenerated queries for table: {table_name}\n")
    
    # Descriptive statistics
    query1 = analyzer.create_analysis_query(table_name, "descriptive_statistics")
    print("1. Descriptive Statistics:")
    print(query1)
    
    # Time series
    query2 = analyzer.create_analysis_query(table_name, "time_series")
    print("\n2. Time Series Analysis:")
    print(query2)
    
    # Data quality
    query3 = analyzer.create_analysis_query(table_name, "data_quality")
    print("\n3. Data Quality Check:")
    print(query3)
    
    # Create table schema
    columns = {
        "id": "int",
        "nombre": "string",
        "edad": "int",
        "fecha": "datetime",
        "calificacion": "real"
    }
    
    schema_command = analyzer.create_table_schema(table_name, columns)
    print("\n4. Create Table Command:")
    print(schema_command)
    
    print("\n" + "=" * 60)
    print("Note: To execute these queries, configure Kusto connection in config/analysis.json")

if __name__ == "__main__":
    main()
