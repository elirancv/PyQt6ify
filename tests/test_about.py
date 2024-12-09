"""
Test suite for About dialog functionality
"""
import unittest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication, QMainWindow
from modules.about import show_about_dialog

class TestAboutDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create the application instance"""
        cls.app = QApplication([])
        cls.window = QMainWindow()

    def setUp(self):
        """Set up mock config for each test"""
        self.mock_config = MagicMock()
        self.mock_config.get_about_info.side_effect = lambda key: {
            'name': 'PyQt6ify Pro',
            'version': '1.0.0',
            'author': 'PyQt6ify Team',
            'website': 'https://github.com/PyQt6ify',
            'icon': 'resources/icons/app_icon.png'
        }[key]

    def test_about_dialog(self):
        """Test that about dialog shows correct information"""
        show_about_dialog(self.window, self.mock_config)
        
        # Verify that config was queried for all required information
        expected_calls = ['name', 'version', 'author', 'website', 'icon']
        actual_calls = [call[0][0] for call in self.mock_config.get_about_info.call_args_list]
        self.assertEqual(sorted(expected_calls), sorted(actual_calls))

    @classmethod
    def tearDownClass(cls):
        """Clean up the application instance"""
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
