"""
About module for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QMessageBox, QApplication, QDialog
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from loguru import logger
import os

def show_about_dialog(config, parent=None):
    """
    Show the About dialog with enhanced application information,
    dynamically loading data from the config.

    :param config: The Config object to retrieve application settings.
    :param parent: Optional parent window for the dialog.
    :return: The created QMessageBox dialog.
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
        about = QMessageBox(parent)
        about.setWindowTitle(f"About {app_name}")
        
        # Set icon if available
        icon_path = about_info.get('icon')
        if icon_path and os.path.exists(icon_path):
            about.setWindowIcon(QIcon(icon_path))

        # Copy the parent's palette if available, otherwise use app palette
        if parent:
            palette = QPalette(parent.palette())
        else:
            palette = QApplication.instance().palette()
        about.setPalette(palette)

        # Set text color based on the theme
        text_color = palette.color(QPalette.ColorRole.WindowText)
        dim_text_color = QColor(text_color.red(), text_color.green(), text_color.blue(), 180)
        link_color = QColor(77, 166, 255)  # Bright blue that works well in dark mode
        
        # Create text with explicit styling
        about_text = f"""
        <div style='color: {text_color.name()}; text-align: center;'>
            <p style='font-size: 16px; font-weight: bold; margin: 0 0 8px 0;'>{app_name}</p>
            <p style='margin: 4px 0;'><span style='color: {dim_text_color.name()};'>Version:</span> {version}</p>
            <p style='margin: 4px 0;'><span style='color: {dim_text_color.name()};'>Author:</span> {author}</p>
            <p style='margin: 8px 0;'>{description}</p>
            <p style='margin: 8px 0;'><a href='{website}' style='color: {link_color.name()};'>Visit Website</a></p>
        </div>
        """
        
        # Set text and make it selectable
        about.setText(about_text)
        about.setTextFormat(Qt.TextFormat.RichText)
        about.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        
        # Set standard buttons and default button
        about.setStandardButtons(QMessageBox.StandardButton.Ok)
        about.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        # Show the dialog
        about.show()
        return about
        
    except Exception as e:
        logger.error(f"Error showing about dialog: {str(e)}")
        return None
