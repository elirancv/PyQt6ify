"""
Tests for the theme manager functionality.
"""

import os
import json
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from modules.theme.theme_manager import ThemeManager
from config.app_config import Config

@pytest.fixture
def theme_manager(qtbot, tmp_path):
    """Create a theme manager instance for testing."""
    app = QApplication.instance() or QApplication([])
    config = Config()
    
    # Override config directory to use a temporary directory
    config.config_dir = str(tmp_path)
    
    manager = ThemeManager(app, config)
    return manager

def test_theme_manager_initialization(theme_manager):
    """Test theme manager initialization."""
    assert theme_manager.current_theme == "light"
    assert isinstance(theme_manager.themes, dict)
    assert "light" in theme_manager.themes
    assert "dark" in theme_manager.themes

def test_switch_theme(theme_manager):
    """Test switching between themes."""
    # Start with light theme
    assert theme_manager.current_theme == "light"
    
    # Switch to dark theme
    theme_manager.switch_theme("dark")
    assert theme_manager.current_theme == "dark"
    
    # Switch back to light theme
    theme_manager.switch_theme("light")
    assert theme_manager.current_theme == "light"

def test_invalid_theme(theme_manager):
    """Test switching to an invalid theme."""
    original_theme = theme_manager.current_theme
    theme_manager.switch_theme("nonexistent_theme")
    # Should keep the original theme when invalid theme is requested
    assert theme_manager.current_theme == original_theme

def test_apply_theme(theme_manager):
    """Test applying theme colors to application palette."""
    theme_manager.switch_theme("dark")
    palette = theme_manager.app.palette()
    
    # Check if some key colors are applied correctly
    dark_theme = theme_manager.themes["dark"]
    assert palette.color(QPalette.ColorRole.Window).name() == dark_theme["window"]
    assert palette.color(QPalette.ColorRole.WindowText).name() == dark_theme["windowText"]

def test_save_and_load_custom_theme(theme_manager, tmp_path):
    """Test saving and loading custom themes."""
    custom_theme = {
        "name": "custom",
        "colors": {
            "window": "#123456",
            "windowText": "#ffffff",
            "base": "#123456",
            "text": "#ffffff"
        }
    }
    
    # Save custom theme
    theme_file = tmp_path / "custom_theme.json"
    with open(theme_file, "w") as f:
        json.dump(custom_theme, f)
    
    # Load custom theme
    theme_manager.load_theme_from_file(str(theme_file))
    assert "custom" in theme_manager.themes
    assert theme_manager.themes["custom"]["window"] == "#123456"

def test_theme_persistence(theme_manager):
    """Test that theme selection persists."""
    # Switch to dark theme
    theme_manager.switch_theme("dark")
    assert theme_manager.current_theme == "dark"
    
    # Create new theme manager instance
    new_manager = ThemeManager(theme_manager.app, theme_manager.config)
    # Should load the previously selected theme
    assert new_manager.current_theme == "dark"

def test_theme_colors_validation(theme_manager):
    """Test theme color validation."""
    valid_color = "#123456"
    invalid_color = "not_a_color"
    
    assert theme_manager._is_valid_color(valid_color)
    assert not theme_manager._is_valid_color(invalid_color)

def test_theme_export(theme_manager, tmp_path):
    """Test theme export functionality."""
    export_path = tmp_path / "exported_theme.json"
    theme_manager.export_theme("light", str(export_path))
    
    assert export_path.exists()
    with open(export_path) as f:
        exported_theme = json.load(f)
    
    assert exported_theme["name"] == "light"
    assert exported_theme["colors"] == theme_manager.themes["light"]
