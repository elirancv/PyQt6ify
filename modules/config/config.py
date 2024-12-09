"""
Configuration module for PyQt6ify Pro.
"""

import os
import configparser
from loguru import logger

class ConfigError(Exception):
    """Custom exception for configuration related errors."""
    pass

class Config:
    """Configuration class for PyQt6ify Pro."""
    
    def __init__(self, config_file=None):
        """Initialize the configuration."""
        # If no config file specified, use default location
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
            
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
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
        
        self.load_config()
        
    def load_config(self):
        """Load the configuration from file."""
        try:
            if not os.path.exists(self.config_file):
                logger.error(f"Configuration file not found: {self.config_file}")
                raise ConfigError(f"Configuration file not found: {self.config_file}")
            
            self.config.read(self.config_file)
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
            raise ConfigError(f"Failed to load configuration: {str(e)}")
    
    def save_config(self):
        """Save the configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise ConfigError(f"Failed to save configuration: {str(e)}")
            
    def get(self, section, option, fallback=None):
        """Get a configuration value with fallback."""
        try:
            if not self.config.has_section(section):
                return fallback
            if not self.config.has_option(section, option):
                return fallback
            return self.config.get(section, option)
        except Exception as e:
            logger.error(f"Error getting config value [{section}][{option}]: {str(e)}")
            return fallback

    def getboolean(self, section, option):
        """Get a boolean configuration value."""
        try:
            if not self.config.has_section(section):
                raise ConfigError(f"Section not found: {section}")
            if not self.config.has_option(section, option):
                raise ConfigError(f"Option not found: {option} in section {section}")
            return self.config.getboolean(section, option)
        except Exception as e:
            logger.error(f"Error getting boolean config value [{section}][{option}]: {str(e)}")
            raise ConfigError(f"Failed to get boolean value: {str(e)}")

    def getint(self, section, option):
        """Get an integer configuration value."""
        try:
            if not self.config.has_section(section):
                raise ConfigError(f"Section not found: {section}")
            if not self.config.has_option(section, option):
                raise ConfigError(f"Option not found: {option} in section {section}")
            return self.config.getint(section, option)
        except Exception as e:
            logger.error(f"Error getting integer config value [{section}][{option}]: {str(e)}")
            raise ConfigError(f"Failed to get integer value: {str(e)}")

    def set(self, section, option, value):
        """Set a configuration value."""
        try:
            if not self.config.has_section(section):
                raise ConfigError(f"Section not found: {section}")
            self.config.set(section, option, str(value))
        except Exception as e:
            logger.error(f"Error setting config value [{section}][{option}]: {str(e)}")
            raise ConfigError(f"Failed to set configuration value: {str(e)}")

    @property
    def modules_enabled(self):
        """Get enabled modules configuration."""
        try:
            return {
                module: self.getboolean('Modules', module)
                for module in self.default_config['Modules'].keys()
            }
        except Exception as e:
            logger.error(f"Error getting modules configuration: {str(e)}")
            return self.default_config['Modules']
            
    @property
    def about_info(self):
        """Get about dialog information."""
        try:
            return {
                'name': self.get('Application', 'Name', fallback=self.default_config['Application']['Name']),
                'version': self.get('Application', 'Version', fallback=self.default_config['Application']['Version']),
                'author': self.get('About', 'Author', fallback=self.default_config['About']['Author']),
                'description': self.get('About', 'Description', fallback=self.default_config['About']['Description']),
                'website': self.get('About', 'Website', fallback=self.default_config['About']['Website']),
                'icon': self.get('About', 'Icon', fallback=self.default_config['About']['Icon'])
            }
        except Exception as e:
            logger.error(f"Error getting about info: {str(e)}")
            return {}
            
    @property
    def app_info(self):
        """Get application information."""
        try:
            return {
                'name': self.get('Application', 'Name', fallback=self.default_config['Application']['Name']),
                'version': self.get('Application', 'Version', fallback=self.default_config['Application']['Version']),
                'debug': self.getboolean('Application', 'Debug')
            }
        except Exception as e:
            logger.error(f"Error getting application info: {str(e)}")
            return {}
            
    @property
    def application_settings(self):
        """Get application settings."""
        return self.config['Application']
        
    @property
    def window_settings(self):
        """Get window settings."""
        try:
            return {
                'start_maximized': self.getboolean('Window', 'start_maximized'),
                'screen_width': self.getint('Window', 'screen_width'),
                'screen_height': self.getint('Window', 'screen_height'),
                'theme': self.get('Window', 'theme', fallback='light')
            }
        except Exception as e:
            logger.error(f"Error getting window settings: {str(e)}")
            return {}
            
    @window_settings.setter
    def window_settings(self, settings):
        """Set window settings."""
        try:
            if not self.config.has_section('Window'):
                self.config.add_section('Window')
                
            for key, value in settings.items():
                self.config.set('Window', key, str(value))
                
            self.save_config()
        except Exception as e:
            logger.error(f"Error setting window settings: {str(e)}")

    @property
    def about_settings(self):
        """Get about settings."""
        try:
            return {
                'author': self.get('About', 'Author', fallback=self.default_config['About']['Author']),
                'description': self.get('About', 'Description', fallback=self.default_config['About']['Description']),
                'website': self.get('About', 'Website', fallback=self.default_config['About']['Website']),
                'icon': self.get('About', 'Icon', fallback=self.default_config['About']['Icon'])
            }
        except Exception as e:
            logger.error(f"Error getting about settings: {str(e)}")
            return self.default_config['About']
