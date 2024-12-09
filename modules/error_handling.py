"""
Error handling module for PyQt6ify Pro.
Provides error dialog and logging functionality.
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from loguru import logger

def setup_logging(log_file):
    """Set up logging configuration."""
    try:
        # Create the log directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(exist_ok=True)
        
        # Remove existing logger
        logger.remove()
        
        # Add file logger
        logger.add(log_file, 
                  format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {module}:{function}:{line} - {message}",
                  level="DEBUG",
                  rotation="1 MB",
                  retention="1 week")
        
        logger.info("Logging setup completed")
        return True
        
    except Exception as e:
        print(f"Failed to setup logging: {e}")
        return False

def show_error_dialog(title, message):
    """Show an error dialog with the given title and message."""
    try:
        # Log the error
        logger.error(f"{title}: {message}")
        
        # Create and show the error dialog
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()
        
    except Exception as e:
        logger.error(f"Failed to show error dialog: {e}")
