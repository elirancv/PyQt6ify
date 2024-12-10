"""
Revised ThemeManager for PyQt6ify Pro.
Handles theme loading, switching, previews, and persistence.
"""

import os
import json
import ctypes
from typing import Dict, List
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from loguru import logger
from modules.config.config import Config


class ThemeManager:
    """Manages application themes."""

    def __init__(self, app: QApplication, config: Config):
        """Initialize the theme manager.

        Args:
            app (QApplication): The main application instance.
            config (Config): Configuration manager instance.
        """
        self.app = app
        self.config = config
        self.themes = {}
        self.current_theme = None
        self.default_theme = "dark"

        # Initialize Windows-specific APIs for dark mode
        try:
            self.dwmapi = ctypes.windll.dwmapi
            self.DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        except Exception:
            self.dwmapi = None
            logger.warning("Windows DWM API not available for dark mode")

        # Load themes
        self.themes_file = os.path.join(os.path.dirname(__file__), 'themes.json')
        self.load_themes()
        logger.info(f"Loaded {len(self.themes)} themes from {self.themes_file}")

        # Set default application style
        self.app.setStyle('Fusion')

        # Apply the last used theme or default
        theme_name = self.config.get('window', 'theme', self.default_theme)
        if not self.apply_theme(theme_name):
            logger.warning(f"Failed to apply theme '{theme_name}'. Falling back to default.")
            self.apply_theme(self.default_theme)

        logger.info("ThemeManager initialized successfully")

    def load_themes(self) -> None:
        """Load themes from JSON file."""
        # Default themes
        self.themes = {
            "light": self._get_default_light_theme(),
            "dark": self._get_default_dark_theme(),
        }

        # Load custom themes from file
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, encoding='utf-8') as f:
                    custom_themes = json.load(f)
                    self.themes.update(custom_themes)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to load themes from {self.themes_file}: {e}")
        else:
            logger.warning(f"Themes file not found: {self.themes_file}")

    def apply_theme(self, theme_name: str, preview_only: bool = False) -> bool:
        """Apply a theme to the application.

        Args:
            theme_name (str): The name of the theme to apply.
            preview_only (bool): If True, apply the theme temporarily without saving.

        Returns:
            bool: True if the theme was applied successfully, False otherwise.
        """
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found.")
            return False

        try:
            theme = self.themes[theme_name]
            palette = QPalette()

            # Map theme keys to palette roles
            role_map = {
                "window": QPalette.ColorRole.Window,
                "windowText": QPalette.ColorRole.WindowText,
                "base": QPalette.ColorRole.Base,
                "alternateBase": QPalette.ColorRole.AlternateBase,
                "text": QPalette.ColorRole.Text,
                "button": QPalette.ColorRole.Button,
                "buttonText": QPalette.ColorRole.ButtonText,
                "brightText": QPalette.ColorRole.BrightText,
                "highlight": QPalette.ColorRole.Highlight,
                "highlightedText": QPalette.ColorRole.HighlightedText,
            }

            # Apply theme colors
            for key, color in theme.items():
                if key in role_map:
                    palette.setColor(QPalette.ColorGroup.All, role_map[key], QColor(color))

            self.app.setPalette(palette)

            # Update dark mode based on the window color brightness
            is_dark = QColor(theme.get("window", "#FFFFFF")).lightness() < 128
            for window in self.app.topLevelWindows():
                self.set_window_dark_mode(window, is_dark)  # Update the title bar appearance

            if not preview_only:
                self.current_theme = theme_name
                self.config.set('window', 'theme', theme_name)
                self.config.save()
                logger.info(f"Applied theme '{theme_name}' successfully.")
            else:
                logger.debug(f"Previewed theme '{theme_name}'.")

            return True

        except Exception as e:
            logger.error(f"Error applying theme '{theme_name}': {e}")
            return False

    def get_available_themes(self) -> List[str]:
        """Get a list of available themes.

        Returns:
            List[str]: Names of available themes.
        """
        return list(self.themes.keys())

    def get_current_theme(self) -> Dict[str, str]:
        """Get the currently applied theme.

        Returns:
            Dict[str, str]: Current theme details.
        """
        if self.current_theme and self.current_theme in self.themes:
            return self.themes[self.current_theme]
        return self.themes[self.default_theme]

    def set_window_dark_mode(self, window, is_dark: bool) -> None:
        """Enable or disable dark mode for a specific window.

        Args:
            window: The window to update.
            is_dark (bool): Whether to enable dark mode.
        """
        if not self.dwmapi:
            return

        try:
            value = ctypes.c_int(is_dark)
            self.dwmapi.DwmSetWindowAttribute(
                int(window.winId()),
                self.DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception as e:
            logger.warning(f"Failed to set dark mode for window: {e}")

    def _get_default_light_theme(self) -> Dict[str, str]:
        """Return the default light theme."""
        return {
            "name": "light",
            "window": "#ffffff",
            "windowText": "#2c3e50",
            "base": "#ffffff",
            "alternateBase": "#f8f9fa",
            "text": "#2c3e50",
            "button": "#e0e0e0",
            "buttonText": "#2c3e50",
            "highlight": "#3498db",
            "highlightedText": "#ffffff",
        }

    def _get_default_dark_theme(self) -> Dict[str, str]:
        """Return the default dark theme."""
        return {
            "name": "dark",
            "window": "#1e1e1e",
            "windowText": "#ffffff",
            "base": "#2c2c2c",
            "alternateBase": "#3c3c3c",
            "text": "#ffffff",
            "button": "#3c3c3c",
            "buttonText": "#ffffff",
            "highlight": "#3498db",
            "highlightedText": "#ffffff",
        }
