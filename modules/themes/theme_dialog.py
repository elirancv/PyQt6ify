"""
Theme dialog for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel,
                          QFrame, QScrollArea, QWidget, QGridLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
from loguru import logger

class ThemeDialog(QDialog):
    """Dialog for theme selection."""
    
    def __init__(self, parent=None, theme_manager=None):
        """Initialize the theme dialog."""
        super().__init__(parent)
        self.parent = parent
        self.theme_manager = theme_manager
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle("Theme Selection")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add description
        description = QLabel("Select a theme to customize the application's appearance:")
        description.setWordWrap(True)
        description.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: palette(text);
            }
        """)
        layout.addWidget(description)
        
        # Add theme combo box
        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumHeight(30)
        if self.theme_manager:
            themes = self.theme_manager.get_available_themes()
            self.theme_combo.addItems(themes)
            
            # Set current theme
            current_theme = self.theme_manager.get_current_theme()
            if current_theme in themes:
                self.theme_combo.setCurrentText(current_theme)
        
        layout.addWidget(self.theme_combo)
        
        # Buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Add apply button
        apply_button = QPushButton("Apply Theme")
        apply_button.setMinimumHeight(30)
        apply_button.clicked.connect(self.apply_theme)
        buttons_layout.addWidget(apply_button)
        
        # Add cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setMinimumHeight(30)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def apply_styles(self):
        """Apply custom styles to the dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: palette(window);
                color: palette(windowText);
                border: 1px solid palette(mid);
            }
            QLabel {
                color: palette(text);
            }
            QComboBox {
                background-color: palette(base);
                color: palette(text);
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 6em;
            }
            QComboBox:hover {
                border-color: palette(highlight);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QPushButton {
                background-color: palette(button);
                color: palette(buttonText);
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: palette(highlight);
                color: palette(highlightedText);
                border-color: palette(highlight);
            }
            QPushButton:pressed {
                background-color: palette(dark);
            }
        """)
    
    def apply_theme(self):
        """Apply the selected theme."""
        if self.theme_manager:
            theme = self.theme_combo.currentText()
            if self.theme_manager.switch_theme(theme):
                logger.info(f"Theme {theme} applied and saved to config")
                self.accept()
            else:
                logger.error(f"Failed to apply theme: {theme}")
