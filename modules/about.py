"""
About dialog for PyQt6ify Pro.
"""

import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from loguru import logger

def show_about_dialog(parent):
    """Show the about dialog."""
    try:
        dialog = AboutDialog(parent)
        dialog.exec()
    except Exception as e:
        logger.error(f"Error showing about dialog: {str(e)}")

class AboutDialog(QDialog):
    """About dialog implementation."""

    def __init__(self, parent=None):
        """Initialize the about dialog."""
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config if parent else None
        self.init_ui()

    def init_ui(self):
        """Initialize the dialog UI."""
        try:
            # Set window properties
            app_name = self.config.get('Application', 'name', 'PyQt6ify Pro') if self.config else 'PyQt6ify Pro'
            self.setWindowTitle(f"About {app_name}")
            self.setFixedSize(400, 300)
            self.setModal(True)

            # Create main layout
            layout = QVBoxLayout()
            layout.setSpacing(20)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add app icon
            if self.config:
                icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                       self.config.get('About', 'icon', 'resources/icons/app_icon.png'))
                if os.path.exists(icon_path):
                    icon_label = QLabel()
                    pixmap = QPixmap(icon_path)
                    scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, 
                                                Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(scaled_pixmap)
                    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(icon_label)

            # Add app name
            app_name = self.config.get('Application', 'name', 'PyQt6ify Pro') if self.config else 'PyQt6ify Pro'
            name_label = QLabel(app_name)
            name_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(name_label)

            # Add version
            version = self.config.get('Application', 'version', '1.0.0') if self.config else '1.0.0'
            version_label = QLabel(f"Version {version}")
            version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(version_label)

            # Add description
            description = self.config.get('About', 'description', 
                                        'A modern PyQt6 application template') if self.config else 'A modern PyQt6 application template'
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(desc_label)

            # Add copyright
            copyright_text = self.config.get('About', 'copyright', 
                                           ' 2024 PyQt6ify Pro. All rights reserved.') if self.config else ' 2024 PyQt6ify Pro. All rights reserved.'
            copyright_label = QLabel(copyright_text)
            copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(copyright_label)

            # Add close button
            button_container = QWidget()
            button_layout = QVBoxLayout()
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)
            close_button.setFixedWidth(100)
            button_layout.addWidget(close_button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_container.setLayout(button_layout)
            layout.addWidget(button_container)

            self.setLayout(layout)

        except Exception as e:
            logger.error(f"Error initializing about dialog UI: {str(e)}")
            raise
