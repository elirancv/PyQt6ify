"""
Test theme dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import QDialog, QListWidget, QPushButton
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
    
    # Check that themes are loaded
    themes = theme_manager.get_available_themes()
    assert theme_list.count() == len(themes)
    
    # Check that each theme is listed
    theme_items = [theme_list.item(i).text() for i in range(theme_list.count())]
    for theme in themes:
        assert theme in theme_items

def test_theme_dialog_current_theme(qapp, theme_manager):
    """Test that current theme is selected in the dialog"""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Get current theme
    current_theme = theme_manager.get_current_theme()
    
    # Check that current theme is selected
    selected_items = theme_list.selectedItems()
    assert len(selected_items) == 1
    assert selected_items[0].text() == current_theme['name']

def test_theme_dialog_change_theme(qapp, theme_manager, monkeypatch):
    """Test changing theme through the dialog"""
    # Create dialog
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Mock theme manager's apply_theme method
    apply_called = {'theme': None}
    def mock_apply_theme(theme_name):
        apply_called['theme'] = theme_name
        return True
    monkeypatch.setattr(theme_manager, 'apply_theme', mock_apply_theme)
    
    # Select a different theme
    available_themes = theme_manager.get_available_themes()
    current_theme = theme_manager.get_current_theme()['name']
    new_theme = next(theme for theme in available_themes if theme != current_theme)
    
    for i in range(theme_list.count()):
        if theme_list.item(i).text() == new_theme:
            theme_list.setCurrentRow(i)
            break
    
    # Click apply button
    apply_button = dialog.findChild(QPushButton, "")
    apply_button.click()
    
    # Verify theme was changed
    assert apply_called['theme'] == new_theme
    assert not dialog.isVisible()

def test_theme_dialog_cancel(qapp, theme_manager, monkeypatch):
    """Test canceling theme change"""
    # Create dialog
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    
    # Mock theme manager's apply_theme method
    apply_called = {'theme': None}
    def mock_apply_theme(theme_name):
        apply_called['theme'] = theme_name
        return True
    monkeypatch.setattr(theme_manager, 'apply_theme', mock_apply_theme)
    
    # Select a different theme
    available_themes = theme_manager.get_available_themes()
    current_theme = theme_manager.get_current_theme()['name']
    new_theme = next(theme for theme in available_themes if theme != current_theme)
    
    for i in range(theme_list.count()):
        if theme_list.item(i).text() == new_theme:
            theme_list.setCurrentRow(i)
            break
    
    # Find and click cancel button
    buttons = dialog.findChildren(QPushButton)
    cancel_button = next(button for button in buttons if button.text() == "Cancel")
    cancel_button.click()
    
    # Verify theme was not changed
    assert apply_called['theme'] is None
    assert not dialog.isVisible()
