"""
Test about dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import QMessageBox, QLabel
from modules.about import show_about_dialog
from modules.config.config import Config

def test_about_dialog_creation(qapp):
    """Test that about dialog can be created"""
    config = Config()
    dialog = show_about_dialog(config)
    assert isinstance(dialog, QMessageBox)
    assert dialog.windowTitle().startswith("About")

def test_about_dialog_content(qapp):
    """Test that about dialog shows correct information"""
    config = Config()
    dialog = show_about_dialog(config)
    
    # Get the dialog text
    text = dialog.text()
    
    # Check that config information is displayed
    about_info = config.about_info
    assert about_info['name'] in text
    assert about_info['version'] in text
    assert about_info['author'] in text
    assert about_info['description'] in text
    assert about_info['website'] in text

def test_about_dialog_close(qapp):
    """Test that about dialog can be closed"""
    config = Config()
    dialog = show_about_dialog(config)
    
    # Simulate clicking OK
    dialog.close()
    assert not dialog.isVisible()

def test_about_dialog_error_handling(qapp, monkeypatch):
    """Test error handling in about dialog"""
    config = Config()
    
    # Mock get method to raise an exception
    def mock_get(*args):
        raise ValueError("Test error")
    monkeypatch.setattr(config, 'get', mock_get)
    
    # Show dialog should return None on error
    dialog = show_about_dialog(config)
    assert dialog is None
