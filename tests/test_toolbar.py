"""Test toolbar functionality"""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from modules.toolbar import create_toolbar

class TestToolBar(unittest.TestCase):
    """Test toolbar functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.app = QApplication([])
        cls.window = QMainWindow()
        
        # Create icons directory if it doesn't exist
        cls.icons_dir = Path('icons')
        cls.icons_dir.mkdir(exist_ok=True)
        
        # Create dummy icon files for testing
        cls.icon_files = {
            'new.png': 'new',
            'open.png': 'open',
            'save.png': 'save',
            'save_as.png': 'save_as'
        }
        for filename, _ in cls.icon_files.items():
            icon_path = cls.icons_dir / filename
            if not icon_path.exists():
                with open(icon_path, 'wb') as f:
                    # Write a minimal valid PNG file
                    f.write(bytes.fromhex('89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4890000000D4944415478DA63FCFF9F198C0003000C7F03FEE8E8E8E80000000049454E44AE426082'))

    def setUp(self):
        """Set up each test"""
        self.toolbar = create_toolbar(self.window)
        self.window.addToolBar(self.toolbar)

    def test_toolbar_creation(self):
        """Test that toolbar is created"""
        self.assertIsNotNone(self.toolbar)

    def test_toolbar_actions(self):
        """Test toolbar actions"""
        actions = [action.text() for action in self.toolbar.actions()]
        expected_actions = ['New', 'Open', 'Save', 'Save As']
        for action in expected_actions:
            self.assertIn(action, actions)

    def test_toolbar_icons(self):
        """Test that toolbar actions have icons"""
        actions = self.toolbar.actions()
        for action in actions:
            self.assertFalse(action.icon().isNull(), f"Icon missing for action: {action.text()}")

    def test_toolbar_tooltips(self):
        """Test toolbar tooltips"""
        actions = self.toolbar.actions()
        tooltips = {
            'New': 'Create a new file',
            'Open': 'Open an existing file',
            'Save': 'Save the current file',
            'Save As': 'Save the file with a new name'
        }
        for action in actions:
            expected_tooltip = tooltips.get(action.text())
            if expected_tooltip:
                self.assertEqual(action.toolTip(), expected_tooltip)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.window.close()
        cls.app.quit()
        
        # Clean up test icon files
        for filename in cls.icon_files:
            icon_path = cls.icons_dir / filename
            if icon_path.exists():
                try:
                    icon_path.unlink()
                except PermissionError:
                    pass  # Ignore permission errors during cleanup
        
        # Try to remove icons directory
        if cls.icons_dir.exists():
            try:
                cls.icons_dir.rmdir()
            except (OSError, PermissionError):
                pass  # Ignore if directory is not empty or permission error

if __name__ == '__main__':
    unittest.main()
