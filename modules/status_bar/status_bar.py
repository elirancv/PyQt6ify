"""
Status bar module for PyQt6ify Pro.
"""
from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import Qt
from loguru import logger

class StatusBar(QStatusBar):
    """Status bar class for the application."""

    def __init__(self, parent=None):
        """Initialize status bar."""
        super().__init__(parent)
        self.parent = parent
        self.message_label = None
        self.theme_label = None
        self.init_status_bar()

    def init_status_bar(self):
        """Initialize status bar components."""
        try:
            self.setStyleSheet("QStatusBar::item { border: none; }")
            self.create_permanent_widgets()
            self.update_message("Ready")
        except Exception as e:
            logger.error(f"Error initializing status bar: {str(e)}")

    def create_permanent_widgets(self):
        """Create permanent widgets for the status bar."""
        try:
            self.message_label = QLabel("Ready")
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.addWidget(self.message_label)
        except Exception as e:
            logger.error(f"Error creating permanent widgets: {str(e)}")

    def update_message(self, message: str):
        """
        Update the status bar message.

        Args:
            message (str): Message to display
        """
        try:
            self.message_label.setText(message)
        except Exception as e:
            logger.error(f"Error updating status bar message: {str(e)}")

    def update_theme_label(self, theme_name: str):
        """
        Update the theme label.

        Args:
            theme_name (str): Name of the current theme
        """
        try:
            if self.theme_label:
                self.theme_label.setText(f"Theme: {theme_name.capitalize()}")
                logger.debug(f"Updated status bar theme label to: {theme_name}")
        except Exception as e:
            logger.error(f"Error updating theme label: {str(e)}")
