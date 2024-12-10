"""
Configuration management module.
"""
import configparser
import os
from typing import Any, Dict

from loguru import logger

class ConfigError(Exception):
    """Custom exception for configuration related errors."""

class Config:
    """Configuration class for PyQt6ify Pro."""

    def __init__(self, config_file: str = "tests/config/config.ini"):
        """Initialize the configuration.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._initializing = True  # Add flag to track initialization

        # Default settings
        self.default_config = {
            'Application': {
                'Name': 'PyQt6ify Pro Lite',
                'Version': '1.0.0.0',
                'Debug': 'False'
            },
            'About': {
                'Author': 'PyQt6ify Team',
                'Description': 'This is a powerful and feature-rich PyQt6 application template.',
                'Website': 'https://github.com/elirancv/PyQt6ify-Pro',
                'Icon': 'modules/resources/icons/app.png'
            },
            'Modules': {
                'logging': 'True',
                'database': 'True',
                'menu': 'True',
                'toolbar': 'True',
                'status_bar': 'True'
            },
            'Window': {
                'start_maximized': 'True',
                'screen_width': '1024',
                'screen_height': '768',
                'theme': 'light'
            }
        }

        self.load()
        self._initializing = False  # Reset flag after initialization

    def load(self) -> None:
        """Load configuration from file."""
        try:
            if not os.path.exists(self.config_file):
                logger.error(f"Configuration file not found: {self.config_file}")
                raise ConfigError(f"Configuration file not found: {self.config_file}")

            self.config.read(self.config_file, encoding='utf-8')
            logger.info("Configuration loaded successfully")

            # Ensure all required sections and options exist
            for section, options in self.default_config.items():
                if not self.config.has_section(section):
                    self.config.add_section(section)
                for option, value in options.items():
                    if not self.config.has_option(section, option):
                        self.config.set(section, option, value)

        except ConfigError:
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise ConfigError(f"Failed to load configuration: {str(e)}") from e

    def save(self) -> None:
        """Save configuration to file."""
        try:
            # Skip saving during initialization
            if self._initializing:
                return

            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise ConfigError(f"Failed to save configuration: {str(e)}") from e

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """Get a value from the configuration.

        Args:
            section (str): Section name.
            option (str): Option name.
            fallback (Any): Default value if section or option not found.

        Returns:
            Any: Configuration value.
        """
        try:
            if not self.config.has_section(section):
                return fallback
            return self.config.get(section, option, fallback=fallback)
        except configparser.Error as e:
            logger.error(f"Error getting config value: {str(e)}")
            return fallback

    def get_modules_enabled(self) -> Dict[str, bool]:
        """Get enabled/disabled status of modules.

        Returns:
            Dict[str, bool]: Dictionary of module names and their enabled status.
        """
        try:
            modules = self.config.items('Modules')
            return {name: self.getboolean('Modules', name) for name, _ in modules}
        except (configparser.Error, ValueError) as e:
            logger.error(f"Error getting modules enabled: {str(e)}")
            raise ConfigError(f"Error getting modules enabled: {str(e)}") from e

    def set_modules_enabled(self, modules: Dict[str, bool]) -> None:
        """Set enabled/disabled status of modules.

        Args:
            modules (Dict[str, bool]): Dictionary of module names and their enabled status.
        """
        try:
            if not self.config.has_section('Modules'):
                self.config.add_section('Modules')
            for name, enabled in modules.items():
                self.config.set('Modules', name, str(enabled))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error setting modules enabled: {str(e)}")
            raise ConfigError(f"Error setting modules enabled: {str(e)}") from e

    def get_about_info(self) -> Dict[str, str]:
        """Get about information.

        Returns:
            Dict[str, str]: Dictionary containing about information.
        """
        try:
            about = dict(self.config.items('About'))
            return about
        except configparser.Error as e:
            logger.error(f"Error getting about info: {str(e)}")
            raise ConfigError(f"Error getting about info: {str(e)}") from e

    def get_app_info(self) -> Dict[str, str]:
        """Get application information.

        Returns:
            Dict[str, str]: Dictionary containing application information.
        """
        try:
            app_info = dict(self.config.items('Application'))
            return app_info
        except configparser.Error as e:
            logger.error(f"Error getting app info: {str(e)}")
            raise ConfigError(f"Error getting app info: {str(e)}") from e

    def get_window_settings(self) -> Dict[str, Any]:
        """Get window settings.

        Returns:
            Dict[str, Any]: Dictionary containing window settings.
        """
        try:
            settings = dict(self.config.items('Window'))
            return settings
        except configparser.Error as e:
            logger.error(f"Error getting window settings: {str(e)}")
            raise ConfigError(f"Error getting window settings: {str(e)}") from e

    def set_window_settings(self, settings: Dict[str, Any]) -> None:
        """Set window settings.

        Args:
            settings (Dict[str, Any]): Dictionary containing window settings.
        """
        try:
            if not self.config.has_section('Window'):
                self.config.add_section('Window')
            for key, value in settings.items():
                self.config.set('Window', key, str(value))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error setting window settings: {str(e)}")
            raise ConfigError(f"Error setting window settings: {str(e)}") from e

    def getboolean(self, section: str, option: str) -> bool:
        """Get a boolean value from the configuration.

        Args:
            section (str): Section name.
            option (str): Option name.

        Returns:
            bool: Boolean value.

        Raises:
            ConfigError: If the section or option doesn't exist or value is invalid.
        """
        try:
            return self.config.getboolean(section, option)
        except configparser.NoSectionError as e:
            logger.error(f"Section not found: {section}")
            raise ConfigError(f"Section not found: {section}") from e
        except configparser.NoOptionError as e:
            logger.error(f"Option not found: {option} in section {section}")
            raise ConfigError(f"Option not found: {option} in section {section}") from e
        except ValueError as e:
            logger.error(f"Invalid boolean value in {section}.{option}: {str(e)}")
            raise ConfigError(f"Invalid boolean value in {section}.{option}: {str(e)}") from e

    def getint(self, section: str, option: str) -> int:
        """Get an integer value from the configuration.

        Args:
            section (str): Section name.
            option (str): Option name.

        Returns:
            int: Integer value.

        Raises:
            ConfigError: If the section or option doesn't exist or value is invalid.
        """
        try:
            return self.config.getint(section, option)
        except configparser.NoSectionError as e:
            logger.error(f"Section not found: {section}")
            raise ConfigError(f"Section not found: {section}") from e
        except configparser.NoOptionError as e:
            logger.error(f"Option not found: {option} in section {section}")
            raise ConfigError(f"Option not found: {option} in section {section}") from e
        except ValueError as e:
            logger.error(f"Invalid integer value in {section}.{option}: {str(e)}")
            raise ConfigError(f"Invalid integer value in {section}.{option}: {str(e)}") from e

    def set(self, section: str, option: str, value: Any) -> None:
        """Set a value in the configuration.

        Args:
            section (str): Section name.
            option (str): Option name.
            value (Any): Value to set.

        Raises:
            ConfigError: If the section doesn't exist.
        """
        try:
            if not self.config.has_section(section):
                raise ConfigError(f"Section not found: {section}")
            self.config.set(section, option, str(value))
            self.save()
        except configparser.Error as e:
            logger.error(f"Error setting value: {str(e)}")
            raise ConfigError(f"Error setting value: {str(e)}") from e

    @property
    def modules_enabled(self) -> Dict[str, bool]:
        """Get enabled/disabled status of modules."""
        try:
            return self.get_modules_enabled()
        except Exception as e:
            logger.error(f"Error getting modules configuration: {str(e)}")
            return {}

    @property
    def about_info(self) -> Dict[str, str]:
        """Get about dialog information."""
        try:
            return self.get_about_info()
        except Exception as e:
            logger.error(f"Error getting about info: {str(e)}")
            return {}

    @property
    def app_info(self) -> Dict[str, str]:
        """Get application information."""
        try:
            return self.get_app_info()
        except Exception as e:
            logger.error(f"Error getting application info: {str(e)}")
            return {}

    @property
    def application_settings(self) -> Dict[str, Any]:
        """Get application settings."""
        try:
            return {
                'name': self.get('Application', 'Name'),
                'version': self.get('Application', 'Version'),
                'debug': self.get('Application', 'Debug')
            }
        except Exception as e:
            logger.error(f"Error getting application settings: {str(e)}")
            return {}

    @property
    def window_settings(self) -> Dict[str, Any]:
        """Get window settings."""
        try:
            return self.get_window_settings()
        except Exception as e:
            logger.error(f"Error getting window settings: {str(e)}")
            return {}

    @window_settings.setter
    def window_settings(self, settings):
        """Set window settings."""
        try:
            self.set_window_settings(settings)
        except Exception as e:
            logger.error(f"Error setting window settings: {str(e)}")
            raise ConfigError(f"Failed to set window settings: {str(e)}") from e

    @property
    def about_settings(self) -> Dict[str, str]:
        """Get about settings."""
        try:
            return self.get_about_info()
        except Exception as e:
            logger.error(f"Error getting about settings: {str(e)}")
            return {}
