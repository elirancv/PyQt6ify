"""
Toolbar module for PyQt6ify Pro.
Provides toolbar functionality with icons and actions.
"""

from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon
import os
from loguru import logger

class ToolBar(QToolBar):
    """Custom toolbar for the application."""
    
    def __init__(self, parent=None):
        """Initialize the toolbar."""
        super().__init__(parent)
        self.parent = parent
        self.setup_toolbar()
    
    def setup_toolbar(self):
        """Set up the toolbar with actions and icons."""
        try:
            # New
            new_action = self.create_action('new.png', 'New', 'Create new file', 'Ctrl+N')
            self.addAction(new_action)
            
            # Open
            open_action = self.create_action('open.png', 'Open', 'Open file', 'Ctrl+O')
            self.addAction(open_action)
            
            # Save
            save_action = self.create_action('save.png', 'Save', 'Save file', 'Ctrl+S')
            self.addAction(save_action)
            
            self.addSeparator()
            
            # Cut
            cut_action = self.create_action('cut.png', 'Cut', 'Cut selection', 'Ctrl+X')
            self.addAction(cut_action)
            
            # Copy
            copy_action = self.create_action('copy.png', 'Copy', 'Copy selection', 'Ctrl+C')
            self.addAction(copy_action)
            
            # Paste
            paste_action = self.create_action('paste.png', 'Paste', 'Paste', 'Ctrl+V')
            self.addAction(paste_action)
            
            self.addSeparator()
            
            # Undo
            undo_action = self.create_action('undo.png', 'Undo', 'Undo last action', 'Ctrl+Z')
            self.addAction(undo_action)
            
            # Redo
            redo_action = self.create_action('redo.png', 'Redo', 'Redo last action', 'Ctrl+Y')
            self.addAction(redo_action)
            
        except Exception as e:
            logger.error(f"Error setting up toolbar: {e}")
    
    def create_action(self, icon_name, text, status_tip, shortcut=None):
        """Create a QAction with the specified properties."""
        try:
            icon_path = os.path.join('resources', 'icons', icon_name)
            action = QAction(QIcon(icon_path), text, self)
            
            if shortcut:
                action.setShortcut(shortcut)
            
            action.setStatusTip(status_tip)
            return action
            
        except Exception as e:
            logger.error(f"Error creating action {text}: {e}")
            # Return a basic action without icon if there's an error
            return QAction(text, self)
