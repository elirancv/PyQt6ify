"""
PyQt6ify Pro - Main Application Entry Point
"""

import sys
import os
from loguru import logger
from PyQt6.QtWidgets import QApplication

from modules.config.config import Config
from modules.core.main_window import MainWindow

def setup_logging():
    """Configure logging settings."""
    logger.add("logs/debug.log", 
               rotation="500 MB",
               retention="10 days",
               level="DEBUG")

def main():
    """Main application entry point."""
    try:
        # Initialize logging
        setup_logging()
        logger.info("Starting PyQt6ify Pro")
        
        # Load configuration first
        config = Config()
        config.load_config()
        
        # Create application instance with dark theme style
        os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'  # Use Fusion style which works well with custom themes
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = MainWindow(config)
        window.show()  # Make sure to show the window
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
