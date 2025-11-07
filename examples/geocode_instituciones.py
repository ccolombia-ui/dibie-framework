"""
DIBIE - Geocoding de Instituciones
Obtener coordenadas geográficas (latitud, longitud) usando Nominatim (OpenStreetMap)
"""
import pandas as pd
from pathlib import Path
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import gspread
from google.oauth2.service_account import Credentials


def geocode_address(geolocator, direccion: str, municipio: str, retry=3):
    """
    Geocodificar una dirección
    
    Args:
        geolocator: Objeto Nominatim
        direccion: Dirección de la institución
        municipio: Municipio
        retry: Número de reintentos
        
    Returns:
        Tuple (latitud, longitud) o (None, None)
    """
    # Construir query completa
    query = f"{direccion}, {municipio}, Colombia"
    
    for attempt in range(retry):
        try:
            location = geolocator.geocode(query, timeout=10)
            if location:
                return location.latitude, location.longitude
            else:
                # Intentar solo con municipio
                query_simple = f"{municipio}, Colombia"
                location = geolocator.geocode(query_simple, timeout=10)
                if location:
                    return location.latitude, location.longitude
            return None, None
            
        except GeocoderTimedOut:
            if attempt < retry - 1:
                time.sleep(2)
                continue
            return None, None
        except GeocoderServiceError:
            return None, None
    
    return None, None


def geocode_maestro_instituciones():
    """
    Agregar coordenadas geográficas al maestro de instituciones
    """
    print("=" * 70)
    print("DIBIE - Geocoding de Instituciones")
    print("=" * 70)
    
    # 1. Cargar datos del CSV
    print("\n1. Cargando maestro_instituciones.csv...")
    csv_path = Path("data/processed/maestro_instituciones.csv")
    
    if not csv_path.exists():
        print(f"✗ No se encontró {csv_path}")
        print("   Ejecuta primero: python examples/create_maestro_instituciones.py")
        return
    
    df = pd.read_csv(csv_path)
    print(f"   ✓ {len(df)} instituciones cargadas")
    
    # 2. Inicializar geocoder
    print("\n2. Inicializando geocoder (Nominatim/OpenStreetMap)...")
    geolocator = Nominatim(user_agent="dibie_geocoder_v1.0")
    print("   ✓ Geocoder listo")
    
    # 3. Geocodificar cada institución
    print(f"\n3. Geocodificando {len(df)} instituciones...")
    print("   (Esto puede tomar varios minutos...)")
    
    geocoded_count = 0
    failed_count = 0
    
    for idx, row in df.iterrows():
        direccion = str(row['direccion']).strip()
        municipio = str(row['municipio']).strip()
        
        if not direccion or not municipio or direccion == 'nan' or municipio == 'nan':
            print(f"   {idx + 1}. ⚠ Sin dirección/municipio: {row['nombre'][:40]}")
            df.at[idx, 'latitud'] = ''
            df.at[idx, 'longitud'] = ''
            failed_count += 1
            continue
        
        print(f"   {idx + 1}. Geocodificando: {row['nombre'][:40]}...", end=" ")
        
        lat, lon = geocode_address(geolocator, direccion, municipio)
        
        if lat and lon:
            df.at[idx, 'latitud'] = lat
            df.at[idx, 'longitud'] = lon
            df.at[idx, 'departamento'] = 'Cundinamarca' if municipio.lower() == 'bogota' else ''
            print(f"✓ ({lat:.6f}, {lon:.6f})")
            geocoded_count += 1
        else:
            df.at[idx, 'latitud'] = ''
            df.at[idx, 'longitud'] = ''
            print("✗ No encontrado")
            failed_count += 1
        
        # Respetar límites de tasa de Nominatim (1 req/segundo)
        time.sleep(1.1)
    
    print(f"\n   ✓ Geocodificación completada:")
    print(f"      Exitosos: {geocoded_count}")
    print(f"      Fallidos: {failed_count}")
    
    # 4. Guardar CSV actualizado
    print("\n4. Guardando datos actualizados...")
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"   ✓ CSV actualizado: {csv_path}")
    
    # 5. Actualizar Google Sheets
    print("\n5. Actualizando Google Sheets...")
    credentials_path = Path("config/credentials_google.json")
    
    if not credentials_path.exists():
        print("   ⚠ No se encontró credentials_google.json")
        print("   Datos guardados solo en CSV")
        return
    
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(
            str(credentials_path),
            scopes=scopes
        )
        client = gspread.authorize(creds)
        
        # Abrir spreadsheet
        spreadsheet_id = "1-E58T6yNokv6y7VS0m5tRihXwUdz4glKQVVDYA8wPLc"
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        # Abrir worksheet maestro_instituciones
        worksheet = spreadsheet.worksheet("maestro_instituciones")
        
        # Actualizar columnas de coordenadas
        print("   Actualizando latitudes...")
        lat_values = [[str(val)] for val in df['latitud'].tolist()]
        worksheet.update(values=lat_values, range_name=f'G2:G{len(df) + 1}')
        
        print("   Actualizando longitudes...")
        lon_values = [[str(val)] for val in df['longitud'].tolist()]
        worksheet.update(values=lon_values, range_name=f'H2:H{len(df) + 1}')
        
        print("   Actualizando departamentos...")
        dept_values = [[str(val)] for val in df['departamento'].tolist()]
        worksheet.update(values=dept_values, range_name=f'F2:F{len(df) + 1}')
        
        print("   ✓ Google Sheets actualizado")
        
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={worksheet.id}"
        print(f"   URL: {sheet_url}")
        
    except Exception as e:
        print(f"   ⚠ Error al actualizar Google Sheets: {e}")
        print("   Datos guardados en CSV")
    
    # 6. Mostrar resumen
    print("\n" + "=" * 70)
    print("Geocoding completado!")
    print("=" * 70)
    print(f"\nResumen:")
    print(f"  Total instituciones: {len(df)}")
    print(f"  Con coordenadas: {geocoded_count}")
    print(f"  Sin coordenadas: {failed_count}")
    print(f"\nArchivo actualizado: {csv_path}")
    
    # Mostrar muestra
    print("\nMuestra de instituciones geocodificadas:")
    geocoded_df = df[df['latitud'] != ''].head(3)
    if not geocoded_df.empty:
        print(geocoded_df[['nombre', 'municipio', 'latitud', 'longitud']].to_string(index=False))


if __name__ == "__main__":
    geocode_maestro_instituciones()
