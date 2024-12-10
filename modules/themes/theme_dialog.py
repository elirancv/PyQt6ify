"""
Theme dialog for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QFrame, QLineEdit
)
from PyQt6.QtCore import pyqtSignal
from loguru import logger

class ThemeDialog(QDialog):
    """Dialog for theme selection."""

    themeChanged = pyqtSignal(str)  # Signal emitted when theme is changed

    def __init__(self, theme_manager, parent=None):
        """Initialize the theme dialog.

        Args:
            theme_manager: The theme manager instance
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.initial_theme = None
        if theme_manager:
            current_theme = theme_manager.get_current_theme()
            self.initial_theme = current_theme['name'] if current_theme else None

        self.init_ui()
        self.apply_styles()
        self.load_themes()

    def init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle("Theme Selection")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add description
        description = QLabel("Select a theme to customize the application's appearance:")
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 12px;")
        layout.addWidget(description)

        # Add theme list
        self.theme_list = QListWidget()
        self.theme_list.setMinimumHeight(150)
        layout.addWidget(self.theme_list)

        # Add preview section
        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        preview_layout = QVBoxLayout()
        preview_layout.setContentsMargins(10, 10, 10, 10)

        preview_label = QLabel("Preview")
        preview_label.setStyleSheet("font-weight: bold;")
        preview_layout.addWidget(preview_label)

        # Add sample widgets for preview
        sample_edit = QLineEdit("Sample text input")
        sample_edit.setEnabled(False)
        preview_layout.addWidget(sample_edit)

        sample_button = QPushButton("Sample Button")
        sample_button.setEnabled(False)
        preview_layout.addWidget(sample_button)

        preview_frame.setLayout(preview_layout)
        layout.addWidget(preview_frame)

        # Add buttons
        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_theme)
        button_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_themes(self):
        """Load available themes into the list."""
        if not self.theme_manager:
            logger.error("Theme manager not provided")
            return

        try:
            # Add available themes
            themes = self.theme_manager.get_available_themes()
            self.theme_list.addItems(themes)

            # Select current theme
            current_theme = self.theme_manager.get_current_theme()
            for i in range(self.theme_list.count()):
                if self.theme_list.item(i).text() == current_theme['name']:
                    self.theme_list.setCurrentRow(i)
                    break

        except Exception as e:
            logger.error(f"Error loading themes: {str(e)}")

    def apply_styles(self):
        """Apply styles to the dialog."""
        if not self.theme_manager:
            return

        try:
            # Get current theme colors
            current_theme = self.theme_manager.get_current_theme()
            background = current_theme.get('window', '#FFFFFF')
            foreground = current_theme.get('windowText', '#000000')
            accent = current_theme.get('highlight', '#0078D4')
            button_bg = current_theme.get('button', '#F0F0F0')
            button_text = current_theme.get('buttonText', '#000000')
            base = current_theme.get('base', '#FFFFFF')
            text = current_theme.get('text', '#000000')

            # Apply theme colors
            self.setStyleSheet(f"""
                QDialog {{
                    background-color: {background};
                    color: {foreground};
                }}
                QLabel {{
                    color: {foreground};
                }}
                QListWidget {{
                    background-color: {base};
                    color: {text};
                    border: 1px solid {accent};
                    border-radius: 4px;
                }}
                QListWidget::item:selected {{
                    background-color: {accent};
                    color: {background};
                }}
                QPushButton {{
                    background-color: {button_bg};
                    color: {button_text};
                    border: 1px solid {accent};
                    border-radius: 4px;
                    padding: 5px 15px;
                }}
                QPushButton:hover {{
                    background-color: {accent};
                    color: {background};
                }}
                QPushButton:disabled {{
                    background-color: {button_bg};
                    color: {button_text};
                    opacity: 0.7;
                }}
                QFrame {{
                    border: 1px solid {accent};
                    border-radius: 4px;
                    background-color: {background};
                }}
                QLineEdit {{
                    background-color: {base};
                    color: {text};
                    border: 1px solid {accent};
                    border-radius: 4px;
                    padding: 5px;
                }}
                QLineEdit:disabled {{
                    background-color: {base};
                    color: {text};
                    opacity: 0.7;
                }}
            """)

        except Exception as e:
            logger.error(f"Error applying styles: {str(e)}")

    def apply_theme(self):
        """Apply the selected theme."""
        if not self.theme_manager:
            return

        try:
            selected_items = self.theme_list.selectedItems()
            if selected_items:
                theme_name = selected_items[0].text()
                if self.theme_manager.apply_theme(theme_name):
                    self.accept()
                else:
                    self.reject()
        except Exception as e:
            logger.error(f"Error applying theme: {str(e)}")
            self.reject()

    def reject(self):
        """Handle dialog rejection."""
        self.close()
