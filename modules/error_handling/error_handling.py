"""Error handling module for PyQt6ify Pro."""
from PyQt6.QtWidgets import QMessageBox
from loguru import logger

def show_error_dialog(title: str, message: str, parent=None, details: str = None) -> QMessageBox:
    """
    Show an error dialog with the given title and message.

    Args:
        title (str): The title of the error dialog
        message (str): The error message to display
        parent (QWidget, optional): The parent widget. Defaults to None.
        details (str, optional): Additional error details. Defaults to None.

    Returns:
        QMessageBox: The error dialog that was shown
    """
    try:
        dialog = QMessageBox(parent)
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        if details:
            dialog.setDetailedText(details)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()
        return dialog
    except Exception as e:
        logger.error(f"Failed to show error dialog: {str(e)}")
        print(f"Error: {title} - {message}")
        return QMessageBox()
