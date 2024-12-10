"""
Configuration management module for PyQt6ify Pro.
"""

import configparser
import os
from typing import Any, Dict
from loguru import logger


class ConfigError(Exception):
    """Custom exception for configuration-related errors."""


class Config:
    """Configuration class for PyQt6ify Pro."""

    def __init__(self, config_file: str = "config/config.ini"):
        """Initialize the configuration.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._last_saved_state = None  # Track the last saved state to avoid redundant writes

        # Default settings
        self.default_config = {
            'Application': {
                'Name': 'PyQt6ify Pro',
                'Version': '1.0.0',
                'Debug': 'False',
            },
            'About': {
                'Author': 'PyQt6ify Team',
                'Description': 'Feature-rich PyQt6 application template.',
                'Website': 'https://github.com/elirancv/PyQt6ify-Pro',
                'Icon': 'resources/icons/app.png',
            },
            'Modules': {
                'logging': 'True',
                'database': 'True',
                'menu': 'True',
                'toolbar': 'True',
                'status_bar': 'True',
            },
            'Window': {
                'start_maximized': 'True',
                'screen_width': '1024',
                'screen_height': '768',
                'theme': 'light',
            },
        }

        # Load the configuration file
        self.load()

    def load(self) -> None:
        """Load configuration from file and ensure defaults are applied."""
        try:
            if not os.path.exists(self.config_file):
                logger.warning(f"Configuration file not found. Creating defaults: {self.config_file}")
                self._apply_defaults()
                self.save()
                return

            self.config.read(self.config_file, encoding='utf-8')
            self._apply_defaults()
            logger.info("Configuration loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise ConfigError(f"Failed to load configuration: {str(e)}") from e

    def _apply_defaults(self) -> None:
        """Ensure all default sections and options exist in the configuration."""
        for section, options in self.default_config.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option, value in options.items():
                if not self.config.has_option(section, option):
                    self.config.set(section, option, value)

    def save(self) -> None:
        """Save configuration to file, avoiding redundant writes."""
        try:
            current_state = self._current_state()
            if current_state == self._last_saved_state:
                logger.debug("No changes detected; skipping save")
                return

            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)

            self._last_saved_state = current_state
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise ConfigError(f"Failed to save configuration: {str(e)}") from e

    def _current_state(self) -> Dict[str, Dict[str, Any]]:
        """Get the current state of the configuration for comparison."""
        state = {}
        for section in self.config.sections():
            state[section] = dict(self.config.items(section))
        return state

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """Get a value from the configuration."""
        try:
            return self.config.get(section, option, fallback=fallback)
        except configparser.Error as e:
            logger.error(f"Error retrieving config value for {section}.{option}: {str(e)}")
            return fallback

    def getboolean(self, section: str, option: str) -> bool:
        """Get a boolean value from the configuration."""
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logger.error(f"Error getting boolean value: {section}.{option}: {str(e)}")
            raise ConfigError(f"Invalid boolean value for {section}.{option}: {str(e)}") from e

    def getint(self, section: str, option: str) -> int:
        """Get an integer value from the configuration."""
        try:
            return self.config.getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logger.error(f"Error getting integer value: {section}.{option}: {str(e)}")
            raise ConfigError(f"Invalid integer value for {section}.{option}: {str(e)}") from e

    def set(self, section: str, option: str, value: Any) -> None:
        """Set a value in the configuration."""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, str(value))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error setting value: {section}.{option} = {value}: {str(e)}")
            raise ConfigError(f"Failed to set value: {str(e)}") from e

    def get_modules_enabled(self) -> Dict[str, bool]:
        """Get enabled/disabled status of modules."""
        try:
            return {name: self.getboolean('Modules', name) for name, _ in self.config.items('Modules')}
        except configparser.Error as e:
            logger.error(f"Error retrieving module statuses: {str(e)}")
            raise ConfigError(f"Error retrieving module statuses: {str(e)}") from e

    def set_modules_enabled(self, modules: Dict[str, bool]) -> None:
        """Set enabled/disabled status of modules."""
        try:
            if not self.config.has_section('Modules'):
                self.config.add_section('Modules')
            for name, enabled in modules.items():
                self.config.set('Modules', name, str(enabled))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error setting modules: {str(e)}")
            raise ConfigError(f"Error setting modules: {str(e)}") from e

    def get_window_settings(self) -> Dict[str, Any]:
        """Get window settings."""
        return {key: self.get('Window', key, fallback=None) for key in self.default_config['Window']}

    def set_window_settings(self, settings: Dict[str, Any]) -> None:
        """Set window settings."""
        try:
            if not self.config.has_section('Window'):
                self.config.add_section('Window')
            for key, value in settings.items():
                self.config.set('Window', key, str(value))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error updating window settings: {str(e)}")
            raise ConfigError(f"Failed to update window settings: {str(e)}") from e

    @property
    def about_info(self) -> Dict[str, str]:
        """Get information for the About dialog."""
        try:
            return {key: self.get('About', key, fallback='') for key in self.default_config['About']}
        except Exception as e:
            logger.error(f"Error retrieving about info: {e}")
            return {}
