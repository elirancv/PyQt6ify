"""
Dashboard module for PyQt6ify Pro.
"""
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from loguru import logger

class Dashboard(QWidget):
    """Main dashboard widget."""

    def __init__(self, parent=None):
        """Initialize dashboard widget."""
        super().__init__(parent)
        self.parent = parent
        logger.debug("Dashboard widget initialized")
        self.init_ui()

    def init_ui(self):
        """Initialize the dashboard UI."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Welcome message
        welcome = QLabel("Welcome to PyQt6ify Pro!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)

        # Description
        description = QLabel("A powerful and feature-rich PyQt6 application template")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Add some space
        layout.addSpacing(20)

        # Create a new project button
        new_project_btn = QPushButton("Create New Project")
        new_project_btn.clicked.connect(self.create_new_project)
        layout.addWidget(new_project_btn)

        # Open existing project button
        open_project_btn = QPushButton("Open Existing Project")
        open_project_btn.clicked.connect(self.open_project)
        layout.addWidget(open_project_btn)

        self.setLayout(layout)

    def create_new_project(self):
        """Handle create new project button click."""
        if hasattr(self.parent, 'new_file'):
            self.parent.new_file()

    def open_project(self):
        """Handle open project button click."""
        if hasattr(self.parent, 'open_file'):
            self.parent.open_file()
