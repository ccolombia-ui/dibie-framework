"""
DIBIE - Análisis de Columnas de Matrícula
Identificar y extraer todas las columnas relacionadas con matrícula por grado
"""
import pandas as pd
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials


def analyze_matricula_columns():
    """
    Analizar columnas de matrícula en la tabla original
    """
    print("=" * 70)
    print("DIBIE - Análisis de Columnas de Matrícula")
    print("=" * 70)
    
    # 1. Configurar autenticación
    credentials_path = Path("config/credentials_google.json")
    
    if not credentials_path.exists():
        print("✗ No se encontró config/credentials_google.json")
        return
    
    # 2. Autenticar con Google Sheets
    print("\n1. Autenticando con Google Sheets...")
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=scopes
    )
    client = gspread.authorize(creds)
    
    # 3. Leer datos
    print("\n2. Leyendo datos de Google Sheets...")
    spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
    sheet_name = "maestro"  # Hoja principal
    
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    
    # Obtener datos como DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    print(f"   ✓ {len(df)} filas, {len(df.columns)} columnas")
    
    # 3. Identificar columnas de matrícula
    print("\n2. Identificando columnas de matrícula...")
    
    # Buscar patrones comunes
    matricula_patterns = [
        'matricula', 'matrícula', 'MATRICULA', 'MATRÍCULA',
        'grado', 'GRADO', 'Grado',
        'transicion', 'transición', 'TRANSICION',
        'primero', 'segundo', 'tercero', 'cuarto', 'quinto',
        'sexto', 'septimo', 'octavo', 'noveno', 'decimo', 'once'
    ]
    
    matricula_cols = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(pattern.lower() in col_lower for pattern in matricula_patterns):
            matricula_cols.append(col)
    
    print(f"   ✓ {len(matricula_cols)} columnas relacionadas con matrícula encontradas")
    
    # 4. Mostrar columnas
    print("\n3. Columnas de matrícula identificadas:")
    for i, col in enumerate(matricula_cols, 1):
        # Obtener algunos valores de muestra
        sample_values = df[col].dropna().head(3).tolist()
        print(f"\n   {i}. {col}")
        print(f"      Tipo: {df[col].dtype}")
        print(f"      No nulos: {df[col].notna().sum()}/{len(df)}")
        if sample_values:
            print(f"      Muestra: {sample_values}")
    
    # 5. Análisis de grados
    print("\n4. Identificando estructura de grados...")
    
    grados_identificados = []
    for col in matricula_cols:
        col_lower = str(col).lower()
        
        # Detectar grado
        if 'transicion' in col_lower or 'transición' in col_lower or 'jardin' in col_lower:
            grado = 'Transición'
        elif 'primero' in col_lower or '1°' in col_lower or 'grado 1' in col_lower:
            grado = '1°'
        elif 'segundo' in col_lower or '2°' in col_lower or 'grado 2' in col_lower:
            grado = '2°'
        elif 'tercero' in col_lower or '3°' in col_lower or 'grado 3' in col_lower:
            grado = '3°'
        elif 'cuarto' in col_lower or '4°' in col_lower or 'grado 4' in col_lower:
            grado = '4°'
        elif 'quinto' in col_lower or '5°' in col_lower or 'grado 5' in col_lower:
            grado = '5°'
        elif 'sexto' in col_lower or '6°' in col_lower or 'grado 6' in col_lower:
            grado = '6°'
        elif 'septimo' in col_lower or 'séptimo' in col_lower or '7°' in col_lower or 'grado 7' in col_lower:
            grado = '7°'
        elif 'octavo' in col_lower or '8°' in col_lower or 'grado 8' in col_lower:
            grado = '8°'
        elif 'noveno' in col_lower or '9°' in col_lower or 'grado 9' in col_lower:
            grado = '9°'
        elif 'decimo' in col_lower or 'décimo' in col_lower or '10°' in col_lower or 'grado 10' in col_lower:
            grado = '10°'
        elif 'once' in col_lower or '11°' in col_lower or 'grado 11' in col_lower:
            grado = '11°'
        else:
            grado = 'Otro'
        
        grados_identificados.append({
            'columna': col,
            'grado': grado,
            'valores_no_nulos': df[col].notna().sum()
        })
    
    # Mostrar resumen por grado
    print("\n   Resumen por grado:")
    grados_df = pd.DataFrame(grados_identificados)
    
    if len(grados_df) > 0:
        resumen = grados_df.groupby('grado').agg({
            'columna': 'count',
            'valores_no_nulos': 'sum'
        }).reset_index()
        resumen.columns = ['Grado', 'Columnas', 'Total Valores']
        
        print(f"\n{resumen.to_string(index=False)}")
    
    # 6. Guardar análisis
    print("\n5. Guardando análisis...")
    
    analysis_dir = Path("data/analysis")
    analysis_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar lista de columnas
    grados_df.to_csv(analysis_dir / "matricula_columns.csv", index=False, encoding='utf-8')
    print(f"   ✓ Guardado en: data/analysis/matricula_columns.csv")
    
    # 7. Crear estructura recomendada
    print("\n6. Estructura recomendada para tabla paramétrica:")
    print("\n   tabla: hechos_matricula")
    print("   ├── dane_institucion (FK)")
    print("   ├── anio")
    print("   ├── grado_codigo (Transición, 1°, 2°, ..., 11°)")
    print("   ├── grado_nombre (Transición, Primero, Segundo, ..., Once)")
    print("   ├── nivel_educativo (Preescolar, Primaria, Secundaria, Media)")
    print("   ├── cantidad_estudiantes")
    print("   └── fecha_corte")
    
    print("\n   tabla: dim_grados (paramétrica)")
    print("   ├── grado_codigo (PK)")
    print("   ├── grado_nombre")
    print("   ├── grado_numero (0-11)")
    print("   ├── nivel_educativo")
    print("   ├── orden")
    print("   └── descripcion")
    
    print("\n✅ Análisis completado!")
    print(f"\n📊 Total columnas de matrícula: {len(matricula_cols)}")
    
    return grados_df


if __name__ == "__main__":
    analyze_matricula_columns()
