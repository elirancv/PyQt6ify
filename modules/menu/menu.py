"""
Menu module for PyQt6ify Pro.
"""
import os
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QIcon
from modules.about import show_about_dialog

class MenuBar(QMenuBar):
    """Main menu bar class for the application."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'icons')
        self.init_menus()

    def init_menus(self):
        """Initialize all menus."""
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_help_menu()

    def get_icon(self, icon_name: str) -> QIcon:
        """Get icon from resources."""
        icon_path = os.path.join(self.icon_path, f"{icon_name}.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    def create_file_menu(self):
        """Create the File menu."""
        file_menu = self.addMenu('&File')

        # New
        new_action = QAction(self.get_icon('new'), '&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create a new file')
        file_menu.addAction(new_action)

        # Open
        open_action = QAction(self.get_icon('open'), '&Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open an existing file')
        file_menu.addAction(open_action)

        # Save
        save_action = QAction(self.get_icon('save'), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save the current file')
        file_menu.addAction(save_action)

        # Save As
        save_as_action = QAction(self.get_icon('save_as'), 'Save &As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.setStatusTip('Save the file with a new name')
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Exit
        exit_action = QAction(self.get_icon('exit'), 'E&xit', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def create_edit_menu(self):
        """Create the Edit menu."""
        edit_menu = self.addMenu('&Edit')

        # Cut
        cut_action = QAction(self.get_icon('cut'), 'Cu&t', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.setStatusTip('Cut the selection')
        edit_menu.addAction(cut_action)

        # Copy
        copy_action = QAction(self.get_icon('copy'), '&Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setStatusTip('Copy the selection')
        edit_menu.addAction(copy_action)

        # Paste
        paste_action = QAction(self.get_icon('paste'), '&Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.setStatusTip('Paste from clipboard')
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        # Preferences
        preferences_action = QAction(self.get_icon('settings'), '&Preferences...', self)
        preferences_action.setStatusTip('Edit application preferences')
        edit_menu.addAction(preferences_action)

    def create_view_menu(self):
        """Create the View menu."""
        view_menu = self.addMenu('&View')

        # Theme
        theme_action = QAction(self.get_icon('theme'), '&Theme...', self)
        theme_action.setStatusTip('Change application theme')
        theme_action.triggered.connect(self.parent.show_theme_dialog)
        view_menu.addAction(theme_action)

        # Toolbar
        toolbar_action = QAction('&Toolbar', self)
        toolbar_action.setCheckable(True)
        toolbar_action.setChecked(True)
        toolbar_action.setStatusTip('Toggle toolbar visibility')
        toolbar_action.triggered.connect(self.toggle_toolbar)
        view_menu.addAction(toolbar_action)

        # Status Bar
        statusbar_action = QAction('&Status Bar', self)
        statusbar_action.setCheckable(True)
        statusbar_action.setChecked(True)
        statusbar_action.setStatusTip('Toggle status bar visibility')
        statusbar_action.triggered.connect(self.toggle_statusbar)
        view_menu.addAction(statusbar_action)

    def create_help_menu(self):
        """Create the Help menu."""
        help_menu = self.addMenu('&Help')

        # About
        about_action = QAction(self.get_icon('about'), '&About', self)
        about_action.setStatusTip('About PyQt6ify Pro')
        about_action.triggered.connect(lambda: show_about_dialog(self.parent.config))
        help_menu.addAction(about_action)

        # Documentation
        docs_action = QAction('&Documentation', self)
        docs_action.setStatusTip('View documentation')
        help_menu.addAction(docs_action)

    def toggle_toolbar(self, checked):
        """Toggle toolbar visibility."""
        if hasattr(self.parent, 'tool_bar'):
            self.parent.tool_bar.setVisible(checked)
            # Update config
            if not self.parent.config.config.has_section('Modules'):
                self.parent.config.config.add_section('Modules')
            self.parent.config.config.set('Modules', 'toolbar', str(checked))
            self.parent.config.save()


    def toggle_statusbar(self, checked):
        """Toggle status bar visibility."""
        if hasattr(self.parent, 'status_bar'):
            self.parent.status_bar.setVisible(checked)
            # Update config
            if not self.parent.config.config.has_section('Modules'):
                self.parent.config.config.add_section('Modules')
            self.parent.config.config.set('Modules', 'status_bar', str(checked))
            self.parent.config.save()
