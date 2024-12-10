"""
Tests for Menu module
"""
from PyQt6.QtWidgets import QMenuBar, QMainWindow, QMenu, QToolBar, QStatusBar
from PyQt6.QtGui import QAction
from modules.menu.menu import MenuBar

def test_menu_creation(qapp):
    """Test that MenuBar can be created"""
    menubar = MenuBar()
    assert isinstance(menubar, QMenuBar)

def test_menu_actions(qapp):
    """Test menu actions"""
    menubar = MenuBar()
    file_menu = menubar.addMenu("File")
    action = file_menu.addAction("Test")
    assert isinstance(action, QAction)

def test_menu_shortcuts(qapp):
    """Test menu shortcuts"""
    menubar = MenuBar()
    file_menu = menubar.addMenu("File")
    action = file_menu.addAction("Test")
    action.setShortcut("Ctrl+T")
    assert action.shortcut().toString() == "Ctrl+T"

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

class TestWindow(QMainWindow):
    """Test window class for menu callbacks."""
    def __init__(self):
        """Initialize test window."""
        super().__init__()
        self.config = {
            'modules': {
                'enabled': ['test']
            }
        }
        self.close_called = False
        self.tool_bar = None
        self.status_bar = None

    def close(self):
        """Handle window close."""
        self.close_called = True

def test_menu_callbacks(qapp):
    """Test menu action callbacks"""
    # Create a parent window with tracking
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

    # Toggle status bar
    statusbar_action.trigger()
    assert not statusbar_action.isChecked()
    assert not window.status_bar.isVisible()

def test_menu_callbacks_no_modules_section(qapp):
    """Test menu callbacks when config has no Modules section"""
    # Create a parent window with tracking
    window = TestWindow()
    window.config = {}  # Empty config
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

    # Toggle status bar
    statusbar_action.trigger()
    assert not statusbar_action.isChecked()
    assert not window.status_bar.isVisible()
