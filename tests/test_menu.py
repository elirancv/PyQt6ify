"""Test menu functionality"""
import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu
from modules.menu import create_menu_bar

class TestMenu(unittest.TestCase):
    """Test menu functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.app = QApplication([])
        cls.window = QMainWindow()

    def setUp(self):
        """Set up each test"""
        self.menu_bar = create_menu_bar(self.window)
        self.window.setMenuBar(self.menu_bar)

    def test_menu_creation(self):
        """Test that menu bar is created"""
        self.assertIsNotNone(self.menu_bar)

    def test_menu_structure(self):
        """Test menu structure"""
        menus = [menu.title() for menu in self.menu_bar.findChildren(QMenu)]
        expected_titles = ['&File', '&Edit', '&View', '&Help']
        for title in expected_titles:
            self.assertIn(title, menus)

    def test_file_menu_actions(self):
        """Test file menu actions"""
        file_menu = None
        for menu in self.menu_bar.findChildren(QMenu):
            if menu.title() == '&File':
                file_menu = menu
                break
        
        self.assertIsNotNone(file_menu)
        actions = [action.text() for action in file_menu.actions()]
        expected_actions = ['&New', '&Open...', '&Save', 'Save &As...', 'E&xit']
        for action in expected_actions:
            self.assertIn(action, actions)

    def test_help_menu_actions(self):
        """Test help menu actions"""
        help_menu = None
        for menu in self.menu_bar.findChildren(QMenu):
            if menu.title() == '&Help':
                help_menu = menu
                break
        
        self.assertIsNotNone(help_menu)
        actions = [action.text() for action in help_menu.actions()]
        expected_actions = ['&About']
        for action in expected_actions:
            self.assertIn(action, actions)

    @patch('modules.menu.show_theme_dialog')
    def test_theme_action(self, mock_show_theme):
        """Test theme action in view menu"""
        view_menu = None
        for menu in self.menu_bar.findChildren(QMenu):
            if menu.title() == '&View':
                view_menu = menu
                break
        
        self.assertIsNotNone(view_menu)
        theme_action = None
        for action in view_menu.actions():
            if 'Theme' in action.text():
                theme_action = action
                break
        
        self.assertIsNotNone(theme_action)
        theme_action.trigger()
        mock_show_theme.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.window.close()
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
