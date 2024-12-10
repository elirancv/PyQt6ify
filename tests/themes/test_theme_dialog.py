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
    """Fixture to create a ThemeManager instance for testing."""
    config = Config()
    return ThemeManager(qapp, config)


def test_theme_dialog_creation(qapp, theme_manager):
    """Test that the ThemeDialog is created successfully."""
    dialog = ThemeDialog(theme_manager)
    assert isinstance(dialog, QDialog)
    assert dialog.windowTitle() == "Theme Selection"


def test_theme_dialog_list_themes(qapp, theme_manager):
    """Test that the dialog lists all available themes."""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)
    assert theme_list is not None

    # Check themes in the list
    themes = theme_manager.get_available_themes()
    assert theme_list.count() == len(themes)

    listed_themes = [theme_list.item(i).text() for i in range(theme_list.count())]
    for theme in themes:
        assert theme in listed_themes


def test_theme_dialog_current_theme(qapp, theme_manager):
    """Test that the currently selected theme is highlighted."""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)

    current_theme = theme_manager.get_current_theme()

    selected_items = theme_list.selectedItems()
    assert len(selected_items) == 1
    assert selected_items[0].text() == current_theme['name']


def test_theme_dialog_change_theme(qapp, theme_manager, monkeypatch):
    """Test changing the theme through the dialog."""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)

    # Mock apply_theme method
    apply_called = {'theme': None}

    def mock_apply_theme(theme_name, preview_only=False):
        if not preview_only:
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

    # Click Apply button
    apply_button = dialog.findChild(QPushButton, "Apply")
    apply_button.click()

    # Validate that the theme was applied
    assert apply_called['theme'] == new_theme
    assert not dialog.isVisible()


def test_theme_dialog_cancel(qapp, theme_manager, monkeypatch):
    """Test canceling a theme change."""
    dialog = ThemeDialog(theme_manager)
    theme_list = dialog.findChild(QListWidget)

    # Mock apply_theme method
    apply_called = {'theme': None}
    original_theme = theme_manager.get_current_theme()['name']

    def mock_apply_theme(theme_name, preview_only=False):
        if not preview_only:
            apply_called['theme'] = theme_name
        return True

    monkeypatch.setattr(theme_manager, 'apply_theme', mock_apply_theme)

    # Select a different theme
    available_themes = theme_manager.get_available_themes()
    new_theme = next(theme for theme in available_themes if theme != original_theme)

    for i in range(theme_list.count()):
        if theme_list.item(i).text() == new_theme:
            theme_list.setCurrentRow(i)
            break

    # Click Cancel button
    cancel_button = dialog.findChild(QPushButton, "Cancel")
    cancel_button.click()

    # Validate that the theme was reverted to the original
    assert apply_called['theme'] is None  # No theme was applied
    assert theme_manager.get_current_theme()['name'] == original_theme
    assert not dialog.isVisible()
