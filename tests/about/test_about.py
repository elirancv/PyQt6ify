"""
Test about dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import QDialog, QLabel
from modules.about import show_about_dialog
from modules.config.config import Config

def test_about_dialog_creation(qapp):
    """Test that about dialog can be created"""
    config = Config()
    dialog = show_about_dialog(config)
    assert isinstance(dialog, QDialog)
    assert dialog.windowTitle() == f"About {config.get('Application', 'Name')}"

def test_about_dialog_content(qapp):
    """Test that about dialog shows correct information"""
    config = Config()
    dialog = show_about_dialog(config)
    
    # Find all labels in the dialog
    labels = dialog.findChildren(QLabel)
    label_texts = [label.text() for label in labels]
    
    # Check that config information is displayed
    assert any(config.get('Application', 'Name') in text for text in label_texts)
    assert any(config.get('Application', 'Version') in text for text in label_texts)
    assert any(config.get('About', 'Author') in text for text in label_texts)
    assert any(config.get('About', 'Description') in text for text in label_texts)
    assert any(config.get('About', 'Website') in text for text in label_texts)

def test_about_dialog_close(qapp):
    """Test that about dialog can be closed"""
    config = Config()
    dialog = show_about_dialog(config)
    
    # Simulate clicking OK
    assert dialog.close()
    assert not dialog.isVisible()
