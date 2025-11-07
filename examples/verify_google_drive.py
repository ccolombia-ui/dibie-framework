"""
DIBIE - Verificación de Google Drive
Script para verificar que la sincronización con Google Drive funciona correctamente
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ingestion.google_drive_connector import GoogleDriveConnector
from ingestion.table_loader import TableLoader

def main():
    print("=" * 70)
    print("DIBIE - Verificación de Google Drive")
    print("=" * 70)
    
    # Inicializar conector
    connector = GoogleDriveConnector()
    
    # 1. Verificar acceso
    print("\n1. Verificando acceso a Google Drive...")
    if connector.is_drive_accessible():
        print(f"   ✓ Google Drive accesible")
        print(f"   Ruta: {connector.get_drive_path()}")
    else:
        print(f"   ✗ Google Drive NO accesible")
        print(f"   Ruta esperada: {connector.get_drive_path()}")
        return
    
    # 2. Listar archivos
    print("\n2. Listando archivos en Google Drive...")
    
    # Todos los archivos
    all_files = connector.list_files(pattern="*")
    print(f"   Total de archivos: {len(all_files)}")
    
    if all_files:
        print("\n   Primeros 10 archivos:")
        for i, file in enumerate(all_files[:10], 1):
            file_path = Path(file)
            print(f"   {i}. {file_path.name} ({file_path.suffix})")
    
    # 3. Archivos por tipo
    print("\n3. Archivos por tipo:")
    
    file_types = {
        'CSV': '*.csv',
        'Excel': '*.xlsx',
        'Google Sheets': '*.gsheet',
        'Documentos': '*.gdoc',
        'JSON': '*.json',
        'Parquet': '*.parquet'
    }
    
    for name, pattern in file_types.items():
        files = connector.list_files(pattern=pattern)
        if files:
            print(f"   {name}: {len(files)} archivo(s)")
            for file in files[:3]:
                print(f"      - {Path(file).name}")
    
    # 4. Información detallada del primer archivo
    if all_files:
        print("\n4. Información detallada del primer archivo:")
        first_file = all_files[0]
        info = connector.get_file_info(first_file)
        
        print(f"   Nombre: {info['name']}")
        print(f"   Ruta: {info['path']}")
        print(f"   Tamaño: {info['size_bytes']:,} bytes")
        print(f"   Modificado: {info['modified']}")
        print(f"   Extensión: {info['extension']}")
    
    # 5. Intentar cargar un archivo CSV si existe
    csv_files = connector.list_files(pattern="*.csv")
    if csv_files:
        print("\n5. Intentando cargar archivo CSV...")
        loader = TableLoader()
        
        try:
            df = loader.load_table(csv_files[0])
            table_info = loader.get_table_info(df)
            
            print(f"   ✓ Archivo cargado exitosamente:")
            print(f"      Archivo: {Path(csv_files[0]).name}")
            print(f"      Filas: {table_info['rows']:,}")
            print(f"      Columnas: {table_info['columns']}")
            print(f"      Columnas: {', '.join(table_info['column_names'][:5])}")
            
            if len(table_info['column_names']) > 5:
                print(f"      ... y {len(table_info['column_names']) - 5} más")
            
        except Exception as e:
            print(f"   ✗ Error al cargar archivo: {str(e)}")
    
    # 6. Verificar enlace simbólico
    print("\n6. Verificando enlace simbólico...")
    symlink_path = Path("data/google_drive")
    
    if symlink_path.exists():
        if symlink_path.is_symlink():
            target = symlink_path.resolve()
            print(f"   ✓ Enlace simbólico configurado correctamente")
            print(f"      Enlace: {symlink_path}")
            print(f"      Apunta a: {target}")
        else:
            print(f"   ⚠ Existe pero NO es un enlace simbólico")
    else:
        print(f"   ✗ Enlace simbólico NO existe")
        print(f"      Ejecute setup_symlink.ps1 como Administrador")
    
    print("\n" + "=" * 70)
    print("Verificación completada")
    print("=" * 70)

if __name__ == "__main__":
    main()
