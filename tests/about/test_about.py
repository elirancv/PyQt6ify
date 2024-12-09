"""
Test about dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import QMessageBox, QLabel
from PyQt6.QtCore import Qt
from modules.about import show_about_dialog
from modules.config.config import Config

@pytest.mark.timeout(5)  # Add timeout to prevent hanging
def test_about_dialog_creation(qtbot):
    """Test that about dialog can be created"""
    print("Starting test_about_dialog_creation")
    config = Config()
    print("Config created")
    dialog = show_about_dialog(config, test_mode=True)
    print("Dialog created")
    qtbot.addWidget(dialog)
    
    # Show dialog manually for testing
    dialog.show()
    qtbot.wait(100)
    
    assert isinstance(dialog, QMessageBox)
    assert dialog.windowTitle().startswith("About")
    
    # Ensure dialog is closed
    dialog.close()
    qtbot.wait(100)
    print("Test completed")

@pytest.mark.timeout(5)
def test_about_dialog_content(qtbot):
    """Test that about dialog shows correct information"""
    config = Config()
    dialog = show_about_dialog(config, test_mode=True)
    qtbot.addWidget(dialog)
    dialog.show()
    qtbot.wait(100)
    
    # Get the dialog text
    text = dialog.text()
    
    # Check that config information is displayed
    about_info = config.about_info
    assert about_info['name'] in text
    assert about_info['version'] in text
    assert about_info['author'] in text
    assert about_info['description'] in text
    assert about_info['website'] in text
    
    dialog.close()
    qtbot.wait(100)

@pytest.mark.timeout(5)
def test_about_dialog_close(qtbot):
    """Test that about dialog can be closed"""
    config = Config()
    dialog = show_about_dialog(config, test_mode=True)
    qtbot.addWidget(dialog)
    dialog.show()
    qtbot.wait(100)
    
    # Simulate clicking OK
    dialog.close()
    qtbot.wait(100)
    assert not dialog.isVisible()

@pytest.mark.timeout(5)
def test_about_dialog_error_handling(qtbot, monkeypatch):
    """Test error handling in about dialog"""
    config = Config()
    
    # Mock get method to raise an exception
    def mock_get(*args, **kwargs):
        raise ValueError("Test error")
    monkeypatch.setattr(config, 'get', mock_get)
    
    # Show dialog should return None on error
    dialog = show_about_dialog(config, test_mode=True)
    assert dialog is None
