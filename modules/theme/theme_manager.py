"""
Theme manager for PyQt6ify Pro.
Handles theme loading, switching, and persistence.
"""

import os
import json
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from config.app_config import Config

# Configure logging to use the centralized app.log
logger = logging.getLogger(__name__)

class ThemeManager:
    """Manages application themes."""
    
    def __init__(self, app: QApplication, config: Config):
        """Initialize the theme manager."""
        self.app = app
        self.config = config
        self.current_theme = "light"  # Default theme
        
        logger.info("Theme manager initialized")
        logger.debug(f"Config directory: {config.config_dir}")
        
        self.themes = {
            "light": {
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
            },
            "dark": {
                "window": "#1a1a1a",
                "windowText": "#ecf0f1",
                "base": "#242424",
                "alternateBase": "#2a2a2a",
                "text": "#ecf0f1",
                "button": "#2d2d2d",
                "buttonText": "#ecf0f1",
                "brightText": "#ffffff",
                "light": "#3d3d3d",
                "midlight": "#2d2d2d",
                "dark": "#1a1a1a",
                "mid": "#353535",
                "shadow": "#141414",
                "highlight": "#3498db",
                "highlightedText": "#ffffff",
                "link": "#3498db",
                "linkVisited": "#9b59b6"
            }
        }
        
        self._load_themes()
        self._load_saved_theme()
    
    def _load_themes(self):
        """Load themes from the themes directory."""
        theme_file = os.path.join(self.config.config_dir, "themes.json")
        if os.path.exists(theme_file):
            try:
                with open(theme_file, 'r') as f:
                    custom_themes = json.load(f)
                self.themes.update(custom_themes)
                logger.info(f"Loaded {len(custom_themes)} custom themes")
            except Exception as e:
                logger.error(f"Error loading themes: {e}")
    
    def _save_themes(self):
        """Save themes to the themes directory."""
        theme_file = os.path.join(self.config.config_dir, "themes.json")
        try:
            # Only save custom themes (not built-in ones)
            custom_themes = {k: v for k, v in self.themes.items() 
                           if k not in ["light", "dark"]}
            with open(theme_file, 'w') as f:
                json.dump(custom_themes, f, indent=4)
            logger.info(f"Saved {len(custom_themes)} custom themes")
        except Exception as e:
            logger.error(f"Error saving themes: {e}")
    
    def get_available_themes(self):
        """Get a list of available theme names."""
        return list(self.themes.keys())
    
    def get_current_theme(self):
        """Get the name of the current theme."""
        return self.current_theme
    
    def apply_theme(self, theme_name):
        """Apply a theme to the application."""
        logger.info(f"Attempting to apply theme: {theme_name}")
        
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found in available themes: {list(self.themes.keys())}")
            return False
        
        try:
            theme = self.themes[theme_name]
            palette = QPalette()
            logger.debug("Creating new QPalette")
            
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
            
            logger.debug("Applying colors to palette...")
            # Apply colors to all color groups
            for theme_key, color_str in theme.items():
                if theme_key in role_map:
                    try:
                        color = QColor(color_str)
                        logger.debug(f"Setting {theme_key} to {color_str}")
                        for group in [QPalette.ColorGroup.Active, 
                                    QPalette.ColorGroup.Inactive, 
                                    QPalette.ColorGroup.Disabled]:
                            palette.setColor(group, role_map[theme_key], color)
                    except Exception as e:
                        logger.error(f"Error setting color {theme_key}: {str(e)}")
                        return False
            
            # Apply palette first
            logger.debug("Applying palette to application")
            try:
                self.app.setPalette(palette)
            except Exception as e:
                logger.error(f"Error setting palette: {str(e)}")
                logger.error(traceback.format_exc())
                return False
            
            # Then apply stylesheet
            logger.debug("Building stylesheet")
            stylesheet = f"""
                QMenuBar {{
                    background-color: {theme["window"]};
                    color: {theme["windowText"]};
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
            """
            
            try:
                logger.debug("Applying stylesheet")
                self.app.setStyleSheet(stylesheet)
                self.current_theme = theme_name
                logger.info(f"Successfully applied theme: {theme_name}")
                return True
            except Exception as e:
                logger.error(f"Error applying stylesheet: {str(e)}")
                logger.error(traceback.format_exc())
                return False
                
        except Exception as e:
            logger.error(f"Error applying theme {theme_name}: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        if theme_name in self.themes:
            success = self.apply_theme(theme_name)
            if success:
                # Store the theme preference in the config file
                theme_file = os.path.join(self.config.config_dir, "theme.txt")
                try:
                    with open(theme_file, 'w') as f:
                        f.write(theme_name)
                    logger.info(f"Saved theme preference: {theme_name}")
                except Exception as e:
                    logger.error(f"Error saving theme preference: {e}")
            return success
        return False

    def load_theme_from_file(self, file_path):
        """Load a theme from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                theme_data = json.load(f)
                
            if isinstance(theme_data, dict):
                if "name" in theme_data and "colors" in theme_data:
                    theme_name = theme_data["name"]
                    theme_colors = theme_data["colors"]
                    self.themes[theme_name] = theme_colors
                    self._save_themes()
                    logger.info(f"Successfully loaded theme {theme_name} from {file_path}")
                    return True
            logger.error("Invalid theme file format")
            return False
        except Exception as e:
            logger.error(f"Error loading theme from file: {e}")
            return False

    def _load_saved_theme(self):
        """Load the previously saved theme."""
        theme_file = os.path.join(self.config.config_dir, "theme.txt")
        try:
            if os.path.exists(theme_file):
                with open(theme_file, 'r') as f:
                    saved_theme = f.read().strip()
                if saved_theme in self.themes:
                    self.apply_theme(saved_theme)
                    logger.info(f"Loaded saved theme: {saved_theme}")
        except Exception as e:
            logger.error(f"Error loading saved theme: {e}")

    def _is_valid_color(self, color_str):
        """Validate if a string is a valid color."""
        try:
            color = QColor(color_str)
            return color.isValid() and (
                color_str.startswith('#') and 
                len(color_str) in [4, 7, 9]  # #RGB, #RRGGBB, or #RRGGBBAA
            )
        except:
            return False

    def export_theme(self, theme_name, file_path):
        """Export a theme to a JSON file."""
        if theme_name not in self.themes:
            logger.error(f"Theme {theme_name} not found")
            return False
            
        theme_data = {
            "name": theme_name,
            "colors": self.themes[theme_name]
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(theme_data, f, indent=4)
            logger.info(f"Successfully exported theme {theme_name} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting theme: {e}")
            return False

    def create_theme(self, name, colors):
        """Create a new theme."""
        if name in self.themes:
            logger.error(f"Theme '{name}' already exists")
            return False
        
        self.themes[name] = colors
        self._save_themes()
        logger.info(f"Created new theme: {name}")
        return True
    
    def delete_theme(self, name):
        """Delete a theme."""
        if name not in self.themes:
            logger.error(f"Theme '{name}' not found")
            return False
        
        if name in ["light", "dark"]:
            logger.error("Cannot delete built-in themes")
            return False
        
        del self.themes[name]
        self._save_themes()
        logger.info(f"Deleted theme: {name}")
        return True
