"""Test error handling functionality"""
import os
import time
from pathlib import Path
import unittest
from PyQt6.QtWidgets import QApplication
from loguru import logger
from modules.error_handling import setup_logging, show_error_dialog

class TestErrorHandling(unittest.TestCase):
    """Test error handling functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.app = QApplication([])
        cls.log_dir = Path('logs')
        cls.log_dir.mkdir(exist_ok=True)
        cls.log_file = cls.log_dir / 'test.log'

    def setUp(self):
        """Set up each test"""
        # Remove existing logger
        logger.remove()
        
        # Clear the log file before each test
        if self.log_file.exists():
            try:
                self.log_file.unlink()
            except PermissionError:
                pass  # Ignore if file is locked
        
        # Set up fresh logging
        setup_logging(self.log_file)

    def test_logging_setup(self):
        """Test that logging is set up correctly"""
        self.assertTrue(self.log_dir.exists())
        self.assertTrue(setup_logging(self.log_file))
        self.assertTrue(self.log_file.exists())

    def test_error_dialog(self):
        """Test that error dialog shows and logs correctly"""
        title = "Test Error"
        message = "Test error message"
        
        # Show error dialog
        show_error_dialog(title, message)
        
        # Give some time for the log to be written
        time.sleep(0.1)
        
        # Read the log file
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                self.assertIn(title, log_content)
                self.assertIn(message, log_content)
        else:
            self.fail("Log file was not created")

    def tearDown(self):
        """Clean up after each test"""
        # Remove existing logger
        logger.remove()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.app.quit()
        
        # Clean up log files
        if cls.log_file.exists():
            try:
                cls.log_file.unlink()
            except PermissionError:
                pass  # Ignore permission errors during cleanup
        
        if cls.log_dir.exists():
            try:
                cls.log_dir.rmdir()
            except (OSError, PermissionError):
                pass  # Ignore if directory is not empty or permission error

if __name__ == '__main__':
    unittest.main()
