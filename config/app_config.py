"""
Configuration management for PyQt6ify Pro.
"""

import configparser
import os
import logging
from pathlib import Path

class ConfigError(Exception):
    """Custom exception for configuration related errors."""
    pass

class Config:
    def __init__(self, config_file='config/config.ini'):
        """
        Initialize the Config class.
        
        Args:
            config_file (str): Path to the configuration file.
        
        Raises:
            ConfigError: If configuration file cannot be loaded or created.
        """
        # Store config directory
        self.config_dir = os.path.dirname(os.path.abspath(config_file))
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        # About details and module settings are controlled from app_config.py
        self.about_info = {
            'name': 'PyQt6ify Pro',
            'version': '1.0.0',
            'author': 'PyQt6ify Team',
            'website': 'https://github.com/PyQt6ify',
            'icon': os.path.join('resources', 'icons', 'app_icon.png')
        }

        # Default module settings
        self.modules = {
            'logging': True,
            'database': True,
            'menu': True,
            'toolbar': True,
            'status_bar': True
        }

        # Default settings
        self.default_config = {
            'APP': {
                'start_maximized': 'True',
                'screen_width': '1024',
                'screen_height': '768',
                'theme': 'light'  # Add default theme setting
            }
        }

        # Ensure resources directory exists
        self._ensure_resource_paths()
        
        # Load or create config file
        try:
            if not os.path.exists(self.config_file):
                self.create_default_config()
            self.load_config()
        except Exception as e:
            raise ConfigError(f"Failed to initialize configuration: {str(e)}")

    def _ensure_resource_paths(self):
        """
        Ensure all required resource directories exist.
        Creates them if they don't exist.
        """
        paths = [
            'resources',
            'resources/icons',
            'logs',
            'config',
            'database'
        ]
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)

    def load_config(self):
        """
        Load the configuration file and validate its contents.
        
        Raises:
            ConfigError: If configuration file is invalid or cannot be read.
        """
        try:
            if not self.config.read(self.config_file):
                raise ConfigError(f"Could not read configuration file: {self.config_file}")
            
            # Validate required sections and options
            required_settings = {
                'APP': ['start_maximized', 'screen_width', 'screen_height', 'theme']
            }
            
            for section, options in required_settings.items():
                if not self.config.has_section(section):
                    raise ConfigError(f"Missing required section: {section}")
                for option in options:
                    if not self.config.has_option(section, option):
                        raise ConfigError(f"Missing required option: {option} in section {section}")
            
            logging.info(f"Configuration loaded successfully from {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to load config: {str(e)}")
            self.create_default_config()

    def create_default_config(self):
        """
        Create a default configuration file if it does not exist or is invalid.
        
        Raises:
            ConfigError: If default configuration cannot be created.
        """
        try:
            self.config['APP'] = self.default_config['APP']
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
            logging.info(f"Default configuration created at: {self.config_file}")
        except Exception as e:
            raise ConfigError(f"Failed to create default configuration: {str(e)}")

    def get_about_info(self, key):
        """
        Get about information.
        
        Args:
            key (str): The key to retrieve from about_info.
        
        Returns:
            str: The value associated with the key or "Unknown" if not found.
        """
        if key not in self.about_info:
            logging.warning(f"Requested unknown about_info key: {key}")
        return self.about_info.get(key, "Unknown")

    def get_app_setting(self, option, fallback=None):
        """
        Get a setting from the APP section.
        
        Args:
            option (str): The option to retrieve.
            fallback: The fallback value if option is not found.
        
        Returns:
            The configuration value or fallback.
        """
        try:
            return self.config.get('APP', option, fallback=fallback)
        except Exception as e:
            logging.error(f"Error retrieving app setting {option}: {str(e)}")
            return fallback

    def is_module_enabled(self, module):
        """
        Check if a module is enabled.
        
        Args:
            module (str): The module to check.
        
        Returns:
            bool: True if the module is enabled, False otherwise.
        """
        if module not in self.modules:
            logging.warning(f"Checking status of unknown module: {module}")
        return self.modules.get(module, False)

    def get(self, section, option, fallback=None):
        """
        Get a configuration value with fallback.
        
        Args:
            section (str): The configuration section.
            option (str): The option within the section.
            fallback: The fallback value if not found.
        
        Returns:
            The configuration value or fallback.
        """
        try:
            return self.config.get(section, option, fallback=fallback)
        except Exception as e:
            logging.error(f"Error retrieving config value {section}.{option}: {str(e)}")
            return fallback
            
    def set_app_setting(self, option, value):
        """
        Set a setting in the APP section and save to file.
        
        Args:
            option (str): The option to set.
            value: The value to set.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if not self.config.has_section('APP'):
                self.config.add_section('APP')
            
            self.config.set('APP', option, str(value))
            
            # Save changes to file
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
                
            logging.info(f"Successfully set app setting {option}={value}")
            return True
            
        except Exception as e:
            logging.error(f"Error setting app setting {option}: {str(e)}")
            return False
