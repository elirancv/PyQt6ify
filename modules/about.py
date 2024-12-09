from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
import logging

def show_about_dialog(window, config):
    """
    Show the About dialog with enhanced application information,
    dynamically loading data from the config.

    :param window: The main application window.
    :param config: The Config object to retrieve application settings.
    """
    # Fetch about info directly from app_config.py
    app_name = config.get_about_info('name')
    version = config.get_about_info('version')
    author = config.get_about_info('author')
    website = config.get_about_info('website')
    icon_path = config.get_about_info('icon')

    # Create the QMessageBox for the About dialog
    about_dialog = QMessageBox(window)
    about_dialog.setWindowTitle(f"About {app_name}")
    about_dialog.setWindowIcon(QIcon(icon_path))

    # Set the primary content of the dialog with rich text formatting
    about_dialog.setText(f"""
        <h3>{app_name}</h3>
        <p><b>Version:</b> {version}</p>
        <p><b>Author:</b> {author}</p>
        <p>This is a powerful and flexible PyQt6-based application.</p>
    """)

    # Add additional informative text
    about_dialog.setInformativeText(f"""
        <p>For more information, visit our 
        <a href='{website}'>official website</a>.</p>
        <p><i>All rights reserved © 2024</i></p>
    """)

    # Set buttons and icons
    about_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
    about_dialog.setIcon(QMessageBox.Icon.Information)
    
    # Execute the dialog
    about_dialog.exec()
