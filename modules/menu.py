"""
Menu module for PyQt6ify Pro.
Provides menu bar and menu items functionality.
"""

import os
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QIcon
from . import about

def create_menu_bar(window):
    """Create a menu bar for the application window."""
    menu_bar = QMenuBar(window)
    
    # File Menu
    file_menu = menu_bar.addMenu('&File')
    
    # New
    new_action = QAction('&New', window)
    new_action.setShortcut('Ctrl+N')
    new_action.setStatusTip('Create a new file')
    file_menu.addAction(new_action)
    
    # Open
    open_action = QAction('&Open...', window)
    open_action.setShortcut('Ctrl+O')
    open_action.setStatusTip('Open an existing file')
    file_menu.addAction(open_action)
    
    # Save
    save_action = QAction('&Save', window)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save the current file')
    file_menu.addAction(save_action)
    
    # Save As
    save_as_action = QAction('Save &As...', window)
    save_as_action.setShortcut('Ctrl+Shift+S')
    save_as_action.setStatusTip('Save the file with a new name')
    file_menu.addAction(save_as_action)
    
    file_menu.addSeparator()
    
    # Exit
    exit_action = QAction('E&xit', window)
    exit_action.setShortcut('Alt+F4')
    exit_action.setStatusTip('Exit the application')
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)
    
    # Edit Menu
    edit_menu = menu_bar.addMenu('&Edit')
    
    # View Menu
    view_menu = menu_bar.addMenu('&View')
    
    # Theme action
    theme_action = QAction('&Theme...', window)
    theme_action.setStatusTip('Change application theme')
    theme_action.triggered.connect(lambda: show_theme_dialog(window))
    view_menu.addAction(theme_action)
    
    # Help Menu
    help_menu = menu_bar.addMenu('&Help')
    
    # About action
    about_action = QAction('&About', window)
    about_action.setStatusTip('Show the application About box')
    about_action.triggered.connect(lambda: about.show_about_dialog(window))
    help_menu.addAction(about_action)
    
    return menu_bar

def show_theme_dialog(window):
    """Show the theme selection dialog."""
    # This is a placeholder for the actual theme dialog implementation
    pass

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
        menubar = create_menu_bar(window)  # Create a new MenuBar
        
        # Set the menubar in the window
        window.setMenuBar(menubar)
        # logging.info("Menu created successfully")
        
    except Exception as e:
        # logging.error(f"Failed to create menu: {e}")
        pass

if __name__ == "__main__":
    """
    The entry point of the PyQt6 application. This block sets up logging, 
    initializes the QApplication and main window, and starts the event loop.
    """
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the application and main window
    from PyQt6.QtWidgets import QApplication, QMainWindow
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
    # logging.info("Application started")
    app.exec()
