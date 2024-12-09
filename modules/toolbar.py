"""
Toolbar module for PyQt6ify Pro.
Provides toolbar functionality with icons and actions.
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon
from loguru import logger

def create_toolbar(window):
    """Create a toolbar for the application window."""
    toolbar = QToolBar(window)
    icons_dir = Path('icons')
    
    def create_action(name, tooltip, shortcut=None):
        """Helper function to create toolbar actions."""
        action = QAction(name, window)
        icon_path = icons_dir / f"{name.lower().replace(' ', '_')}.png"
        if icon_path.exists():
            action.setIcon(QIcon(str(icon_path)))
        action.setToolTip(tooltip)
        if shortcut:
            action.setShortcut(shortcut)
        return action
    
    try:
        # New
        new_action = create_action('New', 'Create a new file', 'Ctrl+N')
        toolbar.addAction(new_action)
        
        # Open
        open_action = create_action('Open', 'Open an existing file', 'Ctrl+O')
        toolbar.addAction(open_action)
        
        # Save
        save_action = create_action('Save', 'Save the current file', 'Ctrl+S')
        toolbar.addAction(save_action)
        
        # Save As
        save_as_action = create_action('Save As', 'Save the file with a new name', 'Ctrl+Shift+S')
        toolbar.addAction(save_as_action)
        
    except Exception as e:
        logger.error(f"Failed to create toolbar: {e}")
    
    return toolbar
