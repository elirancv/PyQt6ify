import sys
import os
from loguru import logger
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from config.app_config import Config, ConfigError
from modules import error_handling, database, menu, status_bar, toolbar, about

class MainWindow(QMainWindow):
    """
    MainWindow class responsible for setting up the main UI window 
    and initializing the application based on configuration settings.
    """
    def __init__(self, config):
        """
        Initialize the MainWindow and UI components.
        
        Args:
            config (Config): Configuration instance
        """
        super().__init__()
        self.config = config
        self.db_connection = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes the main user interface elements of the window.
        Sets up window properties, menus, toolbars, and status bar based on configuration.
        """
        try:
            start_time = time.time()
            logger.info("Initializing UI")
            
            # Set window properties
            self.setup_window_properties()
            
            # Initialize UI components
            self.init_components()
            
            end_time = time.time()
            logger.info(f"UI initialized in {end_time - start_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Failed to initialize UI: {str(e)}")
            error_handling.show_error_dialog("UI Initialization Error", str(e))

    def setup_window_properties(self):
        """Set up basic window properties like title, icon, and size."""
        try:
            self.setWindowTitle(self.config.get_about_info('name'))
            
            # Set window icon with validation
            icon_path = self.config.get_about_info('icon')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                logger.warning(f"Icon not found at path: {icon_path}")
            
            # Set window geometry
            width = int(self.config.get_app_setting('screen_width', '1024'))
            height = int(self.config.get_app_setting('screen_height', '768'))
            self.setGeometry(100, 100, width, height)
            
            if self.config.get_app_setting('start_maximized', 'True').lower() == 'true':
                self.setWindowState(Qt.WindowState.WindowMaximized)
        except Exception as e:
            logger.error(f"Error setting window properties: {str(e)}")
            raise

    def init_components(self):
        """Initialize UI components based on configuration."""
        try:
            if self.config.is_module_enabled('menu'):
                logger.info("Creating menu")
                menu.create_menu(self, self.config)
            
            if self.config.is_module_enabled('status_bar'):
                logger.info("Creating status bar")
                status_bar.create_status_bar(self)
                self.statusBar().showMessage("Ready")
            
            if self.config.is_module_enabled('toolbar'):
                logger.info("Creating toolbar")
                toolbar.create_toolbar(self)
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            raise

    def init_database(self):
        """Initialize database connection if enabled."""
        if self.config.is_module_enabled('database'):
            try:
                logger.info("Initializing database")
                self.db_connection = database.initialize_database()
            except Exception as e:
                logger.error(f"Database initialization failed: {str(e)}")
                error_handling.show_error_dialog("Database Error", str(e))

    def closeEvent(self, event):
        """
        Handle application shutdown.
        Clean up resources and close connections.
        """
        try:
            if self.db_connection:
                logger.info("Closing database connection")
                self.db_connection.close()
            
            logger.info("Application shutting down")
            event.accept()
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")
            event.accept()

def setup_logging():
    """Configure logging with rotation and proper formatting."""
    try:
        # Remove default logger
        logger.remove()
        
        # Add file logger with rotation
        logger.add(
            "logs/app.log",
            rotation="500 MB",
            retention="10 days",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO"
        )
        
        # Add console logger
        logger.add(
            sys.stderr,
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO"
        )
    except Exception as e:
        print(f"Failed to setup logging: {str(e)}")
        sys.exit(1)

def main():
    """
    Main application entry point.
    Initializes logging, configuration, and creates the main window.
    """
    try:
        # Setup logging first
        setup_logging()
        logger.info("Starting application")
        start_time = time.time()
        
        # Initialize configuration
        config = Config()
        
        # Create QApplication instance
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = MainWindow(config)
        window.show()
        
        # Initialize database after window is shown
        window.init_database()
        
        end_time = time.time()
        logger.info(f"Application startup completed in {end_time - start_time:.2f} seconds")
        
        # Start event loop
        sys.exit(app.exec())
    except ConfigError as e:
        logger.error(f"Configuration error: {str(e)}")
        error_handling.show_error_dialog("Configuration Error", str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        error_handling.show_error_dialog("Critical Error", str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
