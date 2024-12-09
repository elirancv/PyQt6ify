import logging
import os
from loguru import logger
from PyQt6.QtWidgets import QMessageBox

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,  # Changed to INFO level
                        format='%(asctime)s:%(levelname)s:%(message)s')

def log_error(error):
    logging.error(error)

def show_error_dialog(title, message):
    """
    Show an error dialog with the given title and message.
    
    Args:
        title (str): The title of the error dialog
        message (str): The error message to display
    """
    logger.error(f"{title}: {message}")
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Icon.Critical)
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.exec()
