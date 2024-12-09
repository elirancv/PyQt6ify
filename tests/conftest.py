"""
PyTest configuration and fixtures for Qt testing
"""
import os
import pytest
from PyQt6.QtWidgets import QApplication

# Use minimal platform for testing
os.environ['QT_QPA_PLATFORM'] = 'minimal'

@pytest.fixture(scope='session')
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([''])
    
    yield app
    
    # Clean up at the end of the session
    for widget in app.topLevelWidgets():
        widget.hide()
        widget.deleteLater()
    app.processEvents()
