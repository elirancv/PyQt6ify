"""
About module for PyQt6ify Pro.
"""

from PyQt6.QtWidgets import QMessageBox, QApplication, QDialog
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from loguru import logger
import os

def show_about_dialog(config, parent=None, test_mode=False):
    """
    Show the About dialog with enhanced application information,
    dynamically loading data from the config.

    :param config: The Config object to retrieve application settings.
    :param parent: Optional parent window for the dialog.
    :param test_mode: If True, dialog will not be shown modally (for testing).
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
        bg_color = palette.color(QPalette.ColorRole.Window)
        accent_color = QColor(77, 166, 255) if text_color.lightness() > 128 else QColor(102, 187, 255)
        dim_text_color = QColor(text_color.red(), text_color.green(), text_color.blue(), 180)
        
        # Create text with explicit styling
        about_text = f"""
        <div style='color: {text_color.name()}; text-align: center; padding: 20px;'>
            <div style='margin-bottom: 24px;'>
                <h1 style='font-size: 24px; font-weight: bold; margin: 0 0 4px 0; color: {accent_color.name()};'>{app_name}</h1>
                <p style='font-size: 14px; margin: 4px 0; color: {dim_text_color.name()};'>Version {version}</p>
            </div>
            
            <div style='margin: 16px 0; line-height: 1.5;'>
                <p style='margin: 8px 0;'>{description}</p>
                <p style='margin: 12px 0; color: {dim_text_color.name()};'>Created by {author}</p>
            </div>
            
            <div style='margin-top: 20px;'>
                <a href='{website}' style='color: {accent_color.name()}; text-decoration: none; font-weight: bold;'>Visit Website</a>
            </div>
        </div>
        """
        
        # Set text and make it selectable
        about.setText(about_text)
        about.setTextFormat(Qt.TextFormat.RichText)
        about.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction | Qt.TextInteractionFlag.LinksAccessibleByMouse)
        
        # Set minimum size for better layout
        about.setMinimumWidth(400)
        
        # Style the OK button to match theme
        ok_button = about.button(QMessageBox.StandardButton.Ok)
        if ok_button:
            ok_button.setMinimumWidth(100)
            
        # Add some padding around the content
        about.layout().setContentsMargins(20, 20, 20, 20)
        
        # Set standard buttons and default button
        about.setStandardButtons(QMessageBox.StandardButton.Ok)
        about.setDefaultButton(QMessageBox.StandardButton.Ok)
        
        # Show the dialog modally
        if not test_mode:
            about.exec()
        return about
        
    except Exception as e:
        logger.error(f"Error showing about dialog: {str(e)}")
        return None
