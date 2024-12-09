"""
Menu module for PyQt6ify Pro.
Provides menu bar and menu items functionality.
"""

import os
from PyQt6.QtWidgets import QMenuBar, QMenu, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from . import about


class MenuBar(QMenuBar):
    """Custom menu bar for the application."""
    
    def __init__(self, parent=None):
        """Initialize the menu bar."""
        super().__init__(parent)
        self.parent = parent
        self.icons_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'icons')
        self.setup_menus()
    
    def get_icon(self, icon_name):
        """Get an icon from the resources directory."""
        icon_path = os.path.join(self.icons_path, f"{icon_name}.png")
        return QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
    
    def setup_menus(self):
        """Set up all menus."""
        self.setup_file_menu()
        self.setup_edit_menu()
        self.setup_view_menu()
        self.setup_help_menu()
    
    def setup_file_menu(self):
        """Set up the File menu."""
        file_menu = self.addMenu('&File')
        
        # New
        new_action = QAction(self.get_icon('new'), '&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create a new file')
        file_menu.addAction(new_action)
        
        # Open
        open_action = QAction(self.get_icon('open'), '&Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open an existing file')
        file_menu.addAction(open_action)
        
        # Save
        save_action = QAction(self.get_icon('save'), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save the current file')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction(self.get_icon('exit'), 'E&xit', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)
    
    def setup_edit_menu(self):
        """Set up the Edit menu."""
        edit_menu = self.addMenu('&Edit')
        
        # Undo
        undo_action = QAction(self.get_icon('undo'), '&Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        edit_menu.addAction(undo_action)
        
        # Redo
        redo_action = QAction(self.get_icon('redo'), '&Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut
        cut_action = QAction(self.get_icon('cut'), 'Cu&t', self)
        cut_action.setShortcut('Ctrl+X')
        edit_menu.addAction(cut_action)
        
        # Copy
        copy_action = QAction(self.get_icon('copy'), '&Copy', self)
        copy_action.setShortcut('Ctrl+C')
        edit_menu.addAction(copy_action)
        
        # Paste
        paste_action = QAction(self.get_icon('paste'), '&Paste', self)
        paste_action.setShortcut('Ctrl+V')
        edit_menu.addAction(paste_action)
        
    def setup_view_menu(self):
        """Set up the View menu."""
        view_menu = self.addMenu('&View')
        
        # Themes
        theme_action = QAction(self.get_icon('themes'), '&Themes...', self)
        theme_action.setStatusTip('Customize application theme')
        theme_action.triggered.connect(self.parent.show_theme_dialog)
        view_menu.addAction(theme_action)
    
    def setup_help_menu(self):
        """Set up the Help menu."""
        help_menu = self.addMenu('&Help')
        
        # About
        about_action = QAction(self.get_icon('about'), '&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_about(self):
        """Show the About dialog."""
        about_dialog = about.AboutDialog(self.parent)
        about_dialog.exec()


def update_status_bar(status_bar, message):
    """
    Update the status bar with the provided message.
    
    :param status_bar: The status bar of the window.
    :param message: The message to display on the status bar.
    """
    status_bar.showMessage(message)


def create_menu(window, config):
    """
    Create a default menu for the application window with icons for each option.
    
    :param window: The main application window (must be QMainWindow).
    :param config: The configuration object for the application.
    """
    try:
        menubar = MenuBar(window)  # Create a new MenuBar
        
        # Set the menubar in the window
        window.setMenuBar(menubar)
        logging.info("Menu created successfully")
        
        # **Connect menu actions to update status bar**
        # new_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "New file created"))
        # open_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File opened"))
        # save_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File saved"))
        # undo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Undo action"))
        # redo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Redo action"))
        # cut_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Cut action"))
        # copy_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Copy action"))
        # paste_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Paste action"))
        # about_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Opened About dialog"))
        
    except Exception as e:
        logging.error(f"Failed to create menu: {e}")


if __name__ == "__main__":
    """
    The entry point of the PyQt6 application. This block sets up logging, 
    initializes the QApplication and main window, and starts the event loop.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the application and main window
    app = QApplication([])
    window = QMainWindow()

    # Initialize the config (ensure that Config is imported properly if necessary)
    from app_config import Config
    config = Config()

    # Create the application menu
    create_menu(window, config)  # Ensure that config is passed

    # Show the main window
    window.show()

    # Log that the application has started and begin the event loop
    logging.info("Application started")
    app.exec()
