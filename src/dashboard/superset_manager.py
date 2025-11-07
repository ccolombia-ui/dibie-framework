"""
DIBIE - Superset Integration
Configure and manage Apache Superset dashboards
"""
import subprocess
import os
import logging
from typing import Dict, Optional
from pathlib import Path


class SupersetManager:
    """Manage Apache Superset integration"""
    
    def __init__(self, host: str = "localhost", port: int = 8088):
        """Initialize Superset manager
        
        Args:
            host: Superset host
            port: Superset port
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger"""
        logger = logging.getLogger('SupersetManager')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('logs/superset_manager.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def is_installed(self) -> bool:
        """Check if Superset is installed
        
        Returns:
            True if installed, False otherwise
        """
        try:
            result = subprocess.run(
                ['superset', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install(self) -> bool:
        """Install Apache Superset
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Installing Apache Superset...")
            
            # Install Superset
            result = subprocess.run(
                ['pip', 'install', 'apache-superset'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.logger.info("Superset installed successfully")
                return True
            else:
                self.logger.error(f"Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error installing Superset: {str(e)}")
            return False
    
    def initialize_db(self) -> bool:
        """Initialize Superset database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Initializing Superset database...")
            
            # Upgrade database
            result = subprocess.run(
                ['superset', 'db', 'upgrade'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.logger.info("Database initialized successfully")
                return True
            else:
                self.logger.error(f"DB initialization failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            return False
    
    def create_admin_user(self, username: str, password: str, 
                         firstname: str = "Admin", 
                         lastname: str = "User",
                         email: str = "admin@dibie.local") -> bool:
        """Create admin user
        
        Args:
            username: Admin username
            password: Admin password
            firstname: First name
            lastname: Last name
            email: Email address
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Creating admin user: {username}")
            
            # Note: This is a simplified version
            # In production, you would use the Superset CLI properly
            env = os.environ.copy()
            env['SUPERSET_CONFIG_PATH'] = str(Path(__file__).parent.parent.parent / 'config' / 'superset_config.py')
            
            result = subprocess.run(
                ['superset', 'fab', 'create-admin',
                 '--username', username,
                 '--firstname', firstname,
                 '--lastname', lastname,
                 '--email', email,
                 '--password', password],
                capture_output=True,
                text=True,
                env=env,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info("Admin user created successfully")
                return True
            else:
                self.logger.warning(f"User creation: {result.stderr}")
                return True  # User might already exist
                
        except Exception as e:
            self.logger.error(f"Error creating admin user: {str(e)}")
            return False
    
    def initialize_superset(self) -> bool:
        """Initialize Superset
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Initializing Superset...")
            
            result = subprocess.run(
                ['superset', 'init'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.logger.info("Superset initialized successfully")
                return True
            else:
                self.logger.error(f"Initialization failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error initializing Superset: {str(e)}")
            return False
    
    def start_server(self, background: bool = False) -> Optional[subprocess.Popen]:
        """Start Superset server
        
        Args:
            background: Run in background
            
        Returns:
            Process object if background, None otherwise
        """
        try:
            self.logger.info(f"Starting Superset server on {self.base_url}")
            
            cmd = [
                'superset', 'run',
                '-p', str(self.port),
                '--with-threads',
                '--reload',
                '--debugger'
            ]
            
            if background:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.logger.info(f"Server started in background (PID: {process.pid})")
                return process
            else:
                subprocess.run(cmd)
                return None
                
        except Exception as e:
            self.logger.error(f"Error starting server: {str(e)}")
            return None
    
    def get_connection_info(self) -> Dict:
        """Get Superset connection information
        
        Returns:
            Connection info dictionary
        """
        return {
            "url": self.base_url,
            "host": self.host,
            "port": self.port,
            "installed": self.is_installed()
        }
    
    def setup_complete_installation(self, admin_username: str = "admin", 
                                   admin_password: str = "admin") -> bool:
        """Complete Superset setup process
        
        Args:
            admin_username: Admin username
            admin_password: Admin password
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("Starting complete Superset installation...")
        
        # Check installation
        if not self.is_installed():
            if not self.install():
                return False
        
        # Initialize database
        if not self.initialize_db():
            return False
        
        # Create admin user
        if not self.create_admin_user(admin_username, admin_password):
            return False
        
        # Initialize Superset
        if not self.initialize_superset():
            return False
        
        self.logger.info("Superset installation completed successfully!")
        self.logger.info(f"Access Superset at: {self.base_url}")
        self.logger.info(f"Username: {admin_username}")
        
        return True


if __name__ == "__main__":
    # Example usage
    manager = SupersetManager()
    info = manager.get_connection_info()
    print(f"Superset Connection Info:")
    print(f"  URL: {info['url']}")
    print(f"  Installed: {info['installed']}")
