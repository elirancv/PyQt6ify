"""
Test error handling module functionality.
"""

import pytest
from PyQt6.QtWidgets import QMessageBox
from modules.error_handling.error_handling import show_error_dialog

def test_show_error_dialog(qapp, monkeypatch):
    """Test that error dialog is shown with correct title and message"""
    # Mock QMessageBox.critical to capture the dialog parameters
    dialog_params = {}
    def mock_critical(parent, title, message, buttons, defaultButton):
        dialog_params['title'] = title
        dialog_params['message'] = message
        return QMessageBox.StandardButton.Ok
    
    monkeypatch.setattr(QMessageBox, 'critical', mock_critical)
    
    # Show error dialog
    show_error_dialog("Test Error", "This is a test error message")
    
    # Verify dialog parameters
    assert dialog_params['title'] == "Test Error"
    assert dialog_params['message'] == "This is a test error message"

def test_show_error_dialog_with_exception(qapp, monkeypatch):
    """Test that error dialog can show exception details"""
    # Mock QMessageBox.critical
    dialog_params = {}
    def mock_critical(parent, title, message, buttons, defaultButton):
        dialog_params['title'] = title
        dialog_params['message'] = message
        return QMessageBox.StandardButton.Ok
    
    monkeypatch.setattr(QMessageBox, 'critical', mock_critical)
    
    # Create an exception
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        show_error_dialog("Error", str(e))
    
    # Verify dialog parameters
    assert dialog_params['title'] == "Error"
    assert dialog_params['message'] == "Test exception"
