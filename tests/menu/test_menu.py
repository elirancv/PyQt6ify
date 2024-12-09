"""
Tests for Menu module
"""
import pytest
from PyQt6.QtWidgets import QMenuBar, QMainWindow, QMenu
from modules.menu.menu import MenuBar
from modules.config.config import Config

def test_menu_creation(qapp):
    """Test that MenuBar can be created"""
    config = Config()
    window = QMainWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    assert isinstance(menu, QMenuBar)
    
    # Check that essential menus exist
    menus = menu.findChildren(QMenu)
    menu_titles = [menu.title() for menu in menus]
    assert any('File' in title for title in menu_titles)
    assert any('Help' in title for title in menu_titles)
