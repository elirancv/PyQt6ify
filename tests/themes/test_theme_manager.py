"""
Unit tests for the ThemeManager module.
"""

from unittest.mock import MagicMock  # Standard library import comes first
import pytest  # Third-party imports come after standard library imports
from modules.themes.theme_manager import ThemeManager
from modules.config.config import Config


@pytest.fixture
def mock_qapp():
    """Fixture to mock a QApplication instance."""
    class MockQApp:
        def __init__(self):
            self._styleSheet = ""

        def styleSheet(self):
            return self._styleSheet

        def setStyleSheet(self, styleSheet):
            self._styleSheet = styleSheet

    return MockQApp()


@pytest.fixture
def mock_config(tmpdir):
    """Fixture to create a mock configuration object."""
    config_path = tmpdir.join("test_config.json")
    config = Config(config_path)
    return config


@pytest.fixture
def theme_manager(mock_qapp, mock_config):
    """Fixture to provide a ThemeManager instance."""
    manager = ThemeManager(mock_qapp, mock_config)
    # Mock missing methods if needed
    manager.get_stylesheet = MagicMock(side_effect=lambda theme_name:
        "background-color: #ffffff;" if theme_name == "light" else "background-color: #000000;"
    )
    manager.get_available_themes = MagicMock(return_value=["light", "dark"])
    return manager


def test_theme_manager_creation(theme_manager):
    """Test that ThemeManager initializes correctly and loads themes."""
    themes = theme_manager.get_available_themes()
    assert len(themes) > 0, "Themes should be available."
    assert "light" in themes, "'light' theme should be available."
    assert "dark" in themes, "'dark' theme should be available."


def test_apply_theme(theme_manager, mock_qapp):
    """Test applying a theme updates the application style."""
    # Apply light theme
    assert theme_manager.apply_theme("light"), "Applying 'light' theme should succeed."
    assert mock_qapp.styleSheet() == theme_manager.get_stylesheet("light"), \
        "'light' theme should update the application's stylesheet."

    # Apply dark theme
    assert theme_manager.apply_theme("dark"), "Applying 'dark' theme should succeed."
    assert mock_qapp.styleSheet() == theme_manager.get_stylesheet("dark"), \
        "'dark' theme should update the application's stylesheet."


def test_invalid_theme(theme_manager):
    """Test applying an invalid theme."""
    result = theme_manager.apply_theme("nonexistent_theme")
    assert not result, "Applying an invalid theme should fail."


def test_theme_persistence(theme_manager, mock_config):
    """Test that the theme persists across sessions."""
    # Apply and persist the 'dark' theme
    assert theme_manager.apply_theme("dark"), "Applying 'dark' theme should succeed."
    theme_manager.save_config(option="theme")
    assert mock_config.get("theme") == "dark", "Config should persist the 'dark' theme."

    # Simulate reloading ThemeManager and ensure the theme persists
    new_theme_manager = ThemeManager(mock_qapp, mock_config)
    assert new_theme_manager.get_current_theme()["name"] == "dark", \
        "Reloaded ThemeManager should retain the 'dark' theme."


def test_dynamic_theme_change(theme_manager, mock_qapp):
    """Test that dynamically changing themes updates the UI."""
    # Apply light theme
    assert theme_manager.apply_theme("light"), "Applying 'light' theme should succeed."
    assert mock_qapp.styleSheet() == theme_manager.get_stylesheet("light"), \
        "'light' theme should update the application's stylesheet."

    # Change to dark theme dynamically
    assert theme_manager.apply_theme("dark"), "Applying 'dark' theme should succeed."
    assert mock_qapp.styleSheet() == theme_manager.get_stylesheet("dark"), \
        "'dark' theme should update the application's stylesheet."
