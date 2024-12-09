"""
Main window implementation for PyQt6ify Pro.
"""

import os
from loguru import logger
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from .module_loader import ModuleLoader
from modules.themes.theme_dialog import ThemeDialog

class MainWindow(QMainWindow):
    """
    MainWindow class responsible for setting up the main UI window 
    and initializing the application based on configuration settings.
    """
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db_connection = None
        
        # Get the base path (project root)
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Initialize module loader with correct base path
        self.module_loader = ModuleLoader(self.base_path)
        
        # Load modules and extensions
        self.modules = {}
        self.load_modules()
        
        # Initialize theme manager
        theme_manager_class = self.get_module_class('themes.theme_manager', 'ThemeManager')
        if theme_manager_class:
            self.theme_manager = theme_manager_class(QApplication.instance(), self.config)
        
        self.init_ui()

    def load_modules(self):
        """Load all modules from the modules directory."""
        try:
            modules_dir = os.path.join(self.base_path, 'modules')
            self.modules = self.module_loader.load_all_modules(modules_dir)
            logger.debug(f"Loaded modules: {list(self.modules.keys())}")
        except Exception as e:
            logger.error(f"Error loading modules: {str(e)}")

    def get_module_class(self, module_name, class_name):
        """
        Get a class from a loaded module.
        
        Args:
            module_name (str): Name of the module
            class_name (str): Name of the class
            
        Returns:
            class: The requested class or None if not found
        """
        try:
            logger.debug(f"Looking for class {class_name} in module {module_name}")
            logger.debug(f"Available modules: {list(self.modules.keys())}")
            
            # Try direct module path first
            if module_name in self.modules:
                module = self.modules[module_name]
                if hasattr(module, class_name):
                    return getattr(module, class_name)
            
            # Try with 'modules.' prefix
            module_path = f'modules.{module_name}'
            if module_path in self.modules:
                module = self.modules[module_path]
                if hasattr(module, class_name):
                    return getattr(module, class_name)
            
            logger.error(f"Class {class_name} not found in module {module_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting class {class_name} from module {module_name}: {str(e)}")
            return None

    def init_ui(self):
        """Initialize the main user interface elements of the window."""
        try:
            self.setup_window_properties()
            self.init_components()
            self.init_database()
            self.show()
        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}")

    def setup_window_properties(self):
        """Set up basic window properties like title, icon, and size."""
        try:
            app_name = self.config.get('Application', 'Name', 'PyQt6ify Pro')
            app_version = self.config.get('Application', 'Version', '1.0.0')
            self.setWindowTitle(f"{app_name} {app_version}")
            
            # Use icon path from config
            icon_path = self.config.get('About', 'icon', 'resources/icons/app_icon.png')
            icon_path = os.path.join(self.base_path, icon_path)
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
                logger.debug(f"Set window icon from: {icon_path}")
            else:
                logger.warning(f"Icon not found at path: {icon_path}")
            
            width = int(self.config.get('Window', 'screen_width', '1024'))
            height = int(self.config.get('Window', 'screen_height', '768'))
            self.setGeometry(100, 100, width, height)
            
            if self.config.get('Window', 'start_maximized', 'True').lower() == 'true':
                self.setWindowState(Qt.WindowState.WindowMaximized)
        except Exception as e:
            logger.error(f"Error setting window properties: {str(e)}")

    def init_components(self):
        """Initialize UI components based on configuration."""
        try:
            # Initialize menu bar
            menu_class = self.get_module_class('menu.menu', 'MenuBar')
            if menu_class:
                self.menu_bar = menu_class(self)
                self.setMenuBar(self.menu_bar)
                logger.debug("Menu bar initialized")
            
            # Initialize toolbar
            toolbar_class = self.get_module_class('toolbar.toolbar', 'ToolBar')
            if toolbar_class:
                self.tool_bar = toolbar_class(self)
                self.addToolBar(self.tool_bar)
                logger.debug("Toolbar initialized")
            
            # Initialize status bar
            status_bar_class = self.get_module_class('status_bar.status_bar', 'StatusBar')
            if status_bar_class:
                self.status_bar = status_bar_class(self)
                self.setStatusBar(self.status_bar)
                logger.debug("Status bar initialized")
            
            # Initialize dashboard
            dashboard_class = self.get_module_class('dashboard.dashboard', 'Dashboard')
            logger.debug(f"Dashboard class found: {dashboard_class}")
            if dashboard_class:
                self.dashboard = dashboard_class(self)
                self.setCentralWidget(self.dashboard)
                logger.debug("Dashboard initialized and set as central widget")
            else:
                logger.error("Failed to load dashboard class")
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")

    def init_database(self):
        """Initialize database."""
        try:
            Database = self.get_module_class('database.database', 'Database')
            if Database:
                self.database = Database(config=self.config)
                logger.debug("Database initialized")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")

    def show_theme_dialog(self):
        """Show the theme selection dialog."""
        try:
            dialog = ThemeDialog(self, theme_manager=self.theme_manager)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error showing theme dialog: {str(e)}")
            logger.error(traceback.format_exc())

    def closeEvent(self, event):
        """
        Handle application shutdown.
        Clean up resources and close connections.
        """
        try:
            if self.db_connection:
                self.db_connection.close()
                logger.info("Closing database connection")
            
            logger.info("Application shutting down")
            event.accept()
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")
            event.accept()
