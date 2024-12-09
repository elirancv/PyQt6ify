"""
Tests for Theme Manager module
"""
import pytest
from modules.themes.theme_manager import ThemeManager
from modules.config.config import Config

def test_theme_manager_creation(qapp):
    """Test that ThemeManager can be created"""
    config = Config()
    theme_manager = ThemeManager(qapp, config)
    
    # Check that theme manager loads themes correctly
    themes = theme_manager.get_available_themes()
    assert len(themes) > 0
    assert 'light' in themes
    assert 'dark' in themes
    
    # Test applying theme
    theme_manager.apply_theme('light')
    assert theme_manager.get_current_theme() == 'light'
