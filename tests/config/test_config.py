"""
Test configuration module.
"""
import configparser
import os
import pytest
from modules.config import Config, ConfigError

def test_config_save_load(tmp_path):
    """Test saving and loading configuration."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))
    config.set('Test', 'key', 'value')
    config.save()

    # Load in a new instance
    config2 = Config(str(config_file))
    assert config2.get('Test', 'key') == 'value'

def test_modules_enabled(tmp_path):
    """Test getting and setting modules enabled."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test initial state
    modules = config.get_modules_enabled()
    assert isinstance(modules, dict)

    # Test setting modules
    new_modules = {'test_module': True}
    config.set_modules_enabled(new_modules)
    assert config.get_modules_enabled()['test_module'] is True

def test_about_info(tmp_path):
    """Test getting about information."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Set some about info
    config.set('About', 'author', 'Test Author')
    config.set('About', 'version', '1.0.0')

    # Get about info
    about = config.get_about_info()
    assert about['author'] == 'Test Author'
    assert about['version'] == '1.0.0'

def test_app_info(tmp_path):
    """Test getting application information."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Set some app info
    config.set('Application', 'name', 'Test App')
    config.set('Application', 'version', '1.0.0')

    # Get app info
    app = config.get_app_info()
    assert app['name'] == 'Test App'
    assert app['version'] == '1.0.0'

def test_window_settings(tmp_path):
    """Test getting and setting window settings."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test setting window settings
    settings = {'width': '800', 'height': '600'}
    config.set_window_settings(settings)

    # Test getting window settings
    loaded = config.get_window_settings()
    assert loaded['width'] == '800'
    assert loaded['height'] == '600'

def test_error_handling(tmp_path):
    """Test error handling."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test getting non-existent section
    assert config.get('NonExistent', 'key') is None

    # Test getting non-existent option
    assert config.get('Test', 'nonexistent') is None

def test_config_initialization(tmp_path):
    """Test configuration initialization."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test default values
    assert config.get('Application', 'name') is None
    assert config.get('Application', 'version') is None
    assert config.get('About', 'author') is None

def test_config_set_get(tmp_path):
    """Test setting and getting configuration values."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    config.set('Test', 'key', 'value')
    assert config.get('Test', 'key') == 'value'

def test_config_invalid_section(tmp_path):
    """Test handling invalid section."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    assert config.get('InvalidSection', 'key') is None
    assert config.get('InvalidSection', 'another_key') is None

def test_config_invalid_key(tmp_path):
    """Test handling invalid key."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    config.set('Test', 'key', 'value')
    assert config.get('Test', 'invalid_key') is None
    assert config.get('Test', 'another_invalid_key') is None

def test_config_invalid_bool(tmp_path):
    """Test handling invalid boolean value."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    config.set('Test', 'bool', 'invalid')
    with pytest.raises(ConfigError):
        config.getboolean('Test', 'bool')

def test_config_invalid_int(tmp_path):
    """Test handling invalid integer value."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    config.set('Test', 'int', 'invalid')
    with pytest.raises(ConfigError):
        config.getint('Test', 'int')

def test_config_load_error(tmp_path):
    """Test handling load error."""
    config_file = tmp_path / "test_config.ini"

    # Create an invalid config file
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('[Invalid Config')

    with pytest.raises(ConfigError):
        config = Config(str(config_file))
        config.load()

def test_config_save_error(tmp_path):
    """Test handling save error."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Make the file read-only
    config.save()  # First save normally
    os.chmod(config_file, 0o444)  # Make read-only

    with pytest.raises(ConfigError):
        config.save()

def test_config_load_file_not_found():
    """Test handling file not found error."""
    with pytest.raises(ConfigError):
        config = Config("nonexistent.ini")
        config.load()

def test_config_get_section_error(tmp_path):
    """Test handling section error in get."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    assert config.get('NonExistentSection', 'key') is None
    assert config.get('AnotherNonExistentSection', 'key') is None

def test_config_getboolean_section_error(tmp_path):
    """Test handling section error in getboolean."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getboolean('NonExistentSection', 'key')

def test_config_getint_section_error(tmp_path):
    """Test handling section error in getint."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getint('NonExistentSection', 'key')

