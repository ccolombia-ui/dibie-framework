"""
DIBIE - Google Sheets Reader
Leer y analizar datos de Google Sheets
"""
import pandas as pd
import json
from typing import Dict, List, Tuple
from pathlib import Path
import re


class GoogleSheetsReader:
    """Leer datos de Google Sheets mediante URL pública"""
    
    def __init__(self):
        """Initialize Google Sheets reader"""
        pass
    
    def extract_sheet_id(self, url: str) -> str:
        """Extract sheet ID from Google Sheets URL
        
        Args:
            url: Google Sheets URL
            
        Returns:
            Sheet ID
        """
        # Extract from URL pattern: /d/{SHEET_ID}/
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if match:
            return match.group(1)
        raise ValueError(f"Could not extract sheet ID from URL: {url}")
    
    def extract_gid(self, url: str) -> str:
        """Extract GID (specific sheet) from URL
        
        Args:
            url: Google Sheets URL
            
        Returns:
            GID or None
        """
        match = re.search(r'gid=(\d+)', url)
        if match:
            return match.group(1)
        return None
    
    def read_sheet(self, url: str, sheet_name: str = None) -> pd.DataFrame:
        """Read Google Sheet as DataFrame
        
        Args:
            url: Google Sheets URL
            sheet_name: Name or index of the sheet to read
            
        Returns:
            DataFrame with sheet data
        """
        try:
            # Try using gspread with service account credentials
            import gspread
            from google.oauth2.service_account import Credentials
            
            try:
                # Use service account credentials
                print("   ⚙ Autenticando con credenciales de servicio...")
                credentials_path = Path("config/credentials_google.json")
                
                if not credentials_path.exists():
                    raise FileNotFoundError("config/credentials_google.json no encontrado")
                
                # Define scopes
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets.readonly',
                    'https://www.googleapis.com/auth/drive.readonly'
                ]
                
                # Authenticate
                creds = Credentials.from_service_account_file(
                    str(credentials_path),
                    scopes=scopes
                )
                gc = gspread.authorize(creds)
                
                sheet_id = self.extract_sheet_id(url)
                print(f"   📄 Abriendo spreadsheet: {sheet_id}")
                spreadsheet = gc.open_by_key(sheet_id)
                
                # Get specific worksheet by gid if available
                gid = self.extract_gid(url)
                if gid:
                    print(f"   📊 Buscando hoja con GID: {gid}")
                    # Find worksheet by id
                    worksheet = None
                    for ws in spreadsheet.worksheets():
                        if str(ws.id) == str(gid):
                            worksheet = ws
                            break
                    if not worksheet:
                        print(f"   ⚠ No se encontró GID={gid}, usando primera hoja")
                        worksheet = spreadsheet.get_worksheet(0)
                else:
                    worksheet = spreadsheet.get_worksheet(0)
                
                print(f"   ✓ Hoja seleccionada: {worksheet.title}")
                
                # Get all values and convert to DataFrame
                print("   ⬇ Descargando datos...")
                data = worksheet.get_all_values()
                if data:
                    df = pd.DataFrame(data[1:], columns=data[0])
                    print(f"   ✓ Datos leídos: {df.shape[0]:,} filas, {df.shape[1]} columnas")
                    return df
                else:
                    return pd.DataFrame()
                    
            except Exception as auth_error:
                print(f"   ✗ Error de autenticación: {auth_error}")
                print(f"\n   💡 IMPORTANTE: Comparte la hoja con la cuenta de servicio:")
                print(f"   📧 aksobhya-googlesheet-806@aksobhya.iam.gserviceaccount.com")
                print(f"\n   Pasos:")
                print(f"   1. Abre: https://docs.google.com/spreadsheets/d/{self.extract_sheet_id(url)}")
                print(f"   2. Clic en 'Compartir' (esquina superior derecha)")
                print(f"   3. Agrega el email de la cuenta de servicio")
                print(f"   4. Permiso: 'Lector' (Viewer)")
                print(f"   5. Enviar invitación")
                raise
                
        except ImportError:
            # Fallback to CSV export if gspread not available
            sheet_id = self.extract_sheet_id(url)
            gid = self.extract_gid(url)
            
            if gid:
                export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            else:
                export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            
            df = pd.read_csv(export_url)
            return df
    
    def read_all_sheets(self, url: str) -> Dict[str, pd.DataFrame]:
        """Read all sheets from a Google Sheets document
        
        Args:
            url: Google Sheets URL
            
        Returns:
            Dictionary with sheet names as keys and DataFrames as values
        """
        sheet_id = self.extract_sheet_id(url)
        
        # Try to read the main sheet first
        try:
            main_df = self.read_sheet(url)
            sheets = {"Sheet1": main_df}
        except Exception as e:
            print(f"Error reading main sheet: {e}")
            sheets = {}
        
        return sheets
    
    def analyze_columns(self, df: pd.DataFrame) -> Dict:
        """Analyze DataFrame columns
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with column analysis
        """
        analysis = {}
        
        for col in df.columns:
            col_name = str(col)  # Ensure column name is string
            try:
                series = df[col]
                analysis[col_name] = {
                    "dtype": str(series.dtype),
                    "non_null_count": int(series.notna().sum()),
                    "null_count": int(series.isna().sum()),
                    "null_percentage": float((series.isna().sum() / len(df)) * 100),
                    "unique_values": int(series.nunique()),
                    "sample_values": series.dropna().head(3).tolist()
                }
            except Exception as e:
                analysis[col_name] = {
                    "dtype": "error",
                    "error": str(e),
                    "non_null_count": 0,
                    "null_count": len(df),
                    "null_percentage": 100.0,
                    "unique_values": 0,
                    "sample_values": []
                }
        
        return analysis
    
    def create_data_dictionary(self, df: pd.DataFrame, table_name: str = "tabla") -> Dict:
        """Create a data dictionary for the DataFrame
        
        Args:
            df: DataFrame to document
            table_name: Name of the table
            
        Returns:
            Data dictionary
        """
        column_analysis = self.analyze_columns(df)
        
        data_dict = {
            "table_name": table_name,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": []
        }
        
        for col, stats in column_analysis.items():
            # Infer business meaning from column name
            business_type = self._infer_business_type(col)
            
            col_info = {
                "column_name": col,
                "data_type": stats["dtype"],
                "business_type": business_type,
                "nullable": stats["null_count"] > 0,
                "null_percentage": round(stats["null_percentage"], 2),
                "unique_values": stats["unique_values"],
                "cardinality": self._classify_cardinality(stats["unique_values"], len(df)),
                "sample_values": stats["sample_values"],
                "description": self._generate_description(col, stats)
            }
            
            data_dict["columns"].append(col_info)
        
        return data_dict
    
    def _infer_business_type(self, column_name: str) -> str:
        """Infer business type from column name
        
        Args:
            column_name: Name of the column
            
        Returns:
            Business type classification
        """
        col_lower = column_name.lower()
        
        # ID fields
        if any(x in col_lower for x in ['id', 'codigo', 'dane', 'nit']):
            return "identifier"
        
        # Names
        if any(x in col_lower for x in ['nombre', 'name', 'denominacion']):
            return "name"
        
        # Addresses and locations
        if any(x in col_lower for x in ['direccion', 'address', 'municipio', 'departamento', 'ciudad']):
            return "location"
        
        # Coordinates
        if any(x in col_lower for x in ['latitud', 'longitud', 'lat', 'lon', 'coordenada']):
            return "coordinate"
        
        # Financial
        if any(x in col_lower for x in ['monto', 'valor', 'presupuesto', 'ingresos', 'egresos', 'saldo']):
            return "financial"
        
        # Dates
        if any(x in col_lower for x in ['fecha', 'date', 'año', 'mes', 'vigencia']):
            return "temporal"
        
        # Quantities
        if any(x in col_lower for x in ['cantidad', 'numero', 'total', 'count']):
            return "quantity"
        
        return "other"
    
    def _classify_cardinality(self, unique_count: int, total_rows: int) -> str:
        """Classify cardinality of a column
        
        Args:
            unique_count: Number of unique values
            total_rows: Total number of rows
            
        Returns:
            Cardinality classification
        """
        ratio = unique_count / total_rows if total_rows > 0 else 0
        
        if unique_count == 1:
            return "constant"
        elif unique_count == total_rows:
            return "unique (PK candidate)"
        elif ratio > 0.95:
            return "high (almost unique)"
        elif ratio > 0.5:
            return "high"
        elif ratio > 0.1:
            return "medium"
        else:
            return "low (dimension candidate)"
    
    def _generate_description(self, column_name: str, stats: Dict) -> str:
        """Generate automatic description for column
        
        Args:
            column_name: Name of the column
            stats: Column statistics
            
        Returns:
            Description text
        """
        desc_parts = []
        
        # Add basic info
        desc_parts.append(f"Columna '{column_name}'")
        
        # Add cardinality info
        if stats["unique_values"] == 1:
            desc_parts.append("con valor constante")
        elif stats["unique_values"] < 10:
            desc_parts.append(f"con {stats['unique_values']} valores únicos")
        
        # Add nullable info
        if stats["null_count"] > 0:
            desc_parts.append(f"({stats['null_percentage']:.1f}% nulos)")
        
        return " - ".join(desc_parts)


if __name__ == "__main__":
    # Test
    reader = GoogleSheetsReader()
    url = "https://docs.google.com/spreadsheets/d/1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc/edit?gid=1897725171#gid=1897725171"
    
    print("Leyendo Google Sheet...")
    df = reader.read_sheet(url)
    print(f"Dimensiones: {df.shape}")
    print(f"Columnas: {list(df.columns[:5])}...")
