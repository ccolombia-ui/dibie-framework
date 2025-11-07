"""
DIBIE - EventStream Manager
Manage Microsoft Fabric EventStreams for real-time data processing
"""
import json
from typing import Dict, List, Optional
import logging
from datetime import datetime


class EventStreamManager:
    """Manage EventStreams for real-time data ingestion and processing"""
    
    def __init__(self, workspace_id: str = "", config_path: str = "config/analysis.json"):
        """Initialize EventStream manager
        
        Args:
            workspace_id: Microsoft Fabric workspace ID
            config_path: Path to analysis configuration
        """
        self.workspace_id = workspace_id
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        
        # Load from config if not provided
        if not self.workspace_id:
            self.workspace_id = self.config.get("eventstream", {}).get("workspace_id", "")
        
        self.eventstream_name = self.config.get("eventstream", {}).get("eventstream_name", "dibie_data_stream")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the manager"""
        logger = logging.Logger('EventStreamManager')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/eventstream_manager.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_eventstream_definition(self, name: str, description: str = "") -> Dict:
        """Create EventStream definition
        
        Args:
            name: Name of the EventStream
            description: Description of the EventStream
            
        Returns:
            EventStream definition dictionary
        """
        definition = {
            "name": name,
            "description": description or f"DIBIE EventStream for {name}",
            "properties": {
                "dataFormat": "json",
                "compression": "none",
                "batchSize": self.config.get("processing", {}).get("batch_size", 1000)
            },
            "sources": [],
            "destinations": [],
            "transformations": []
        }
        
        self.logger.info(f"Created EventStream definition: {name}")
        return definition
    
    def add_source(self, definition: Dict, source_type: str, source_config: Dict) -> Dict:
        """Add a source to the EventStream
        
        Args:
            definition: EventStream definition
            source_type: Type of source (e.g., 'custom', 'azure_blob', 'event_hub')
            source_config: Source configuration
            
        Returns:
            Updated EventStream definition
        """
        source = {
            "type": source_type,
            "config": source_config,
            "timestamp": datetime.now().isoformat()
        }
        
        if "sources" not in definition:
            definition["sources"] = []
        
        definition["sources"].append(source)
        self.logger.info(f"Added {source_type} source to EventStream")
        
        return definition
    
    def add_destination(self, definition: Dict, dest_type: str, dest_config: Dict) -> Dict:
        """Add a destination to the EventStream
        
        Args:
            definition: EventStream definition
            dest_type: Type of destination (e.g., 'kusto', 'lakehouse', 'kql_database')
            dest_config: Destination configuration
            
        Returns:
            Updated EventStream definition
        """
        destination = {
            "type": dest_type,
            "config": dest_config,
            "timestamp": datetime.now().isoformat()
        }
        
        if "destinations" not in definition:
            definition["destinations"] = []
        
        definition["destinations"].append(destination)
        self.logger.info(f"Added {dest_type} destination to EventStream")
        
        return definition
    
    def add_transformation(self, definition: Dict, transform_name: str, transform_query: str) -> Dict:
        """Add a transformation to the EventStream
        
        Args:
            definition: EventStream definition
            transform_name: Name of the transformation
            transform_query: Transformation query (KQL or other)
            
        Returns:
            Updated EventStream definition
        """
        transformation = {
            "name": transform_name,
            "query": transform_query,
            "timestamp": datetime.now().isoformat()
        }
        
        if "transformations" not in definition:
            definition["transformations"] = []
        
        definition["transformations"].append(transformation)
        self.logger.info(f"Added transformation: {transform_name}")
        
        return definition
    
    def create_data_pipeline_config(self, source_path: str, destination_table: str) -> Dict:
        """Create a complete data pipeline configuration
        
        Args:
            source_path: Path to source data
            destination_table: Destination table name
            
        Returns:
            Pipeline configuration
        """
        pipeline = {
            "name": f"pipeline_{destination_table}",
            "source": {
                "type": "file_system",
                "path": source_path,
                "watch": True
            },
            "processing": {
                "batch_size": self.config.get("processing", {}).get("batch_size", 1000),
                "parallel_workers": self.config.get("processing", {}).get("parallel_workers", 4)
            },
            "destination": {
                "type": "kusto",
                "table": destination_table,
                "mapping": "auto"
            },
            "schedule": {
                "type": "continuous",
                "interval_seconds": 60
            }
        }
        
        self.logger.info(f"Created pipeline config: {source_path} -> {destination_table}")
        return pipeline
    
    def save_definition(self, definition: Dict, output_path: str) -> str:
        """Save EventStream definition to file
        
        Args:
            definition: EventStream definition
            output_path: Output file path
            
        Returns:
            Path to saved file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(definition, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved EventStream definition: {output_path}")
        return output_path


if __name__ == "__main__":
    # Example usage
    manager = EventStreamManager()
    definition = manager.create_eventstream_definition("test_stream")
    print(json.dumps(definition, indent=2))
