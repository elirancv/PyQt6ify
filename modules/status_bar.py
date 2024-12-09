"""
Status Bar module for PyQt6ify Pro.
Provides status bar functionality.
"""

from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import Qt
from loguru import logger

class StatusBar(QStatusBar):
    """Custom status bar for the application."""
    
    def __init__(self, parent=None):
        """Initialize the status bar."""
        super().__init__(parent)
        self.setup_status_bar()
    
    def setup_status_bar(self):
        """Set up the status bar with permanent widgets."""
        try:
            # Add permanent message
            self.permanent_message = QLabel()
            self.permanent_message.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.addPermanentWidget(self.permanent_message)
            
            # Set initial message
            self.permanent_message.setText("Ready")
            
        except Exception as e:
            logger.error(f"Error setting up status bar: {e}")
    
    def update_permanent_message(self, message):
        """Update the permanent message in the status bar."""
        try:
            self.permanent_message.setText(message)
        except Exception as e:
            logger.error(f"Error updating permanent message: {e}")
    
    def showMessage(self, message, timeout=0):
        """Override showMessage to add logging."""
        try:
            super().showMessage(message, timeout)
            logger.debug(f"Status bar message: {message}")
        except Exception as e:
            logger.error(f"Error showing message: {e}")
