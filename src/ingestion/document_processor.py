"""
DIBIE - Document Processor
Process documents from Google Drive (Google Docs, PDFs, etc.)
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging


class DocumentProcessor:
    """Process various document types from Google Drive"""
    
    SUPPORTED_TYPES = {
        '.txt': 'text',
        '.pdf': 'pdf',
        '.docx': 'word',
        '.doc': 'word',
        '.gdoc': 'google_doc'
    }
    
    def __init__(self, output_dir: str = "data/documents"):
        """Initialize document processor
        
        Args:
            output_dir: Directory for processed documents
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the document processor"""
        logger = logging.getLogger('DocumentProcessor')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/document_processor.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def process_text_file(self, file_path: str, encoding: str = 'utf-8') -> Dict:
        """Process a text file
        
        Args:
            file_path: Path to the text file
            encoding: File encoding
            
        Returns:
            Dictionary with processed content
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.logger.info(f"Processing text file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return {
                "file_name": path.name,
                "file_path": str(path),
                "type": "text",
                "content": content,
                "word_count": len(content.split()),
                "char_count": len(content),
                "line_count": len(content.splitlines())
            }
        except Exception as e:
            self.logger.error(f"Error processing text file: {str(e)}")
            raise
    
    def extract_metadata(self, file_path: str) -> Dict:
        """Extract metadata from a document
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dictionary with metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "path": str(path),
            "extension": path.suffix,
            "size_bytes": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime
        }
    
    def save_processed_document(self, data: Dict, name: str) -> str:
        """Save processed document data
        
        Args:
            data: Processed document data
            name: Name for the output file
            
        Returns:
            Path to saved file
        """
        output_path = self.output_dir / f"{name}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved processed document: {output_path}")
        return str(output_path)
    
    def list_documents(self, directory: str, extensions: Optional[List[str]] = None) -> List[str]:
        """List documents in a directory
        
        Args:
            directory: Directory to search
            extensions: List of file extensions to filter (e.g., ['.txt', '.pdf'])
            
        Returns:
            List of document paths
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        documents = []
        
        for ext in (extensions or self.SUPPORTED_TYPES.keys()):
            documents.extend(dir_path.rglob(f"*{ext}"))
        
        return [str(d) for d in documents if d.is_file()]


if __name__ == "__main__":
    # Example usage
    processor = DocumentProcessor()
    print(f"Supported document types: {list(processor.SUPPORTED_TYPES.keys())}")
