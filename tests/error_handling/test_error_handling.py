"""
Test module for error handling.
"""

from PyQt6.QtWidgets import QMessageBox
from modules.error_handling.error_handling import show_error_dialog

def test_show_error_dialog(qtbot):
    """Test showing error dialog."""
    result = show_error_dialog("Test Error", "This is a test error")
    assert isinstance(result, QMessageBox)

def test_show_error_dialog_with_title(qtbot):
    """Test showing error dialog with custom title."""
    result = show_error_dialog("Test Error", "This is a test error", "Custom Title")
    assert isinstance(result, QMessageBox)
    assert result.windowTitle() == "Custom Title"

def test_show_error_dialog_with_details(qtbot):
    """Test showing error dialog with details."""
    result = show_error_dialog(
        "Test Error",
        "This is a test error",
        details="Detailed error information"
    )
    assert isinstance(result, QMessageBox)

def test_show_error_dialog_with_exception(qtbot):
    """Test showing error dialog with exception."""
    try:
        raise ValueError("Test exception")
    except ValueError as e:
        result = show_error_dialog("Test Error", str(e))
        assert isinstance(result, QMessageBox)
