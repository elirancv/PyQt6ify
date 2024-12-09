"""
Test suite for theme manager functionality.
"""

import sys
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from theme_manager import ThemeManager
import logging

class TestThemeManager(unittest.TestCase):
    """Test cases for ThemeManager class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Configure logging for tests
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s | %(levelname)s | TEST | %(message)s',
            handlers=[
                logging.FileHandler('theme_manager_test.log'),
                logging.StreamHandler()
            ]
        )
        
        # Create QApplication instance if not exists
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
        
        cls.theme_manager = ThemeManager()
        logging.info("Test environment set up")
    
    def setUp(self):
        """Set up each test."""
        # Reset to light theme before each test
        self.theme_manager.apply_theme("light")
        logging.info("Reset to light theme")
    
    def test_theme_initialization(self):
        """Test theme manager initialization."""
        logging.info("Testing theme initialization")
        self.assertEqual(self.theme_manager.get_current_theme(), "light")
        self.assertIn("light", self.theme_manager.get_available_themes())
        self.assertIn("dark", self.theme_manager.get_available_themes())
    
    def test_theme_change(self):
        """Test changing themes."""
        logging.info("Testing theme change")
        
        # Test changing to dark theme
        success = self.theme_manager.apply_theme("dark")
        self.assertTrue(success)
        self.assertEqual(self.theme_manager.get_current_theme(), "dark")
        
        # Verify palette colors
        palette = QApplication.instance().palette()
        dark_theme = self.theme_manager.themes["dark"]
        
        logging.info("Verifying dark theme colors")
        self.assertEqual(
            palette.color(QPalette.ColorRole.Window).name(),
            QColor(dark_theme["window"]).name()
        )
        self.assertEqual(
            palette.color(QPalette.ColorRole.WindowText).name(),
            QColor(dark_theme["windowText"]).name()
        )
    
    def test_invalid_theme(self):
        """Test applying non-existent theme."""
        logging.info("Testing invalid theme")
        success = self.theme_manager.apply_theme("nonexistent_theme")
        self.assertFalse(success)
        self.assertEqual(self.theme_manager.get_current_theme(), "light")
    
    def test_theme_persistence(self):
        """Test theme persistence across changes."""
        logging.info("Testing theme persistence")
        
        # Change to dark theme
        self.theme_manager.apply_theme("dark")
        self.assertEqual(self.theme_manager.get_current_theme(), "dark")
        
        # Try invalid theme (should fail)
        self.theme_manager.apply_theme("invalid")
        # Should still be dark
        self.assertEqual(self.theme_manager.get_current_theme(), "dark")
        
        # Change back to light
        self.theme_manager.apply_theme("light")
        self.assertEqual(self.theme_manager.get_current_theme(), "light")

if __name__ == '__main__':
    unittest.main()
