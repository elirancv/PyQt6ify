"""
Theme Dialog for PyQt6ify Pro - A modern and polished theme manager.
"""

import logging
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QComboBox,
                           QPushButton, QLabel, QFrame, QWidget, QScrollArea,
                           QGridLayout, QLineEdit, QApplication)
from PyQt6.QtCore import Qt, QSize, QMargins, QTimer
from PyQt6.QtGui import QPalette, QColor, QIcon, QPainter, QPen, QPainterPath
import qtawesome as qta
import traceback

class ModernFrame(QFrame):
    """A modern looking frame with rounded corners and shadow."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernFrame")
        self.setStyleSheet("""
            #modernFrame {
                background-color: palette(base);
                border-radius: 8px;
                border: 1px solid palette(mid);
            }
        """)

class ModernButton(QPushButton):
    """Modern styled button with hover effects."""
    def __init__(self, text="", parent=None, primary=False):
        super().__init__(text, parent)
        self.primary = primary
        self.setMinimumHeight(36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("primaryButton" if primary else "secondaryButton")
        
        # Add some padding
        self.setContentsMargins(12, 6, 12, 6)
        
        # Make sure the button is wide enough
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(text)
        self.setMinimumWidth(max(text_width + 48, 120))

class PreviewWidget(QWidget):
    """Widget that shows a preview of the theme."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the preview widget UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title bar with window controls
        title_bar = ModernFrame()
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(16, 8, 16, 8)
        
        title_label = QLabel("Window Title")
        title_label.setStyleSheet("font-weight: 600; font-size: 13px;")
        
        # Window controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        for color in ["#fc5753", "#fdbc40", "#33c748"]:  # macOS-style window controls
            control = QWidget()
            control.setFixedSize(12, 12)
            control.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
            controls_layout.addWidget(control)
        
        title_layout.addLayout(controls_layout)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title_bar)
        
        # Main content area
        content = ModernFrame()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(24, 24, 24, 24)
        
        # Menu bar
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(24)
        for menu in ["File", "Edit", "View", "Help"]:
            menu_btn = QLabel(menu)
            menu_btn.setStyleSheet("""
                QLabel {
                    color: palette(text);
                    font-size: 13px;
                }
                QLabel:hover {
                    color: palette(highlight);
                }
            """)
            menu_layout.addWidget(menu_btn)
        menu_layout.addStretch()
        content_layout.addLayout(menu_layout)
        
        # Toolbar
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 8, 0, 8)
        toolbar_layout.setSpacing(8)
        
        # Add toolbar buttons with icons
        for icon_name in ["fa5s.file", "fa5s.save", "fa5s.folder-open"]:
            btn = ModernButton()
            btn.setIcon(qta.icon(icon_name))
            btn.setFixedSize(36, 36)
            toolbar_layout.addWidget(btn)
        
        toolbar_layout.addStretch()
        content_layout.addWidget(toolbar)
        
        # Button section
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(12)
        
        regular_btn = ModernButton("Regular Button")
        disabled_btn = ModernButton("Disabled Button")
        accent_btn = ModernButton("Accent Button", primary=True)
        disabled_btn.setEnabled(False)
        
        buttons_layout.addWidget(regular_btn)
        buttons_layout.addWidget(disabled_btn)
        buttons_layout.addWidget(accent_btn)
        buttons_layout.addStretch()
        content_layout.addWidget(buttons_widget)
        
        # Form section
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(16)
        form_layout.setHorizontalSpacing(12)
        
        # Input field
        input_label = QLabel("Input Field:")
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter text here...")
        input_field.setMinimumHeight(36)
        form_layout.addWidget(input_label, 0, 0)
        form_layout.addWidget(input_field, 0, 1)
        
        # Dropdown
        combo_label = QLabel("Dropdown:")
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        combo.setMinimumHeight(36)
        form_layout.addWidget(combo_label, 1, 0)
        form_layout.addWidget(combo, 1, 1)
        
        content_layout.addLayout(form_layout)
        layout.addWidget(content)
        
        # Status bar
        status_bar = ModernFrame()
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(16, 8, 16, 8)
        status_label = QLabel("Status: Ready")
        status_layout.addWidget(status_label)
        layout.addWidget(status_bar)

