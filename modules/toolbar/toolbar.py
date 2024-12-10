"""
Toolbar module for PyQt6ify Pro.
"""
import os
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize

class ToolBar(QToolBar):
    """Main toolbar class."""

    def __init__(self, parent=None):
        """Initialize toolbar."""
        super().__init__(parent)
        self.parent = parent
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'icons')
        self.init_toolbar()

    def init_toolbar(self):
        """Initialize toolbar items."""
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.add_file_actions()
        self.add_edit_actions()
        self.add_view_actions()

    def get_icon(self, icon_name: str) -> QIcon:
        """Get icon from resources."""
        icon_path = os.path.join(self.icon_path, f"{icon_name}.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    def add_file_actions(self):
        """Add file-related actions."""
        new_action = QAction(self.get_icon('new'), 'New', self)
        new_action.setStatusTip('Create a new file')
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.parent.new_file if hasattr(self.parent, 'new_file') else lambda: None)
        self.addAction(new_action)

        open_action = QAction(self.get_icon('open'), 'Open', self)
        open_action.setStatusTip('Open an existing file')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.parent.open_file if hasattr(self.parent, 'open_file') else lambda: None)
        self.addAction(open_action)

        save_action = QAction(self.get_icon('save'), 'Save', self)
        save_action.setStatusTip('Save the current file')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.parent.save_file if hasattr(self.parent, 'save_file') else lambda: None)
        self.addAction(save_action)

        self.addSeparator()

    def add_edit_actions(self):
        """Add edit-related actions."""
        cut_action = QAction(self.get_icon('cut'), 'Cut', self)
        cut_action.setStatusTip('Cut the selection')
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.parent.cut if hasattr(self.parent, 'cut') else lambda: None)
        self.addAction(cut_action)

        copy_action = QAction(self.get_icon('copy'), 'Copy', self)
        copy_action.setStatusTip('Copy the selection')
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.parent.copy if hasattr(self.parent, 'copy') else lambda: None)
        self.addAction(copy_action)

        paste_action = QAction(self.get_icon('paste'), 'Paste', self)
        paste_action.setStatusTip('Paste from clipboard')
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.parent.paste if hasattr(self.parent, 'paste') else lambda: None)
        self.addAction(paste_action)

        self.addSeparator()

    def add_view_actions(self):
        """Add view-related actions."""
        theme_action = QAction(self.get_icon('theme'), 'Theme', self)
        theme_action.setStatusTip('Change application theme')
        theme_action.triggered.connect(self.parent.show_theme_dialog)
        self.addAction(theme_action)

        settings_action = QAction(self.get_icon('settings'), 'Settings', self)
        settings_action.setStatusTip('Application settings')
        self.addAction(settings_action)