def test_config_get_error_handling(tmp_path):
    """Test error handling in get method."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test with invalid config file
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('[Invalid Config')

    assert config.get('Section', 'key') is None

def test_config_getboolean_error_handling(tmp_path):
    """Test error handling in getboolean method."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getboolean('NonExistentSection', 'key')

def test_config_getint_error_handling(tmp_path):
    """Test error handling in getint method."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Create invalid config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('[Test]\nkey = invalid')

    with pytest.raises(ConfigError):
        config.getint('Test', 'key')

def test_config_set_error_handling(tmp_path):
    """Test error handling in set method."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Create invalid config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('[Invalid Config')

    with pytest.raises(ConfigError):
        config.set('Test', 'key', 'value')

def test_config_get_error_complete(tmp_path):
    """Test complete error handling in get method."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    assert config.get('NonExistentSection', 'key') is None

def test_config_getboolean_section_not_found(tmp_path):
    """Test getboolean with non-existent section."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getboolean('NonExistentSection', 'key')

def test_config_getboolean_option_not_found(tmp_path):
    """Test getboolean with non-existent option."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getboolean('Test', 'nonexistent')

def test_config_getint_section_not_found(tmp_path):
    """Test getint with non-existent section."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getint('NonExistentSection', 'key')

def test_config_getint_option_not_found(tmp_path):
    """Test getint with non-existent option."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.getint('Test', 'nonexistent')

def test_config_getint_invalid_value(tmp_path):
    """Test getint with invalid value."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    config.set('Test', 'key', 'invalid')
    with pytest.raises(ConfigError):
        config.getint('Test', 'key')

def test_config_set_section_not_found(tmp_path):
    """Test set with non-existent section."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.set('NonExistentSection', 'key', 'value')

@pytest.fixture
def config_setup(tmp_path):
    """Setup a test configuration file."""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    return Config(str(config_file))

@pytest.fixture
def empty_config(tmp_path):
    """Setup a test configuration file without default sections."""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    config = Config(str(config_file))
    config.config = configparser.ConfigParser()  # Reset to empty config
    return config

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.load()  # Load the configuration upon initialization

    def load(self):
        try:
            self.config.read(self.file_path)
        except configparser.Error as e:
            raise ConfigError(f"Failed to load configuration: {e}")

    def get_about_info(self):
        about_info = {}
        if 'About' in self.config.sections():
            about_info['author'] = self.config.get('About', 'author', fallback=None)
            about_info['version'] = self.config.get('About', 'version', fallback=None)
        return about_info

    def get_app_info(self):
        app_info = {}
        if 'Application' in self.config.sections():
            app_info['name'] = self.config.get('Application', 'name', fallback=None)
            app_info['version'] = self.config.get('Application', 'version', fallback=None)
        return app_info

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as config_file:
            self.config.write(config_file)

    def get(self, section, option):
        if self.config.has_section(section):
            return self.config.get(section, option, fallback=None)
        return None

    def get_modules_enabled(self):
        modules = {}
        if 'Modules' in self.config.sections():
            for option in self.config.options('Modules'):
                modules[option] = self.config.getboolean('Modules', option)
        return modules

    def set_modules_enabled(self, value):
        if not self.config.has_section('Modules'):
            self.config.add_section('Modules')
        for module, enabled in value.items():
            self.config.set('Modules', module, str(enabled))

    def get_window_settings(self):
        settings = {}
        if 'Window' in self.config.sections():
            for option in self.config.options('Window'):
                settings[option] = self.config.get('Window', option)
        return settings

    def set_window_settings(self, settings):
        if not self.config.has_section('Window'):
            self.config.add_section('Window')
        for setting, val in settings.items():
            self.config.set('Window', setting, val)

    def getboolean(self, section, option):
        if self.config.has_section(section):
            return self.config.getboolean(section, option, fallback=None)
        raise ConfigError(f"Section '{section}' not found")

    def getint(self, section, option):
        if self.config.has_section(section):
            return self.config.getint(section, option, fallback=None)
        raise ConfigError(f"Section '{section}' not found")
