"""
Tests for the theme dialog functionality.
"""

import pytest
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStatusBar,
                              QComboBox, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from modules.theme.theme_dialog import ThemeDialog, ModernFrame, ModernButton, PreviewWidget
from modules.theme.theme_manager import ThemeManager
from config.app_config import Config

@pytest.fixture
def main_window(qtbot):
    """Create a main window with status bar for testing."""
    window = QMainWindow()
    window.setStatusBar(QStatusBar())
    qtbot.addWidget(window)
    return window

@pytest.fixture
def theme_dialog(qtbot, main_window, tmp_path):
    """Create a theme dialog instance for testing."""
    app = QApplication.instance() or QApplication([])
    config = Config()
    config.config_dir = str(tmp_path)
    theme_manager = ThemeManager(app, config)
    dialog = ThemeDialog(theme_manager, main_window)
    qtbot.addWidget(dialog)
    return dialog

def test_modern_frame(qtbot):
    """Test ModernFrame initialization and styling."""
    frame = ModernFrame()
    qtbot.addWidget(frame)
    
    style = frame.styleSheet()
    assert "border-radius: 8px" in style
    assert "background-color: palette(base)" in style
    assert frame.objectName() == "modernFrame"

def test_modern_button(qtbot):
    """Test ModernButton initialization and styling."""
    # Test primary button
    primary_btn = ModernButton("Primary", primary=True)
    qtbot.addWidget(primary_btn)
    assert primary_btn.objectName() == "primaryButton"
    assert primary_btn.minimumHeight() >= 36
    
    # Test secondary button
    secondary_btn = ModernButton("Secondary")
    qtbot.addWidget(secondary_btn)
    assert secondary_btn.objectName() == "secondaryButton"
    assert secondary_btn.cursor() == Qt.CursorShape.PointingHandCursor

def test_preview_widget(qtbot):
    """Test PreviewWidget initialization and UI setup."""
    preview = PreviewWidget()
    qtbot.addWidget(preview)
    
    # Check that the preview widget has been set up properly
    assert preview.layout() is not None
    assert preview.minimumHeight() > 0

def test_theme_dialog_initialization(theme_dialog):
    """Test theme dialog initialization."""
    assert theme_dialog.theme_manager is not None
    assert theme_dialog.windowTitle() == "Theme Manager"
    
    # Check that the theme selector is populated
    theme_selector = theme_dialog.findChild(QComboBox)
    assert theme_selector is not None
    assert theme_selector.count() >= 2  # At least light and dark themes

def test_theme_switching(theme_dialog, qtbot):
    """Test switching themes in the dialog."""
    theme_selector = theme_dialog.findChild(QComboBox)
    
    # Switch to dark theme
    theme_selector.setCurrentText("dark")
    qtbot.wait(100)  # Wait for theme to apply
    assert theme_dialog.theme_manager.current_theme == "dark"
    
    # Switch back to light theme
    theme_selector.setCurrentText("light")
    qtbot.wait(100)  # Wait for theme to apply
    assert theme_dialog.theme_manager.current_theme == "light"

def test_create_theme(theme_dialog, qtbot, monkeypatch):
    """Test creating a new theme."""
    # Mock the QInputDialog.getText method
    def mock_getText(*args, **kwargs):
        return "Custom Theme", True
    monkeypatch.setattr("PyQt6.QtWidgets.QInputDialog.getText", mock_getText)
    
    # Find and click the create theme button
    create_button = None
    for button in theme_dialog.findChildren(ModernButton):
        if "Create" in button.text():
            create_button = button
            break
    
    assert create_button is not None
    qtbot.mouseClick(create_button, Qt.MouseButton.LeftButton)
    qtbot.wait(100)  # Wait for theme to be created
    
    # Verify the new theme exists
    theme_selector = theme_dialog.findChild(QComboBox)
    assert "Custom Theme" in [theme_selector.itemText(i) for i in range(theme_selector.count())]

def test_delete_theme(theme_dialog, qtbot, monkeypatch):
    """Test deleting a theme."""
    # First create a custom theme
    def mock_getText(*args, **kwargs):
        return "Theme to Delete", True
    monkeypatch.setattr("PyQt6.QtWidgets.QInputDialog.getText", mock_getText)
    
    create_button = None
    for button in theme_dialog.findChildren(ModernButton):
        if "Create" in button.text():
            create_button = button
            break
    
    qtbot.mouseClick(create_button, Qt.MouseButton.LeftButton)
    qtbot.wait(100)
    
    # Mock the QMessageBox.question method to return Yes
    def mock_question(*args, **kwargs):
        from PyQt6.QtWidgets import QMessageBox
        return QMessageBox.StandardButton.Yes
    monkeypatch.setattr("PyQt6.QtWidgets.QMessageBox.question", mock_question)
    
    # Select the custom theme
    theme_selector = theme_dialog.findChild(QComboBox)
    theme_selector.setCurrentText("Theme to Delete")
    
    # Find and click the delete button
    delete_button = None
    for button in theme_dialog.findChildren(ModernButton):
        if "Delete" in button.text():
            delete_button = button
            break
    
    assert delete_button is not None
    qtbot.mouseClick(delete_button, Qt.MouseButton.LeftButton)
    qtbot.wait(100)
    
    # Verify the theme was deleted
    assert "Theme to Delete" not in [theme_selector.itemText(i) for i in range(theme_selector.count())]

def test_theme_preview(theme_dialog, qtbot):
    """Test that theme preview updates when switching themes."""
    preview = theme_dialog.findChild(PreviewWidget)
    assert preview is not None
    
    # Switch themes and verify the preview updates
    theme_selector = theme_dialog.findChild(QComboBox)
    initial_palette = preview.palette()
    
    # Switch to a different theme
    current_theme = theme_selector.currentText()
    new_theme = "dark" if current_theme == "light" else "light"
    theme_selector.setCurrentText(new_theme)
    qtbot.wait(100)
    
    # Verify the palette changed
    assert preview.palette() != initial_palette
