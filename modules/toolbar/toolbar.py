"""
Toolbar implementation for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QToolBar, QMainWindow
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize
import os
from loguru import logger

class ToolBar(QToolBar):
    """Main toolbar class for the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_toolbar()
    
    def init_toolbar(self):
        """Initialize the toolbar with actions."""
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        # Add actions
        self.add_file_actions()
        self.add_edit_actions()
        self.add_view_actions()
        
    def add_file_actions(self):
        """Add file-related actions to the toolbar."""
        # New
        new_action = QAction(self.get_icon('new.png'), 'New', self)
        new_action.setStatusTip('Create a new file')
        new_action.setShortcut('Ctrl+N')
        self.addAction(new_action)
        
        # Open
        open_action = QAction(self.get_icon('open.png'), 'Open', self)
        open_action.setStatusTip('Open an existing file')
        open_action.setShortcut('Ctrl+O')
        self.addAction(open_action)
        
        # Save
        save_action = QAction(self.get_icon('save.png'), 'Save', self)
        save_action.setStatusTip('Save the current file')
        save_action.setShortcut('Ctrl+S')
        self.addAction(save_action)
        
        self.addSeparator()
    
    def add_edit_actions(self):
        """Add edit-related actions to the toolbar."""
        # Cut
        cut_action = QAction(self.get_icon('cut.png'), 'Cut', self)
        cut_action.setStatusTip('Cut the selection')
        cut_action.setShortcut('Ctrl+X')
        self.addAction(cut_action)
        
        # Copy
        copy_action = QAction(self.get_icon('copy.png'), 'Copy', self)
        copy_action.setStatusTip('Copy the selection')
        copy_action.setShortcut('Ctrl+C')
        self.addAction(copy_action)
        
        # Paste
        paste_action = QAction(self.get_icon('paste.png'), 'Paste', self)
        paste_action.setStatusTip('Paste from clipboard')
        paste_action.setShortcut('Ctrl+V')
        self.addAction(paste_action)
        
        self.addSeparator()
    
    def add_view_actions(self):
        """Add view-related actions to the toolbar."""
        # Theme
        theme_action = QAction(self.get_icon('theme.png'), 'Theme', self)
        theme_action.setStatusTip('Change application theme')
        theme_action.triggered.connect(lambda: self.parent.show_theme_dialog())
        self.addAction(theme_action)
        
        # Settings
        settings_action = QAction(self.get_icon('settings.png'), 'Settings', self)
        settings_action.setStatusTip('Application settings')
        self.addAction(settings_action)
    
    def get_icon(self, icon_name):
        """
        Get an icon from the resources directory.
        
        Args:
            icon_name (str): Name of the icon file
            
        Returns:
            QIcon: The icon object or a default icon if not found
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        icon_path = os.path.join(base_dir, 'resources', 'icons', icon_name)
        
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        else:
            logger.warning(f"Icon not found: {icon_path}")
            return QIcon()
