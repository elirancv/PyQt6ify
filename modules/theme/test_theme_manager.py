"""
Unit tests for the ThemeManager class.
"""

import unittest
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from .theme_manager import ThemeManager
from config.app_config import Config

# Configure logging to use the centralized app.log
logger = logging.getLogger(__name__)

class TestThemeManager(unittest.TestCase):
    """Test cases for ThemeManager class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Create QApplication instance if it doesn't exist
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication([])
        
        # Create config instance
        cls.config = Config()
        logger.info("Test environment set up")
    
    def setUp(self):
        """Set up each test."""
        self.theme_manager = ThemeManager(self.app, self.config)
        self.theme_manager.apply_theme("light")
        logger.info("Reset to light theme")
    
    def test_theme_initialization(self):
        """Test theme manager initialization."""
        logger.info("Testing theme initialization")
        self.assertEqual(self.theme_manager.current_theme, "light")
        self.assertIn("light", self.theme_manager.get_available_themes())
        self.assertIn("dark", self.theme_manager.get_available_themes())
    
    def test_theme_change(self):
        """Test changing themes."""
        logger.info("Testing theme change")
        
        # Test changing to dark theme
        success = self.theme_manager.apply_theme("dark")
        self.assertTrue(success)
        self.assertEqual(self.theme_manager.current_theme, "dark")
        
        # Verify palette colors
        palette = self.app.palette()
        dark_theme = self.theme_manager.themes["dark"]
        
        logger.info("Verifying dark theme colors")
        self.assertEqual(
            palette.color(QPalette.ColorRole.Window).name(),
            QColor(dark_theme["window"]).name()
        )
    
    def test_invalid_theme(self):
        """Test applying non-existent theme."""
        logger.info("Testing invalid theme")
        success = self.theme_manager.apply_theme("nonexistent_theme")
        self.assertFalse(success)
        self.assertEqual(self.theme_manager.current_theme, "light")
    
    def test_theme_persistence(self):
        """Test theme persistence across changes."""
        logger.info("Testing theme persistence")
        
        # Change to dark theme
        success = self.theme_manager.apply_theme("dark")
        self.assertTrue(success)
        
        # Create new instance and verify theme persists
        new_manager = ThemeManager(self.app, self.config)
        self.assertEqual(new_manager.current_theme, "dark")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.app.quit()
        logger.info("ThemeManager test suite completed")

if __name__ == '__main__':
    unittest.main()
