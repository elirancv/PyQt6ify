import logging
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon
from modules.status_bar import update_status_bar

def create_toolbar(window):
    """
    Create a default toolbar for the application window with icons for each option.
    
    :param window: The main application window.
    """
    try:
        toolbar = QToolBar("Main Toolbar")
        window.addToolBar(toolbar)

        # File actions
        new_action = QAction(QIcon('resources/icons/new.png'), 'New', window)
        open_action = QAction(QIcon('resources/icons/open.png'), 'Open', window)
        save_action = QAction(QIcon('resources/icons/save.png'), 'Save', window)
        
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        
        # Edit actions
        undo_action = QAction(QIcon('resources/icons/undo.png'), 'Undo', window)
        redo_action = QAction(QIcon('resources/icons/redo.png'), 'Redo', window)
        cut_action = QAction(QIcon('resources/icons/cut.png'), 'Cut', window)
        copy_action = QAction(QIcon('resources/icons/copy.png'), 'Copy', window)
        paste_action = QAction(QIcon('resources/icons/paste.png'), 'Paste', window)
        
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addSeparator()
        toolbar.addAction(cut_action)
        toolbar.addAction(copy_action)
        toolbar.addAction(paste_action)
        toolbar.addSeparator()
        
        # Exit action
        exit_action = QAction(QIcon('resources/icons/exit.png'), 'Exit', window)
        exit_action.triggered.connect(window.close)
        toolbar.addAction(exit_action)
        
        logging.info("Toolbar created successfully")
        
        # Connect actions to status bar updates
        new_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "New file created"))
        open_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File opened"))
        save_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File saved"))
        undo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Undo action"))
        redo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Redo action"))
        cut_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Cut action"))
        copy_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Copy action"))
        paste_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Paste action"))
        
    except Exception as e:
        logging.error(f"Failed to create toolbar: {e}")

