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
        # Log the error
        logger.error(f"{title}: {message}")
        
        # Show the dialog using QMessageBox.critical
        return QMessageBox.critical(
            parent,
            title,
            message,
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        
    except Exception as e:
        logger.error(f"Error showing error dialog: {str(e)}")
        # If we can't show the error dialog, at least print to console
        print(f"Error: {title} - {message}")
        return QMessageBox.StandardButton.Ok
