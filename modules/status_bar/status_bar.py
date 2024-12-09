"""
Status bar implementation for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QStatusBar, QLabel
from PyQt6.QtCore import Qt
from loguru import logger

class StatusBar(QStatusBar):
    """Main status bar class for the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_status_bar()
    
    def init_status_bar(self):
        """Initialize the status bar with permanent widgets."""
        try:
            # Create permanent widgets
            self.create_permanent_widgets()
            
            # Set initial message
            self.showMessage("Ready")
            
        except Exception as e:
            logger.error(f"Error initializing status bar: {str(e)}")
    
    def create_permanent_widgets(self):
        """Create permanent widgets for the status bar."""
        try:
            # Create permanent message label
            self.message_label = QLabel()
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.addPermanentWidget(self.message_label)
            
            # Create theme label
            self.theme_label = QLabel()
            self.theme_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.addPermanentWidget(self.theme_label)
            
        except Exception as e:
            logger.error(f"Error creating permanent widgets: {str(e)}")
    
    def update_theme_label(self, theme_name):
        """
        Update the theme label with current theme name.
        
        Args:
            theme_name (str): Name of the current theme
        """
        try:
            self.theme_label.setText(f"Theme: {theme_name}")
        except Exception as e:
            logger.error(f"Error updating theme label: {str(e)}")
    
    def showMessage(self, message, timeout=0):
        """
        Show a message in the status bar.
        
        Args:
            message (str): Message to display
            timeout (int): Time in milliseconds before the message is cleared (0 for no timeout)
        """
        try:
            super().showMessage(message, timeout)
            self.message_label.setText(message)
        except Exception as e:
            logger.error(f"Error showing message: {str(e)}")
