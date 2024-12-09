"""
PyTest configuration and fixtures for Qt testing
"""
import os
import sys
import pytest
import logging
import warnings
import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Suppress Qt-related warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

def pytest_configure(config):
    """Configure pytest for Qt testing."""
    if platform.system() == 'Windows':
        # Disable the Windows Error Reporting dialog
        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

@pytest.fixture(scope='session')
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

@pytest.fixture(autouse=True)
def cleanup_widgets(qapp, request):
    """Clean up widgets after each test."""
    def cleanup():
        try:
            for widget in qapp.topLevelWidgets():
                if widget.isVisible():
                    widget.hide()
                    widget.deleteLater()
            qapp.processEvents()
        except Exception:
            pass  # Ignore cleanup errors
            
    request.addfinalizer(cleanup)
    return qapp
