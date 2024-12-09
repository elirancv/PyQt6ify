import logging
from PyQt6.QtWidgets import QStatusBar, QLabel

def create_status_bar(window):
    """
    Creates and sets up the status bar for the main window.
    A permanent label with the text "Ready" is added to the status bar.
    
    :param window: The main application window.
    """
    try:
        status_bar = QStatusBar(window)
        window.setStatusBar(status_bar)
        
        # Adding a permanent label to the status bar
        permanent_label = QLabel("Ready")
        status_bar.addPermanentWidget(permanent_label)
        
        logging.info("Status bar initialized successfully.")
        logging.info("Permanent status label set to 'Ready'.")
        
    except Exception as e:
        logging.error(f"Failed to create status bar: {e}")

def update_status_bar(status_bar, message):
    """
    Updates the status bar with a temporary message.
    
    :param status_bar: The QStatusBar object.
    :param message: The message to display in the status bar.
    """
    status_bar.showMessage(message, 5000)  # Display the message for 5 seconds
    logging.info(f"Status bar updated with message: '{message}'")
