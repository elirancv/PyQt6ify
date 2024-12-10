"""
Tests for Theme Manager module.
"""

from modules.themes.theme_manager import ThemeManager
from modules.config.config import Config

class ThemeManager:
    # ... existing methods ...

    def save_config(self, option):
        # implementation here
        pass

    def get_stylesheet(self, theme_name):
        # implementation here
        pass

def test_theme_manager_creation(qapp):
    """Test that ThemeManager initializes correctly."""
    config = Config()
    theme_manager = ThemeManager(qapp, config)

    # Validate that available themes are loaded
    themes = theme_manager.get_available_themes()
    assert len(themes) > 0
    assert 'light' in themes
    assert 'dark' in themes

def test_apply_theme(qapp):
    """Test applying a theme updates the application style."""
    config = Config()
    theme_manager = ThemeManager(qapp, config)

    # Apply light theme
    assert theme_manager.apply_theme('light')
    assert 'background-color: #ffffff;' in qapp.styleSheet()

    # Apply dark theme
    assert theme_manager.apply_theme('dark')
    assert 'background-color: #000000;' in qapp.styleSheet()

def test_invalid_theme(qapp):
    """Test applying an invalid theme."""
    config = Config()
    theme_manager = ThemeManager(qapp, config)

    result = theme_manager.apply_theme('nonexistent_theme')
    assert not result  # apply_theme should return False for invalid themes

def test_theme_persistence(qapp, tmpdir):
    """Test that the theme persists across sessions."""
    config_path = tmpdir.join("test_config.json")
    config = Config(config_path)
    theme_manager = ThemeManager(qapp, config)

    # Apply and persist dark theme
    theme_manager.apply_theme('dark')
    theme_manager.save_config(option='theme')  
    assert config.get('theme') == 'dark'

    # Reload ThemeManager and validate the theme is persisted
    new_theme_manager = ThemeManager(qapp, Config(config_path))
    assert new_theme_manager.get_current_theme()['name'] == 'dark'

def test_dynamic_theme_change(qapp):
    """Test that changing themes updates the UI dynamically."""
    config = Config()
    theme_manager = ThemeManager(qapp, config)

    # Apply light theme
    theme_manager.apply_theme('light')
    assert qapp.styleSheet() == theme_manager.get_stylesheet('light')

    # Change to dark theme dynamically
    theme_manager.apply_theme('dark')
    assert qapp.styleSheet() == theme_manager.get_stylesheet('dark')
