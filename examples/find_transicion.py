"""
Buscar columna de Transición en Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

credentials_path = Path("config/credentials_google.json")
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(str(credentials_path), scopes=scopes)
client = gspread.authorize(creds)

spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
spreadsheet = client.open_by_key(spreadsheet_id)
worksheet = spreadsheet.worksheet("maestro")

data = worksheet.get_all_values()
headers = data[0]

print("Buscando columnas relacionadas con matrícula/grados:\n")

for i, header in enumerate(headers):
    header_lower = str(header).lower()
    if any(keyword in header_lower for keyword in ['transici', 'grado', 'matrícula', 'matricula', 'jardín', 'jardin', 'preescolar']):
        print(f"Columna {i}: '{header}'")
    elif str(header).strip() in ['T', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
        print(f"Columna {i}: '{header}' ← NÚMERO/LETRA")

print("\n\nPrimeras 20 columnas:")
for i, header in enumerate(headers[:20]):
    print(f"{i}: '{header}'")
