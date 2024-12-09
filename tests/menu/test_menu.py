"""
Tests for Menu module
"""
import pytest
from PyQt6.QtWidgets import QMenuBar, QMainWindow, QMenu, QToolBar, QStatusBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from modules.menu.menu import MenuBar
from modules.config.config import Config
import configparser

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
    assert any('Edit' in title for title in menu_titles)
    assert any('View' in title for title in menu_titles)
    assert any('Help' in title for title in menu_titles)

def test_menu_actions(qapp):
    """Test menu actions"""
    window = QMainWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Test File menu actions
    file_menu = next(m for m in menu.findChildren(QMenu) if 'File' in m.title())
    actions = file_menu.actions()
    action_texts = [a.text() for a in actions]
    
    assert any('&New' in text for text in action_texts)
    assert any('&Open' in text for text in action_texts)
    assert any('&Save' in text for text in action_texts)
    assert any('E&xit' in text for text in action_texts)
    
    # Test Edit menu actions
    edit_menu = next(m for m in menu.findChildren(QMenu) if 'Edit' in m.title())
    actions = edit_menu.actions()
    action_texts = [a.text() for a in actions]
    
    assert any('Cu&t' in text for text in action_texts)
    assert any('&Copy' in text for text in action_texts)
    assert any('&Paste' in text for text in action_texts)

def test_menu_shortcuts(qapp):
    """Test menu shortcuts"""
    window = QMainWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Get all actions
    actions = menu.findChildren(QAction)
    shortcuts = {a.text(): a.shortcut() for a in actions if a.shortcut()}
    
    # Test common shortcuts
    assert shortcuts.get('&New') == 'Ctrl+N'
    assert shortcuts.get('&Open...') == 'Ctrl+O'
    assert shortcuts.get('&Save') == 'Ctrl+S'
    assert shortcuts.get('Cu&t') == 'Ctrl+X'
    assert shortcuts.get('&Copy') == 'Ctrl+C'
    assert shortcuts.get('&Paste') == 'Ctrl+V'

def test_menu_icons(qapp):
    """Test menu icons"""
    window = QMainWindow()
    menu = MenuBar(window)
    
    # Test icon loading for non-existent icon
    icon = menu.get_icon('non_existent.png')
    assert icon.isNull()  # Icon should be null when file doesn't exist
    
    # Test with actual icons
    save_action = next(a for a in menu.findChildren(QAction) if 'Save' in a.text())
    assert not save_action.icon().isNull()  # Save action should have an icon

def test_view_menu(qapp):
    """Test View menu"""
    window = QMainWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Test View menu actions
    view_menu = next(m for m in menu.findChildren(QMenu) if 'View' in m.title())
    actions = view_menu.actions()
    action_texts = [a.text() for a in actions]
    
    assert any('&Toolbar' in text for text in action_texts)
    assert any('&Status Bar' in text for text in action_texts)

def test_help_menu(qapp):
    """Test Help menu"""
    window = QMainWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Test Help menu actions
    help_menu = next(m for m in menu.findChildren(QMenu) if 'Help' in m.title())
    actions = help_menu.actions()
    action_texts = [a.text() for a in actions]
    
    assert any('&About' in text for text in action_texts)

def test_menu_callbacks(qapp):
    """Test menu action callbacks"""
    # Create a parent window with tracking
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.close_called = False
            self.tool_bar = None
            self.status_bar = None
            
            # Mock config
            config = configparser.ConfigParser()
            config.add_section('Modules')
            config.set('Modules', 'toolbar_visible', 'true')
            config.set('Modules', 'statusbar_visible', 'true')
            
            def save_config(self):
                if not self.config.has_section('Modules'):
                    self.config.add_section('Modules')
                if hasattr(self.parent, 'tool_bar'):
                    self.config.set('Modules', 'toolbar_visible', str(self.parent.tool_bar.isVisible()).lower())
                if hasattr(self.parent, 'status_bar'):
                    self.config.set('Modules', 'statusbar_visible', str(self.parent.status_bar.isVisible()).lower())
            
            self.config = type('Config', (), {
                'config': config,
                'save_config': save_config,
                'parent': self
            })()
        
        def close(self):
            self.close_called = True
    
    window = TestWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Test Exit action
    file_menu = next(m for m in menu.findChildren(QMenu) if 'File' in m.title())
    exit_action = next(a for a in file_menu.actions() if 'E&xit' in a.text())
    exit_action.trigger()
    
    assert window.close_called
    
    # Test View menu callbacks
    view_menu = next(m for m in menu.findChildren(QMenu) if 'View' in m.title())
    toolbar_action = next(a for a in view_menu.actions() if '&Toolbar' in a.text())
    statusbar_action = next(a for a in view_menu.actions() if '&Status Bar' in a.text())
    
    # Initial state
    assert toolbar_action.isChecked()
    assert statusbar_action.isChecked()
    
    # Create toolbar and status bar for testing
    window.tool_bar = QToolBar()
    window.status_bar = QStatusBar()
    window.tool_bar.setVisible(True)
    window.status_bar.setVisible(True)
    
    # Toggle toolbar
    toolbar_action.trigger()
    assert not toolbar_action.isChecked()
    assert not window.tool_bar.isVisible()
    assert window.config.config.get('Modules', 'toolbar_visible') == 'false'
    
    # Toggle status bar
    statusbar_action.trigger()
    assert not statusbar_action.isChecked()
    assert not window.status_bar.isVisible()
    assert window.config.config.get('Modules', 'statusbar_visible') == 'false'

def test_menu_callbacks_no_modules_section(qapp):
    """Test menu callbacks when config has no Modules section"""
    # Create a parent window with tracking
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.close_called = False
            self.tool_bar = None
            self.status_bar = None
            
            # Mock config without Modules section
            config = configparser.ConfigParser()
            
            def save_config(self):
                if not self.config.has_section('Modules'):
                    self.config.add_section('Modules')
                if hasattr(self.parent, 'tool_bar'):
                    self.config.set('Modules', 'toolbar_visible', str(self.parent.tool_bar.isVisible()).lower())
                if hasattr(self.parent, 'status_bar'):
                    self.config.set('Modules', 'statusbar_visible', str(self.parent.status_bar.isVisible()).lower())
            
            self.config = type('Config', (), {
                'config': config,
                'save_config': save_config,
                'parent': self
            })()
        
        def close(self):
            self.close_called = True
    
    window = TestWindow()
    menu = MenuBar(window)
    window.setMenuBar(menu)
    
    # Create toolbar and status bar for testing
    window.tool_bar = QToolBar()
    window.status_bar = QStatusBar()
    window.tool_bar.setVisible(True)
    window.status_bar.setVisible(True)
    
    # Test View menu callbacks
    view_menu = next(m for m in menu.findChildren(QMenu) if 'View' in m.title())
    toolbar_action = next(a for a in view_menu.actions() if '&Toolbar' in a.text())
    statusbar_action = next(a for a in view_menu.actions() if '&Status Bar' in a.text())
    
    # Initial state
    assert toolbar_action.isChecked()
    assert statusbar_action.isChecked()
    
    # Toggle toolbar
    toolbar_action.trigger()
    assert not toolbar_action.isChecked()
    assert not window.tool_bar.isVisible()
    assert window.config.config.get('Modules', 'toolbar_visible') == 'false'
    
    # Toggle status bar
    statusbar_action.trigger()
    assert not statusbar_action.isChecked()
    assert not window.status_bar.isVisible()
    assert window.config.config.get('Modules', 'statusbar_visible') == 'false'
