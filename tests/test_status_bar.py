"""
Test suite for Status Bar functionality
"""
import unittest
from PyQt6.QtWidgets import QApplication, QMainWindow
from modules.status_bar import StatusBar

class TestStatusBar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create the application instance"""
        cls.app = QApplication([])
        cls.main_window = QMainWindow()

    def setUp(self):
        """Create a fresh status bar for each test"""
        self.status_bar = StatusBar(self.main_window)

    def test_status_bar_creation(self):
        """Test that the status bar is created correctly"""
        self.assertIsNotNone(self.status_bar)

    def test_status_message(self):
        """Test setting and getting status messages"""
        test_message = "Test Status Message"
        self.status_bar.showMessage(test_message)
        self.assertEqual(self.status_bar.currentMessage(), test_message)

    def test_temporary_message(self):
        """Test temporary message display"""
        permanent_msg = "Permanent Message"
        temp_msg = "Temporary Message"
        timeout = 100  # 100ms
        
        self.status_bar.showMessage(permanent_msg)
        self.status_bar.showMessage(temp_msg, timeout)
        self.assertEqual(self.status_bar.currentMessage(), temp_msg)

    @classmethod
    def tearDownClass(cls):
        """Clean up the application instance"""
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
