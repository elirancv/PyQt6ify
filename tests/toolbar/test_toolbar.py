"""Test module for toolbar."""
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction
from modules.toolbar.toolbar import ToolBar

def test_toolbar_creation(qtbot):
    """Test creating a toolbar."""
    toolbar = ToolBar()
    assert isinstance(toolbar, QToolBar)

def test_toolbar_actions(qtbot):
    """Test toolbar actions."""
    toolbar = ToolBar()
    action = toolbar.addAction("Test")
    assert isinstance(action, QAction)

def test_toolbar_visibility(qtbot):
    """Test toolbar visibility."""
    toolbar = ToolBar()
    assert toolbar.isVisible()
    toolbar.hide()
    assert not toolbar.isVisible()
    toolbar.show()
    assert toolbar.isVisible()
