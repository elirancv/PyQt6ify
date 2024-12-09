"""
PyTest configuration and fixtures
"""
import pytest
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """Create a Qt application instance for the entire test session"""
    app = QApplication([])
    yield app
    app.quit()
