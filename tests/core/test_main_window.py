"""
Tests for MainWindow class
"""
import pytest
from PyQt6.QtWidgets import QMainWindow
from modules.core.main_window import MainWindow
from modules.config.config import Config

def test_main_window_creation(qapp):
    """Test that MainWindow can be created"""
    config = Config()
    config.set('Application', 'Name', 'PyQt6ify Pro')
    config.set('Application', 'Version', '1.0.0')
    window = MainWindow(config)
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "PyQt6ify Pro 1.0.0"
