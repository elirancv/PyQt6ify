"""
About module for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from loguru import logger
import os

def show_about_dialog(window, config):
    """
    Show the About dialog with enhanced application information,
    dynamically loading data from the config.

    :param window: The main application window.
    :param config: The Config object to retrieve application settings.
    """
    try:
        # Get about info from config
        about_info = config.about_info
        app_name = about_info['name']
        version = about_info['version']
        author = about_info['author']
        description = about_info['description']
        website = about_info['website']
        
        # Create about dialog
        about = QMessageBox(window)
        about.setWindowTitle(f"About {app_name}")
        
        # Set icon if available
        icon_path = about_info.get('icon')
        if icon_path and os.path.exists(icon_path):
            about.setWindowIcon(QIcon(icon_path))

        # Copy the window's palette
        palette = QPalette(window.palette())
        about.setPalette(palette)

        # Set text color based on the theme
        text_color = palette.color(QPalette.ColorRole.WindowText)
        dim_text_color = QColor(text_color.red(), text_color.green(), text_color.blue(), 180)
        link_color = QColor(77, 166, 255)  # Bright blue that works well in dark mode
        
        # Create text with explicit styling
        about_text = f"""
        <div style='color: {text_color.name()}; position: absolute; left: 50%; transform: translateX(-45%);'>
            <p style='font-size: 16px; font-weight: bold; margin: 0 0 8px 0;'>{app_name}</p>
            <p style='margin: 4px 0;'><span style='color: {dim_text_color.name()};'>Version:</span> {version}</p>
            <p style='margin: 4px 0;'><span style='color: {dim_text_color.name()};'>Author:</span> {author}</p>
            <p style='margin: 8px 0;'>{description}</p>
            <p style='margin: 4px 0;'>For more information, visit our <a href='{website}' style='color: {link_color.name()};'>official website</a></p>
        </div>
        """
        
        about.setText(about_text)
        about.setTextFormat(Qt.TextFormat.RichText)
        about.setIcon(QMessageBox.Icon.Information)
        about.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set size constraints
        about.setFixedWidth(470)
        about.setFixedHeight(200)
        
        # Apply window background color
        about.setStyleSheet(f"""
            QMessageBox {{
                background-color: {palette.color(QPalette.ColorRole.Window).name()};
                color: {text_color.name()};
                width: 470px;
                height: 200px;
            }}
            QLabel {{
                background-color: {palette.color(QPalette.ColorRole.Window).name()};
                color: {text_color.name()};
                width: 470px;
            }}
            QPushButton {{
                min-width: 87px;
                min-height: 25px;
                padding: 0px;
                margin: 0px 4px;
            }}
            QPushButton:default {{
                border: 2px solid {link_color.name()};
            }}
        """)
        
        logger.info(f"Showing about dialog for {app_name} {version}")
        about.exec()
        
    except Exception as e:
        logger.error(f"Error showing about dialog: {str(e)}")
        # Show a simpler error dialog if something goes wrong
        QMessageBox.critical(window, "Error", f"Error showing about dialog: {str(e)}")
