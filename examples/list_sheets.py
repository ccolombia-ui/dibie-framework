"""
DIBIE - Listar hojas disponibles en Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path


spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
credentials_path = Path("config/credentials_google.json")

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(
    str(credentials_path),
    scopes=scopes
)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(spreadsheet_id)

print(f"Spreadsheet: {spreadsheet.title}")
print(f"\nHojas disponibles:")
for i, worksheet in enumerate(spreadsheet.worksheets(), 1):
    print(f"{i}. {worksheet.title} (GID: {worksheet.id})")
