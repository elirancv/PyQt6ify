from PyQt6.QtWidgets import QMenuBar, QMainWindow
from PyQt6.QtGui import QIcon, QAction
import logging
from modules import status_bar, about


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
        menubar = QMenuBar(window)  # Create a new QMenuBar
        
        # File menu
        file_menu = menubar.addMenu('File')
        new_action = QAction(QIcon('resources/icons/new.png'), 'New', window)
        open_action = QAction(QIcon('resources/icons/open.png'), 'Open', window)
        save_action = QAction(QIcon('resources/icons/save.png'), 'Save', window)
        exit_action = QAction(QIcon('resources/icons/exit.png'), 'Exit', window)
        exit_action.triggered.connect(window.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        undo_action = QAction(QIcon('resources/icons/undo.png'), 'Undo', window)
        redo_action = QAction(QIcon('resources/icons/redo.png'), 'Redo', window)
        cut_action = QAction(QIcon('resources/icons/cut.png'), 'Cut', window)
        copy_action = QAction(QIcon('resources/icons/copy.png'), 'Copy', window)
        paste_action = QAction(QIcon('resources/icons/paste.png'), 'Paste', window)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction(QIcon('resources/icons/about.png'), 'About', window)
        about_action.triggered.connect(lambda: about.show_about_dialog(window, config))
        help_menu.addAction(about_action)
        
        # Set the menubar in the window
        window.setMenuBar(menubar)
        logging.info("Menu created successfully")
        
        # **Connect menu actions to update status bar**
        new_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "New file created"))
        open_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File opened"))
        save_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File saved"))
        undo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Undo action"))
        redo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Redo action"))
        cut_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Cut action"))
        copy_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Copy action"))
        paste_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Paste action"))
        about_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Opened About dialog"))
        
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
