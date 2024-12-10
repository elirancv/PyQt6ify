"""
Enhanced About module for PyQt6ify Pro.
"""

import os
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QApplication
from loguru import logger


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
        app_name = about_info.get('Name', 'PyQt6ify Pro')
        version = about_info.get('Version', '1.0.0')
        author = about_info.get('Author', 'PyQt6ify Team')
        description = about_info.get('Description', 'A modern PyQt6 application template.')
        website = about_info.get('Website', 'https://github.com')
        icon_path = about_info.get('icon', 'resources/icons/app.png')

        # Resolve full path for the icon
        if not os.path.isabs(icon_path):
            icon_path = os.path.join(os.getcwd(), icon_path)

        # Create about dialog
        about = QMessageBox(parent)
        about.setWindowTitle(f"About {app_name}")

        # Set app icon from config.ini
        if os.path.exists(icon_path):
            about.setWindowIcon(QIcon(icon_path))
        else:
            logger.warning(f"App icon not found: {icon_path}")

        # Use the parent's palette if available, otherwise use app palette
        palette = parent.palette() if parent else QApplication.instance().palette()
        about.setPalette(palette)

        # Determine text colors based on the theme
        text_color = palette.color(QPalette.ColorRole.WindowText)
        accent_color = QColor(77, 166, 255) if text_color.lightness() > 128 else QColor(102, 187, 255)
        dim_text_color = QColor(text_color.red(), text_color.green(), text_color.blue(), 180)

        # Construct styled About content
        about_content = f"""
        <div style="color: {text_color.name()}; text-align: center; padding: 20px;">
            <h1 style="font-size: 20px; font-weight: bold; margin-bottom: 8px; color: {accent_color.name()};">
                {app_name}
            </h1>
            <p style="font-size: 14px; margin-bottom: 16px;">Version {version}</p>
            <p style="font-size: 12px; margin: 0 0 16px; line-height: 1.5;">
                {description}
            </p>
            <p style="font-size: 12px; color: {dim_text_color.name()}; margin-bottom: 12px;">
                Created by: <b>{author}</b>
            </p>
            <a href="{website}" style="color: {accent_color.name()}; text-decoration: none; font-weight: bold;">
                Visit Website
            </a>
        </div>
        """

        # Set content
        about.setText(about_content)
        about.setTextFormat(Qt.TextFormat.RichText)
        about.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction | Qt.TextInteractionFlag.LinksAccessibleByMouse)

        # Adjust dialog size and layout
        about.setMinimumWidth(500)
        about.setMinimumHeight(300)
        about.layout().setContentsMargins(20, 20, 20, 20)

        # Add buttons
        about.setStandardButtons(QMessageBox.StandardButton.Ok)
        about.setDefaultButton(QMessageBox.StandardButton.Ok)
        ok_button = about.button(QMessageBox.StandardButton.Ok)
        if ok_button:
            ok_button.setMinimumWidth(100)
            ok_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {accent_color.name()};
                    color: #ffffff;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background-color: {accent_color.darker(120).name()};
                }}
                QPushButton:pressed {{
                    background-color: {accent_color.darker(140).name()};
                }}
            """)

        # Display dialog
        if not test_mode:
            about.exec()

        return about

    except Exception as e:
        logger.error(f"Error showing about dialog: {str(e)}")
        return None
