"""
Tests for Toolbar module
"""
import pytest
from PyQt6.QtWidgets import QToolBar, QMainWindow
from modules.toolbar.toolbar import ToolBar
from modules.config.config import Config

def test_toolbar_creation(qapp):
    """Test that ToolBar can be created"""
    config = Config()
    window = QMainWindow()
    toolbar = ToolBar(window)
    window.addToolBar(toolbar)
    
    assert isinstance(toolbar, QToolBar)
    
    # Check that essential actions exist
    action_texts = [action.text() for action in toolbar.actions()]
    assert any('New' in text for text in action_texts)
    assert any('Open' in text for text in action_texts)
    assert any('Save' in text for text in action_texts)
