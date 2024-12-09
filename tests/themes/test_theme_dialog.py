"""
Test theme dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import QDialog
from modules.themes.theme_dialog import ThemeDialog
from modules.themes.theme_manager import ThemeManager
from modules.config.config import Config

@pytest.fixture
def theme_manager(qapp):
    """Create a theme manager instance for testing"""
    config = Config()
    return ThemeManager(qapp, config)

def test_theme_dialog_creation(qapp, theme_manager):
    """Test that theme dialog can be created"""
    dialog = ThemeDialog(theme_manager)
    assert isinstance(dialog, QDialog)
    assert dialog.windowTitle() == "Theme Selection"

def test_theme_dialog_list_themes(qapp, theme_manager):
    """Test that theme dialog lists available themes"""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    assert theme_list is not None
    assert theme_list.count() > 0
    
    # Check that each theme in the manager is listed
    theme_items = [theme_list.item(i).text() for i in range(theme_list.count())]
    for theme in theme_manager.get_themes():
        assert theme['name'] in theme_items

def test_theme_dialog_current_theme(qapp, theme_manager):
    """Test that current theme is selected in the dialog"""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Get current theme
    current_theme = theme_manager.get_current_theme()
    
    # Find the selected item in the list
    selected_items = theme_list.selectedItems()
    assert len(selected_items) == 1
    assert selected_items[0].text() == current_theme['name']

def test_theme_dialog_change_theme(qapp, theme_manager, monkeypatch):
    """Test changing theme through the dialog"""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Mock theme manager's apply_theme method
    applied_theme = None
    def mock_apply_theme(theme_name):
        nonlocal applied_theme
        applied_theme = theme_name
    monkeypatch.setattr(theme_manager, 'apply_theme', mock_apply_theme)
    
    # Select a different theme
    for i in range(theme_list.count()):
        item = theme_list.item(i)
        if item.text() != theme_manager.get_current_theme()['name']:
            theme_list.setCurrentItem(item)
            break
    
    # Simulate clicking OK
    dialog.accept()
    
    # Verify theme was changed
    assert applied_theme is not None
    assert applied_theme != theme_manager.get_current_theme()['name']

def test_theme_dialog_cancel(qapp, theme_manager, monkeypatch):
    """Test canceling theme change"""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Mock theme manager's apply_theme method
    theme_changed = False
    def mock_apply_theme(theme_name):
        nonlocal theme_changed
        theme_changed = True
    monkeypatch.setattr(theme_manager, 'apply_theme', mock_apply_theme)
    
    # Select a different theme
    for i in range(theme_list.count()):
        item = theme_list.item(i)
        if item.text() != theme_manager.get_current_theme()['name']:
            theme_list.setCurrentItem(item)
            break
    
    # Simulate clicking Cancel
    dialog.reject()
    
    # Verify theme was not changed
    assert not theme_changed
