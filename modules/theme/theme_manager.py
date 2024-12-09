"""
Theme manager for handling application themes.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import logging
import json
import os
import traceback

class ThemeManager:
    """Manages application themes including loading, saving, and applying themes."""
    
    def __init__(self, config_dir="config"):
        """Initialize the theme manager."""
        self.config_dir = config_dir
        self.current_theme = "light"
        
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler('theme_manager.log'),
                logging.StreamHandler()
            ]
        )
        
        logging.info("Initializing ThemeManager")
        logging.debug(f"Config directory: {config_dir}")
        
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
    
    def _load_themes(self):
        """Load themes from the themes directory."""
        theme_file = os.path.join(self.config_dir, "themes.json")
        if os.path.exists(theme_file):
            try:
                with open(theme_file, 'r') as f:
                    custom_themes = json.load(f)
                self.themes.update(custom_themes)
                logging.info(f"Loaded {len(custom_themes)} custom themes")
            except Exception as e:
                logging.error(f"Error loading themes: {e}")
    
    def _save_themes(self):
        """Save themes to the themes directory."""
        theme_file = os.path.join(self.config_dir, "themes.json")
        try:
            # Only save custom themes (not built-in ones)
            custom_themes = {k: v for k, v in self.themes.items() 
                           if k not in ["light", "dark"]}
            with open(theme_file, 'w') as f:
                json.dump(custom_themes, f, indent=4)
            logging.info(f"Saved {len(custom_themes)} custom themes")
        except Exception as e:
            logging.error(f"Error saving themes: {e}")
    
    def get_available_themes(self):
        """Get a list of available theme names."""
        return list(self.themes.keys())
    
    def get_current_theme(self):
        """Get the name of the current theme."""
        return self.current_theme
    
    def apply_theme(self, theme_name):
        """Apply a theme to the application."""
        logging.info(f"Attempting to apply theme: {theme_name}")
        
        if theme_name not in self.themes:
            logging.error(f"Theme '{theme_name}' not found in available themes: {list(self.themes.keys())}")
            return False
        
        try:
            theme = self.themes[theme_name]
            palette = QPalette()
            logging.debug("Creating new QPalette")
            
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
            
            logging.debug("Applying colors to palette...")
            # Apply colors to all color groups
            for theme_key, color_str in theme.items():
                if theme_key in role_map:
                    try:
                        color = QColor(color_str)
                        logging.debug(f"Setting {theme_key} to {color_str}")
                        for group in [QPalette.ColorGroup.Active, 
                                    QPalette.ColorGroup.Inactive, 
                                    QPalette.ColorGroup.Disabled]:
                            palette.setColor(group, role_map[theme_key], color)
                    except Exception as e:
                        logging.error(f"Error setting color {theme_key}: {str(e)}")
                        return False
            
            # Apply palette first
            app = QApplication.instance()
            if not app:
                logging.error("No QApplication instance found")
                return False
                
            logging.debug("Applying palette to application")
            try:
                app.setPalette(palette)
            except Exception as e:
                logging.error(f"Error setting palette: {str(e)}")
                logging.error(traceback.format_exc())
                return False
            
            # Then apply stylesheet
            logging.debug("Building stylesheet")
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
                logging.debug("Applying stylesheet")
                app.setStyleSheet(stylesheet)
                self.current_theme = theme_name
                logging.info(f"Successfully applied theme: {theme_name}")
                return True
            except Exception as e:
                logging.error(f"Error applying stylesheet: {str(e)}")
                logging.error(traceback.format_exc())
                return False
                
        except Exception as e:
            logging.error(f"Error applying theme {theme_name}: {str(e)}")
            logging.error(traceback.format_exc())
            return False
    
    def create_theme(self, name, colors):
        """Create a new theme."""
        if name in self.themes:
            logging.error(f"Theme '{name}' already exists")
            return False
        
        self.themes[name] = colors
        self._save_themes()
        logging.info(f"Created new theme: {name}")
        return True
    
    def delete_theme(self, name):
        """Delete a theme."""
        if name not in self.themes:
            logging.error(f"Theme '{name}' not found")
            return False
        
        if name in ["light", "dark"]:
            logging.error("Cannot delete built-in themes")
            return False
        
        del self.themes[name]
        self._save_themes()
        logging.info(f"Deleted theme: {name}")
        return True