class ThemeDialog(QDialog):
    """Dialog for managing application themes."""
    def __init__(self, theme_manager, parent=None):
        """Initialize the theme dialog."""
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.parent = parent  # Store parent reference to access status bar
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the dialog's user interface."""
        self.setWindowTitle("Theme Settings")
        self.setMinimumWidth(700)
        self.setMinimumHeight(800)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Theme selection section
        theme_section = ModernFrame()
        theme_layout = QHBoxLayout(theme_section)
        theme_layout.setContentsMargins(24, 16, 24, 16)
        
        theme_label = QLabel("Current Theme:")
        theme_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumWidth(200)
        self.theme_combo.setMinimumHeight(36)
        self.theme_combo.addItems(self.theme_manager.get_available_themes())
        self.theme_combo.setCurrentText(self.theme_manager.get_current_theme())
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addWidget(theme_section)
        
        # Preview section
        preview_label = QLabel("Preview:")
        preview_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(preview_label)
        
        # Preview area
        preview_area = ModernFrame()
        preview_layout = QVBoxLayout(preview_area)
        preview_layout.setContentsMargins(2, 2, 2, 2)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.preview = PreviewWidget()
        scroll.setWidget(self.preview)
        preview_layout.addWidget(scroll)
        layout.addWidget(preview_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        create_button = ModernButton("Create New Theme", primary=True)
        create_button.setIcon(qta.icon("fa5s.plus"))
        create_button.clicked.connect(self.on_create_theme)
        
        delete_button = ModernButton("Delete Theme")
        delete_button.setIcon(qta.icon("fa5s.trash"))
        delete_button.clicked.connect(self.on_delete_theme)
        
        close_button = ModernButton("Close")
        close_button.setIcon(qta.icon("fa5s.times"))
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(create_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Apply global styling
        self.setStyleSheet("""
            QDialog {
                background-color: palette(window);
                color: palette(windowText);
            }
            QLabel {
                color: palette(text);
            }
            QComboBox {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 6px 12px;
                background-color: palette(button);
                selection-background-color: palette(highlight);
                selection-color: palette(highlightedText);
            }
            QComboBox:hover {
                border-color: palette(highlight);
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QLineEdit {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 6px 12px;
                background-color: palette(base);
                selection-background-color: palette(highlight);
                selection-color: palette(highlightedText);
            }
            QLineEdit:focus {
                border-color: palette(highlight);
            }
            #primaryButton {
                background-color: palette(highlight);
                color: palette(highlightedText);
                border: none;
                border-radius: 4px;
                font-weight: 600;
            }
            #primaryButton:hover {
                background-color: #2962ff;
            }
            #primaryButton:pressed {
                background-color: #2145cc;
            }
            #secondaryButton {
                background-color: palette(button);
                color: palette(buttonText);
                border: 1px solid palette(mid);
                border-radius: 4px;
            }
            #secondaryButton:hover {
                background-color: palette(light);
                border-color: palette(highlight);
            }
            #secondaryButton:pressed {
                background-color: palette(midlight);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: palette(base);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: palette(mid);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: palette(dark);
            }
        """)
    
    def on_theme_changed(self, theme_name):
        """Handle theme selection changes."""
        try:
            logging.info(f"Theme dialog: changing theme to {theme_name}")
            
            # Defer the theme change using a single-shot timer
            # This prevents the dialog from closing due to event loop issues
            QTimer.singleShot(100, lambda: self._apply_theme(theme_name))
            
        except Exception as e:
            logging.error(f"Error in theme dialog theme change: {str(e)}")
            logging.error(traceback.format_exc())
            self.theme_combo.setCurrentText(self.theme_manager.get_current_theme())
    
    def _apply_theme(self, theme_name):
        """Actually apply the theme change."""
        try:
            if self.parent and hasattr(self.parent, 'statusBar'):
                self.parent.statusBar().showMessage(f"Applying theme: {theme_name}...")
                
            if self.theme_manager.apply_theme(theme_name):
                logging.info(f"Theme dialog: successfully applied theme {theme_name}")
                if self.parent and hasattr(self.parent, 'statusBar'):
                    self.parent.statusBar().showMessage(f"Theme '{theme_name}' applied successfully", 3000)
                # Force the preview to refresh
                self.preview.update()
            else:
                logging.error(f"Theme dialog: failed to apply theme {theme_name}")
                if self.parent and hasattr(self.parent, 'statusBar'):
                    self.parent.statusBar().showMessage(f"Failed to apply theme '{theme_name}'", 3000)
                self.theme_combo.setCurrentText(self.theme_manager.get_current_theme())
                
        except Exception as e:
            logging.error(f"Error applying theme: {str(e)}")
            logging.error(traceback.format_exc())
            if self.parent and hasattr(self.parent, 'statusBar'):
                self.parent.statusBar().showMessage(f"Error applying theme: {str(e)}", 3000)
            self.theme_combo.setCurrentText(self.theme_manager.get_current_theme())
    
    def on_create_theme(self):
        """Handle creating a new theme."""
        # TODO: Implement theme creation dialog
        logging.info("Theme creation dialog not implemented yet")
    
    def on_delete_theme(self):
        """Handle deleting the current theme."""
        current_theme = self.theme_combo.currentText()
        if self.theme_manager.delete_theme(current_theme):
            self.theme_combo.removeItem(self.theme_combo.currentIndex())
            self.theme_manager.apply_theme("light")
            self.theme_combo.setCurrentText("light")
