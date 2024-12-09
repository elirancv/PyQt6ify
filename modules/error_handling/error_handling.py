"""
Error handling implementation for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QMessageBox
from loguru import logger

def show_error_dialog(title, message, parent=None):
    """
    Show an error dialog with the specified title and message.
    
    Args:
        title (str): Title of the error dialog
        message (str): Error message to display
        parent (QWidget, optional): Parent widget for the dialog
    """
    try:
        error_dialog = QMessageBox(parent)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Log the error
        logger.error(f"{title}: {message}")
        
        # Show the dialog
        error_dialog.exec()
        
    except Exception as e:
        logger.error(f"Error showing error dialog: {str(e)}")
        # If we can't show the error dialog, at least print to console
        print(f"Error: {title} - {message}")
