"""
Example: Setup and Start Apache Superset
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from dashboard.superset_manager import SupersetManager

def main():
    print("=" * 60)
    print("DIBIE - Apache Superset Setup")
    print("=" * 60)
    
    # Initialize Superset manager
    manager = SupersetManager(host='localhost', port=8088)
    
    # Check if already installed
    if manager.is_installed():
        print("\n✓ Apache Superset is already installed")
        
        # Get connection info
        info = manager.get_connection_info()
        print(f"\nConnection Info:")
        print(f"  URL: {info['url']}")
        print(f"  Host: {info['host']}")
        print(f"  Port: {info['port']}")
        
        # Ask to start server
        response = input("\n¿Iniciar servidor de Superset? (s/n): ")
        if response.lower() == 's':
            print("\nIniciando Superset...")
            print("Presione Ctrl+C para detener el servidor")
            print(f"Acceda a: {info['url']}")
            manager.start_server(background=False)
    else:
        print("\n✗ Apache Superset no está instalado")
        response = input("¿Desea instalar Superset ahora? (s/n): ")
        
        if response.lower() == 's':
            print("\nInstalando Apache Superset...")
            print("Esto puede tomar varios minutos...")
            
            # Prompt for admin credentials
            username = input("Username para admin (default: admin): ") or "admin"
            password = input("Password para admin (default: admin): ") or "admin"
            
            # Complete setup
            if manager.setup_complete_installation(username, password):
                print("\n" + "=" * 60)
                print("✓ Superset instalado exitosamente!")
                print("=" * 60)
                print(f"\nAcceda a: {manager.base_url}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                print("\nPara iniciar el servidor, ejecute:")
                print("  python examples/superset_setup.py")
            else:
                print("\n✗ Error durante la instalación")
                print("Por favor, revise los logs en logs/superset_manager.log")

if __name__ == "__main__":
    main()
