"""
Main window implementation for PyQt6ify Pro.
"""

import os
import sys
import importlib
import traceback
from loguru import logger
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from modules.themes.theme_dialog import ThemeDialog
from modules.themes.theme_manager import ThemeManager
from modules.menu.menu import MenuBar
from modules.toolbar.toolbar import ToolBar
from modules.status_bar.status_bar import StatusBar
from modules.dashboard.dashboard import Dashboard
from modules.database.database import Database

class MainWindow(QMainWindow):
    """
    MainWindow class responsible for setting up the main UI window
    and initializing the application based on configuration settings.
    """
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db_connection = None
        self.menu_bar = None
        self.tool_bar = None
        self.status_bar = None
        self.dashboard = None
        self.database = None
        self.theme_manager = None

        # Get the base path (project root)
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # Add base path to Python path
        if self.base_path not in sys.path:
            sys.path.insert(0, self.base_path)

        # Initialize theme manager
        self.theme_manager = ThemeManager(QApplication.instance(), self.config)

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize the main user interface elements of the window."""
        try:
            self.setup_window_properties()
            self.init_components()
            self.init_database()
            self.show()
        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}")
            traceback.print_exc()

    def setup_window_properties(self):
        """Set up basic window properties like title, icon, and size."""
        try:
            app_name = self.config.get('application', 'name', 'PyQt6ify Pro')
            app_version = self.config.get('application', 'version', '1.0.0')
            self.setWindowTitle(f"{app_name} {app_version}")

            # Set window icon
            icon_path = self.config.get('about', 'icon', 'resources\\icons\\app.png')
            if icon_path:
                # If path is relative, make it absolute
                if not os.path.isabs(icon_path):
                    icon_path = os.path.normpath(os.path.join(self.base_path, icon_path))
                logger.debug(f"Set window icon from: {icon_path}")
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
                else:
                    logger.warning(f"Icon not found at path: {icon_path}")

            # Set window size
            size = self.config.get('window', 'size', '800x600').split('x')
            self.resize(int(size[0]), int(size[1]))

            # Set window position
            position = self.config.get('window', 'position', 'center')
            if position == 'center':
                screen = QApplication.primaryScreen().geometry()
                x = (screen.width() - self.width()) // 2
                y = (screen.height() - self.height()) // 2
                self.move(x, y)

            # Set maximized state
            if self.config.get('window', 'start_maximized', 'True').lower() == 'true':
                self.setWindowState(Qt.WindowState.WindowMaximized)
        except Exception as e:
            logger.error(f"Error setting window properties: {str(e)}")
            traceback.print_exc()

    def init_components(self):
        """Initialize UI components based on configuration."""
        try:
            # Initialize menu bar
            self.menu_bar = MenuBar(self)
            self.setMenuBar(self.menu_bar)

            # Initialize toolbar
            self.tool_bar = ToolBar(self)
            self.addToolBar(self.tool_bar)

            # Initialize status bar
            self.status_bar = StatusBar(self)
            self.setStatusBar(self.status_bar)

            # Initialize dashboard
            self.dashboard = Dashboard(self)
            self.setCentralWidget(self.dashboard)

            # Initialize database
            self.database = Database(self)

        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            traceback.print_exc()

    def init_database(self):
        """Initialize database."""
        try:
            # Database is already initialized in init_components
            pass
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            traceback.print_exc()

    def show_theme_dialog(self):
        """Show the theme selection dialog."""
        try:
            dialog = ThemeDialog(self.theme_manager, self)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error showing theme dialog: {str(e)}")
            traceback.print_exc()

    def show_about_dialog(self):
        """Show the about dialog."""
        try:
            from modules.about import show_about_dialog
            show_about_dialog(self)
        except Exception as e:
            logger.error(f"Error showing about dialog: {str(e)}")
            traceback.print_exc()

    def closeEvent(self, event):
        """Handle application shutdown."""
        logger.info("Application shutting down")
        event.accept()
