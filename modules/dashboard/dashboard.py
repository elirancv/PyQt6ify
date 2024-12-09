"""
Main dashboard widget implementation.
"""

import os
from loguru import logger
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                          QHBoxLayout, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from modules.config.config import Config
from modules.core.module_loader import ModuleLoader

class MetricCard(QFrame):
    """A card widget to display metrics."""
    
    def __init__(self, title, value, icon="📊"):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Icon and title in horizontal layout
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("", 16))
        title_label = QLabel(title)
        title_label.setFont(QFont("", 10))
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Value
        value_label = QLabel(str(value))
        value_label.setFont(QFont("", 24, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add to layout
        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        
        self.setLayout(layout)

class Dashboard(QWidget):
    """Main dashboard widget that serves as the central widget of the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.debug("Dashboard widget initialized")
        
        # Get config and module_loader from parent window
        self.parent = parent
        self.config = parent.config if parent else None
        self.module_loader = parent.module_loader if parent else None
        
        if not self.config or not self.module_loader:
            logger.error("Dashboard requires a parent window with config and module_loader")
            return
            
        self.setup_ui()
        
    def setup_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Welcome section with reduced vertical space
        welcome_layout = QVBoxLayout()
        welcome_layout.setSpacing(5)
        
        app_name = self.config.get('Application', 'name', 'PyQt6ify Pro')
        title = QLabel(f"Welcome to {app_name}")
        title.setObjectName("dashboard-title")
        description = QLabel("This is a powerful and feature-rich PyQt6 application template.")
        description.setObjectName("dashboard-description")
        
        welcome_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(description, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(welcome_layout)

        # Metrics section in a horizontal layout
        metrics_widget = QWidget()
        metrics_widget.setObjectName("metrics-widget")
        metrics_layout = QHBoxLayout(metrics_widget)
        metrics_layout.setSpacing(10)
        
        # Calculate metrics
        loaded_modules = sum(1 for module_name in self.module_loader.loaded_modules 
                           if not module_name.endswith('__init__'))
        available_themes = len(self.config.window_settings.get('available_themes', ['light', 'dark']))
        db_tables = len(self.config.get('Database', 'tables', '').split(','))

        # Create metric cards with icons and better spacing
        metrics = [
            ("📦", "Loaded Modules", str(loaded_modules)),
            ("🎨", "Available Themes", str(available_themes)),
            ("🗃️", "Database Tables", str(db_tables))
        ]

        for icon, label, value in metrics:
            metric_card = QFrame()
            metric_card.setObjectName("metric-card")
            card_layout = QVBoxLayout(metric_card)
            card_layout.setSpacing(5)
            
            icon_label = QLabel(icon)
            icon_label.setObjectName("metric-icon")
            value_label = QLabel(value)
            value_label.setObjectName("metric-value")
            name_label = QLabel(label)
            name_label.setObjectName("metric-name")
            
            card_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)
            
            metrics_layout.addWidget(metric_card)

        main_layout.addWidget(metrics_widget)

        # Features section in a grid layout
        features_label = QLabel("Key Features")
        features_label.setObjectName("section-title")
        main_layout.addWidget(features_label)

        features_grid = QGridLayout()
        features_grid.setSpacing(15)

        features = [
            ("🔌", "Module System", "Extensible plugin architecture for easy customization"),
            ("🎨", "Theme Support", "Built-in light and dark themes with customization options"),
            ("🗄️", "Database Integration", "SQLite database with automatic table management"),
            ("🛠️", "Error Handling", "Comprehensive error logging and handling system"),
            ("⚡", "Performance", "Optimized for speed and responsiveness"),
            ("🔒", "Security", "Built-in security features and data protection")
        ]

        row = 0
        col = 0
        for icon, title, desc in features:
            feature_card = QFrame()
            feature_card.setObjectName("feature-card")
            feature_layout = QVBoxLayout(feature_card)
            feature_layout.setSpacing(5)

            icon_title = QLabel(f"{icon} {title}")
            icon_title.setObjectName("feature-title")
            description = QLabel(desc)
            description.setObjectName("feature-description")
            description.setWordWrap(True)

            feature_layout.addWidget(icon_title)
            feature_layout.addWidget(description)

            features_grid.addWidget(feature_card, row, col)
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1

        main_layout.addLayout(features_grid)
        
        # Add stretch to push everything up
        main_layout.addStretch()

        # Add stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            #dashboard-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            #dashboard-description {
                font-size: 14px;
                color: #888;
            }
            #metrics-widget {
                margin: 10px 0;
            }
            #metric-card {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 15px;
                min-width: 150px;
            }
            #metric-icon {
                font-size: 24px;
            }
            #metric-value {
                font-size: 28px;
                font-weight: bold;
            }
            #metric-name {
                font-size: 14px;
                color: #888;
            }
            #section-title {
                font-size: 20px;
                font-weight: bold;
                margin: 10px 0;
            }
            #feature-card {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 15px;
            }
            #feature-title {
                font-size: 16px;
                font-weight: bold;
            }
            #feature-description {
                font-size: 13px;
                color: #888;
            }
        """)
