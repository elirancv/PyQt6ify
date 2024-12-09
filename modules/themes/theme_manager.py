"""
Theme manager for PyQt6ify Pro.
Handles theme loading, switching, and persistence.
"""

import os
import json
from loguru import logger
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from modules.config.config import Config

class ThemeManager:
    """Manages application themes."""
    
    def __init__(self, app: QApplication, config: Config):
        """Initialize the theme manager.

        Args:
            app (QApplication): The main application instance.
            config (Config): The configuration manager instance.
        """
        self.app = app
        self.config = config
        self.themes = {}
        self.current_theme = None
        self.default_theme = "dark"
        
        # Initialize Windows DWM API constants
        try:
            import ctypes
            self.dwmapi = ctypes.windll.dwmapi
            self.DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        except Exception:
            self.dwmapi = None
            logger.warning("Windows DWM API not available")
        
        # Load themes from JSON file
        self.themes_file = os.path.join(os.path.dirname(__file__), 'themes.json')
        self.load_themes()
        logger.info(f"Loaded {len(self.themes)} themes from {self.themes_file}")

        # Set Fusion style which works better with custom themes
        self.app.setStyle('Fusion')

        # Apply theme from config or default
        theme_name = self.config.get('Window', 'theme', self.default_theme)
        self.apply_theme(theme_name)
        
        logger.info("Theme manager initialized")
        logger.debug(f"Themes file: {self.themes_file}")

    def load_themes(self):
        """Load themes from the themes.json file."""
        # Initialize default themes
        self.themes = {
            "light": self._get_default_light_theme(),
            "dark": self._get_default_dark_theme()
        }
        
        # Load custom themes from file
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r') as f:
                    custom_themes = json.load(f)
                    self.themes.update(custom_themes)
            except Exception as e:
                logger.error(f"Error loading themes: {str(e)}")
        else:
            logger.warning(f"Themes file not found: {self.themes_file}")
    
    def _get_default_light_theme(self):
        """Get the default light theme colors."""
        return {
            "name": "light",
            "window": "#ffffff",
            "windowText": "#2c3e50",
            "base": "#ffffff",
            "alternateBase": "#f8f9fa",
            "text": "#2c3e50",
            "button": "#f8f9fa",
            "buttonText": "#2c3e50",
            "brightText": "#ffffff",
            "light": "#ffffff",
            "midlight": "#f1f3f5",
            "dark": "#343a40",
            "mid": "#dee2e6",
            "shadow": "#adb5bd",
            "highlight": "#3498db",
            "highlightedText": "#ffffff",
            "link": "#3498db",
            "linkVisited": "#9b59b6"
        }
    
    def _get_default_dark_theme(self):
        """Get the default dark theme colors."""
        return {
            "name": "dark",
            "window": "#1a1a1a",
            "windowText": "#ecf0f1",
            "base": "#2c2c2c",
            "alternateBase": "#353535",
            "text": "#ecf0f1",
            "button": "#2c2c2c",
            "buttonText": "#ecf0f1",
            "brightText": "#ffffff",
            "light": "#404040",
            "midlight": "#353535",
            "dark": "#1a1a1a",
            "mid": "#2c2c2c",
            "shadow": "#000000",
            "highlight": "#3498db",
            "highlightedText": "#ffffff",
            "link": "#3498db",
            "linkVisited": "#9b59b6"
        }
    
    def _save_themes(self):
        """Save themes to the themes directory."""
        try:
            # Only save custom themes, not default ones
            custom_themes = {name: theme for name, theme in self.themes.items()
                           if name not in ["light", "dark"]}
            
            with open(self.themes_file, 'w') as f:
                json.dump(custom_themes, f, indent=4)
                
            logger.info(f"Saved {len(custom_themes)} custom themes to {self.themes_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving themes: {str(e)}")
            return False
    
    def get_available_themes(self):
        """Get a list of available theme names."""
        return list(self.themes.keys())
    
    def get_current_theme(self):
        """Get the current theme."""
        if not self.current_theme or self.current_theme not in self.themes:
            return self.themes[self.default_theme]
        return self.themes[self.current_theme]
    
    def set_window_dark_mode(self, window, is_dark):
        """Set dark mode for a specific window.
        
        Args:
            window: The window to set dark mode for
            is_dark (bool): Whether to enable dark mode
        """
        if not self.dwmapi:
            return
            
        try:
            import ctypes
            value = ctypes.c_int(is_dark)
            self.dwmapi.DwmSetWindowAttribute(
                int(window.winId()),
                self.DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception as e:
            logger.warning(f"Could not set window dark mode: {str(e)}")

    def apply_theme(self, theme_name):
        """Apply a theme to the application."""
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found")
            return False
        
        try:
            theme = self.themes[theme_name]
            palette = QPalette()
            
            # Map theme colors to palette roles
            role_map = {
                "window": QPalette.ColorRole.Window,
                "windowText": QPalette.ColorRole.WindowText,
                "base": QPalette.ColorRole.Base,
                "alternateBase": QPalette.ColorRole.AlternateBase,
                "text": QPalette.ColorRole.Text,
                "button": QPalette.ColorRole.Button,
                "buttonText": QPalette.ColorRole.ButtonText,
                "brightText": QPalette.ColorRole.BrightText,
                "light": QPalette.ColorRole.Light,
                "midlight": QPalette.ColorRole.Midlight,
                "dark": QPalette.ColorRole.Dark,
                "mid": QPalette.ColorRole.Mid,
                "shadow": QPalette.ColorRole.Shadow,
                "highlight": QPalette.ColorRole.Highlight,
                "highlightedText": QPalette.ColorRole.HighlightedText,
                "link": QPalette.ColorRole.Link,
                "linkVisited": QPalette.ColorRole.LinkVisited
            }
            
            # Apply colors to all color groups
            for theme_key, color_str in theme.items():
                if theme_key in role_map:
                    try:
                        color = QColor(color_str)
                        for group in [QPalette.ColorGroup.Active, 
                                    QPalette.ColorGroup.Inactive, 
                                    QPalette.ColorGroup.Disabled]:
                            palette.setColor(group, role_map[theme_key], color)
                    except Exception as e:
                        logger.error(f"Error setting color {theme_key}: {str(e)}")
                        return False
            
            # Apply palette
            self.app.setPalette(palette)
            
            # Update window dark mode based on window color brightness
            window_color = QColor(theme["window"])
            is_dark = window_color.lightness() < 128
            for window in self.app.topLevelWindows():
                self.set_window_dark_mode(window, is_dark)
            
            # Apply stylesheet
            stylesheet = f"""
                QWidget {{
                    background-color: {theme["window"]};
                }}
                QMenuBar {{
                    background-color: {theme["window"]};
                    color: {theme["windowText"]};
                    border: none;
                }}
                QMenuBar::item:selected {{
                    background-color: {theme["highlight"]};
                    color: {theme["highlightedText"]};
                }}
                QMenu {{
                    background-color: {theme["window"]};
                    color: {theme["windowText"]};
                    border: 1px solid {theme["mid"]};
                }}
                QMenu::item:selected {{
                    background-color: {theme["highlight"]};
                    color: {theme["highlightedText"]};
                }}
                QToolBar {{
                    background-color: {theme["window"]};
                    border: none;
                }}
                QStatusBar {{
                    background-color: {theme["window"]};
                    color: {theme["windowText"]};
                }}
            """
            
            self.app.setStyleSheet(stylesheet)
            self.current_theme = theme_name
            
            # Save to config immediately
            self.config.set('Window', 'theme', theme_name)
            self.config.save_config()
            
            return True
                
        except Exception as e:
            logger.error(f"Error applying theme {theme_name}: {str(e)}")
            return False
    
    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        if theme_name in self.themes:
            success = self.apply_theme(theme_name)
            if success:
                # Save to config
                self.config.set('Window', 'theme', theme_name)
                logger.info(f"Switched to theme: {theme_name}")
                return True
            
        logger.error(f"Failed to switch to theme: {theme_name}")
        return False
    
    def load_theme_from_file(self, file_path):
        """Load a theme from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                theme = json.load(f)
            
            # Validate theme
            if not isinstance(theme, dict):
                raise ValueError("Theme must be a dictionary")
            
            # Add theme
            name = os.path.splitext(os.path.basename(file_path))[0]
            self.themes[name] = theme
            self._save_themes()
            
            logger.info(f"Loaded theme from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading theme from {file_path}: {str(e)}")
            return False
    
    def export_theme(self, theme_name, file_path):
        """Export a theme to a JSON file."""
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found")
            return False
            
        try:
            with open(file_path, 'w') as f:
                json.dump(self.themes[theme_name], f, indent=4)
                
            logger.info(f"Exported theme {theme_name} to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting theme {theme_name}: {str(e)}")
            return False
    
    def create_theme(self, name, colors):
        """Create a new theme."""
        if name in self.themes:
            logger.error(f"Theme '{name}' already exists")
            return False
            
        try:
            # Validate colors
            for color in colors.values():
                if not self._is_valid_color(color):
                    raise ValueError(f"Invalid color: {color}")
            
            # Add theme
            self.themes[name] = colors
            self._save_themes()
            
            logger.info(f"Created new theme: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating theme {name}: {str(e)}")
            return False
    
    def delete_theme(self, name):
        """Delete a theme."""
        if name not in self.themes:
            logger.error(f"Theme '{name}' not found")
            return False
            
        if name in ["light", "dark"]:
            logger.error("Cannot delete default themes")
            return False
            
        try:
            del self.themes[name]
            self._save_themes()
            
            logger.info(f"Deleted theme: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting theme {name}: {str(e)}")
            return False
    
    def _is_valid_color(self, color_str):
        """Validate if a string is a valid color."""
        try:
            QColor(color_str)
            return True
        except:
            return False
