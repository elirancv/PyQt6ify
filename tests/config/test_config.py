"""
Test configuration module functionality.
"""

import os
import pytest
import configparser
from modules.config.config import Config, ConfigError

def test_config_initialization():
    """Test that Config can be initialized with default values"""
    config = Config()
    assert config.get('Application', 'Name') == 'PyQt6ify Pro'
    assert config.get('Application', 'Version') == '1.0.0'
    assert config.get('Application', 'Debug') == 'True'

def test_config_set_get():
    """Test setting and getting config values"""
    config = Config()
    config.set('Application', 'Name', 'Test App')
    assert config.get('Application', 'Name') == 'Test App'

def test_config_save_load(tmp_path):
    """Test saving and loading config file"""
    # Create a new config file
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = PyQt6ify Pro\nVersion = 1.0.0\n")
    
    # Load the config
    config = Config(str(config_file))
    config.set('Application', 'Name', 'Test App')
    config.save_config()
    
    # Load the config in a new instance
    config2 = Config(str(config_file))
    assert config2.get('Application', 'Name') == 'Test App'

def test_config_invalid_section():
    """Test getting value from invalid section"""
    config = Config()
    # Should return fallback value for invalid section
    assert config.get('InvalidSection', 'Key', fallback='default') == 'default'
    assert config.get('InvalidSection', 'Key') is None  # None is default fallback

def test_config_invalid_key():
    """Test getting invalid key from valid section"""
    config = Config()
    # Should return fallback value for invalid key
    assert config.get('Application', 'InvalidKey', fallback='default') == 'default'
    assert config.get('Application', 'InvalidKey') is None  # None is default fallback

def test_config_boolean_values():
    """Test getting boolean values"""
    config = Config()
    assert config.getboolean('Application', 'Debug') is True

def test_config_int_values():
    """Test getting integer values"""
    config = Config()
    config.set('Application', 'TestInt', '42')
    assert config.getint('Application', 'TestInt') == 42

def test_config_invalid_bool():
    """Test getting invalid boolean value"""
    config = Config()
    with pytest.raises(ConfigError):
        config.getboolean('Application', 'Name')

def test_config_invalid_int():
    """Test getting invalid integer value"""
    config = Config()
    with pytest.raises(ConfigError):
        config.getint('Application', 'Name')

def test_modules_enabled(tmp_path):
    """Test getting enabled modules configuration"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Modules]\nlogging = True\ndatabase = False\nmenu = True\n")
    
    config = Config(str(config_file))
    modules = config.modules_enabled
    assert isinstance(modules, dict)
    assert modules['logging'] is True
    assert modules['database'] is False
    assert modules['menu'] is True

def test_about_info(tmp_path):
    """Test getting about dialog information"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\nDescription = Test Description\n")
    
    config = Config(str(config_file))
    info = config.about_info
    assert isinstance(info, dict)
    assert info['author'] == 'Test Author'
    assert info['description'] == 'Test Description'

def test_app_info(tmp_path):
    """Test getting application information"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nVersion = 2.0.0\n")
    
    config = Config(str(config_file))
    info = config.app_info
    assert info['name'] == 'Test App'
    assert info['version'] == '2.0.0'

def test_app_info_error(tmp_path):
    """Test error handling in app_info"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[InvalidSection]\nKey = Value\n")
    
    config = Config(str(config_file))
    info = config.app_info
    assert isinstance(info, dict)
    # Should use default values when section is missing
    assert info['name'] == config.default_config['Application']['Name']
    assert info['version'] == config.default_config['Application']['Version']
    assert info['debug'] is False

def test_app_info_error_complete(tmp_path, mocker):
    """Test complete error handling in app_info"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock get and getboolean to raise errors
    mocker.patch.object(config, 'get', side_effect=Exception("Mock error"))
    mocker.patch.object(config, 'getboolean', side_effect=Exception("Mock error"))
    
    # Should return empty dict on error
    info = config.app_info
    assert isinstance(info, dict)
    assert len(info) == 0

def test_application_settings(tmp_path):
    """Test getting application settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nDebug = True\n")
    
    config = Config(str(config_file))
    settings = config.application_settings
    assert settings['name'] == 'Test App'
    assert settings['debug'] == 'True'  # Debug is stored as string

def test_application_settings_error_complete(tmp_path, mocker):
    """Test complete error handling in application_settings"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock get to raise an error
    mocker.patch.object(config, 'get', side_effect=Exception("Mock error"))
    
    # Should return empty dict on error
    settings = config.application_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0

def test_window_settings(tmp_path):
    """Test getting and setting window settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nstart_maximized = True\n")
    
    config = Config(str(config_file))
    
    # Test getting window settings
    settings = config.window_settings
    assert isinstance(settings, dict)
    assert settings['start_maximized'] is True
    
    # Test setting window settings
    new_settings = {
        'start_maximized': False,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'dark'
    }
    config.window_settings = new_settings
    
    # Verify settings were saved
    settings = config.window_settings
    assert settings['start_maximized'] is False
    assert settings['screen_width'] == 800
    assert settings['screen_height'] == 600
    assert settings['theme'] == 'dark'

def test_window_settings_error(tmp_path):
    """Test error handling in window settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[InvalidSection]\nKey = Value\n")
    
    config = Config(str(config_file))
    settings = config.window_settings
    assert isinstance(settings, dict)
    # Should use default values when section is missing
    assert settings['start_maximized'] is True
    assert settings['screen_width'] == 1024
    assert settings['screen_height'] == 768
    assert settings['theme'] == 'light'

def test_window_settings_section_error(tmp_path):
    """Test error handling in window settings when section is missing"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()  # Create empty file
    
    config = Config(str(config_file))
    settings = config.window_settings
    assert isinstance(settings, dict)
    # Should use default values when section is missing
    assert settings['start_maximized'] is True
    assert settings['screen_width'] == 1024
    assert settings['screen_height'] == 768
    assert settings['theme'] == 'light'

def test_window_settings_setter_section_error(tmp_path):
    """Test error handling in window settings setter when section is missing"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()  # Create empty file
    
    config = Config(str(config_file))
    settings = {
        'start_maximized': False,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'dark'
    }
    
    # Should create section and set values
    config.window_settings = settings
    
    # Verify settings were saved
    saved_settings = config.window_settings
    assert saved_settings['start_maximized'] is False
    assert saved_settings['screen_width'] == 800
    assert saved_settings['screen_height'] == 600
    assert saved_settings['theme'] == 'dark'

def test_window_settings_save_error_complete(tmp_path, mocker):
    """Test complete error handling in window_settings setter"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock save_config to raise an error
    mocker.patch.object(config, 'save_config', side_effect=ConfigError("Mock error"))
    
    # Should raise ConfigError
    with pytest.raises(ConfigError, match="Failed to set window settings"):
        config.window_settings = {'start_maximized': True}

def test_about_settings(tmp_path):
    """Test getting about settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\nDescription = Test Description\n")
    
    config = Config(str(config_file))
    settings = config.about_settings
    assert settings['author'] == 'Test Author'
    assert settings['description'] == 'Test Description'

def test_about_settings_error(tmp_path):
    """Test error handling in about settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[InvalidSection]\nKey = Value\n")
    
    config = Config(str(config_file))
    settings = config.about_settings
    assert isinstance(settings, dict)
    # Should use default values
    assert settings['author'] == config.default_config['About']['Author']
    assert settings['description'] == config.default_config['About']['Description']

def test_modules_enabled_error(tmp_path):
    """Test error handling in modules_enabled"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[InvalidSection]\nKey = Value\n")
    
    config = Config(str(config_file))
    modules = config.modules_enabled
    assert isinstance(modules, dict)
    # Should use default values when section is missing
    for key in config.default_config['Modules']:
        assert modules[key] == (config.default_config['Modules'][key].lower() == 'true')

def test_about_info(tmp_path):
    """Test getting about dialog information"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\nDescription = Test Description\n")
    
    config = Config(str(config_file))
    info = config.about_info
    assert isinstance(info, dict)
    assert info['author'] == 'Test Author'
    assert info['description'] == 'Test Description'

def test_about_info_error(tmp_path):
    """Test error handling in about_info"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[InvalidSection]\nKey = Value\n")
    
    config = Config(str(config_file))
    info = config.about_info
    assert isinstance(info, dict)
    # Should use default values when section is missing
    assert info['author'] == config.default_config['About']['Author']
    assert info['description'] == config.default_config['About']['Description']
    assert info['website'] == config.default_config['About']['Website']
    assert info['icon'] == config.default_config['About']['Icon']

def test_window_settings_error_complete(tmp_path):
    """Test complete error handling in window_settings setter"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Invalid settings should be accepted and saved
    invalid_settings = {
        'invalid_key': 'value'
    }
    
    config.window_settings = invalid_settings
    settings = config.window_settings
    assert isinstance(settings, dict)
    
    # Compare with default values, converting strings to appropriate types
    defaults = config.default_config['Window']
    assert settings['start_maximized'] == (defaults['start_maximized'].lower() == 'true')
    assert settings['screen_width'] == int(defaults['screen_width'])
    assert settings['screen_height'] == int(defaults['screen_height'])
    assert settings['theme'] == defaults['theme']

def test_config_load_error(tmp_path, mocker):
    """Test error handling when loading config file fails"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()  # Create empty file
    
    config = Config(str(config_file))
    
    # Mock read to raise an error
    mocker.patch.object(config.config, 'read', side_effect=Exception("Mock error"))
    
    with pytest.raises(ConfigError, match="Failed to load configuration"):
        config.load_config()

def test_config_save_error(tmp_path, mocker):
    """Test error handling when saving config file fails"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()  # Create empty file
    
    config = Config(str(config_file))
    
    # Mock write to raise an error
    mocker.patch.object(config.config, 'write', side_effect=Exception("Mock error"))
    
    with pytest.raises(ConfigError, match="Failed to save configuration"):
        config.save_config()

def test_window_settings_setter_error(tmp_path):
    """Test error handling when setting window settings fails"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Create a read-only file
    read_only_file = tmp_path / "read_only.ini"
    read_only_file.touch()
    os.chmod(read_only_file, 0o444)  # Read-only file
    
    # Try to save to the read-only file
    config.config_file = str(read_only_file)
    settings = {
        'start_maximized': False,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'dark'
    }
    
    # Should handle error when saving settings
    with pytest.raises(ConfigError, match="Failed to set window settings"):
        config.window_settings = settings
    
    # Clean up
    os.chmod(read_only_file, 0o777)  # Restore permissions

def test_config_load_file_not_found():
    """Test loading nonexistent config file."""
    with pytest.raises(ConfigError, match="Configuration file not found: nonexistent.ini"):
        Config("nonexistent.ini")

def test_config_get_section_error(tmp_path):
    """Test error handling when getting value from nonexistent section"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    assert config.get('NonexistentSection', 'Key') is None
    assert config.get('NonexistentSection', 'Key', fallback='default') == 'default'

def test_config_getboolean_section_error(tmp_path):
    """Test error handling when getting boolean from nonexistent section"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    with pytest.raises(ConfigError, match="Section not found"):
        config.getboolean('NonexistentSection', 'Key')

def test_config_getint_section_error(tmp_path):
    """Test error handling when getting integer from nonexistent section"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    with pytest.raises(ConfigError, match="Section not found"):
        config.getint('NonexistentSection', 'Key')

def test_window_settings_save_error(tmp_path):
    """Test error handling when saving window settings fails"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    os.chmod(config_file, 0o444)  # Make file read-only
    
    with pytest.raises(ConfigError, match="Failed to set window settings"):
        config.window_settings = {'start_maximized': True}
    
    os.chmod(config_file, 0o666)  # Restore permissions

def test_about_settings_error_complete(tmp_path, mocker):
    """Test complete error handling in about settings"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock get method to raise an exception
    mocker.patch.object(config, 'get', side_effect=Exception("Mock error"))
    
    settings = config.about_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0  # Should return empty dict on error

def test_get_error_handling(tmp_path, mocker):
    """Test error handling in get method"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock configparser's get to raise an exception
    mocker.patch.object(config.config, 'get', side_effect=Exception("Mock error"))
    
    # Should return fallback value
    assert config.get('Section', 'Option', fallback='default') == 'default'

def test_getboolean_error_handling(tmp_path, mocker):
    """Test error handling in getboolean method"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock configparser's getboolean to raise an exception
    mocker.patch.object(config.config, 'getboolean', side_effect=Exception("Mock error"))
    
    with pytest.raises(ConfigError, match="Failed to get boolean value"):
        config.getboolean('Section', 'Option')

def test_getint_error_handling(tmp_path, mocker):
    """Test error handling in getint method"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Section]\nOption = Invalid\n")
    
    config = Config(str(config_file))
    
    with pytest.raises(ConfigError, match="Failed to get integer value"):
        config.getint('Section', 'Option')

def test_set_error_handling(tmp_path, mocker):
    """Test error handling in set method"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Section]\nOption = Value\n")
    
    config = Config(str(config_file))
    
    # Mock configparser's set to raise an error
    mocker.patch.object(config.config, 'set', side_effect=Exception("Mock error"))
    
    with pytest.raises(ConfigError, match="Failed to set configuration value"):
        config.set('Section', 'Option', 'NewValue')

def test_get_error_complete(tmp_path, mocker):
    """Test complete error handling in get method"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock configparser's get to raise an exception
    mocker.patch.object(config.config, 'get', side_effect=Exception("Mock error"))
    
    # Should return fallback value
    assert config.get('Section', 'Option', fallback='default') == 'default'

def test_modules_enabled_error_complete(tmp_path, mocker):
    """Test complete error handling in modules_enabled"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock getboolean to raise an error
    mocker.patch.object(config, 'getboolean', side_effect=Exception("Mock error"))
    
    # Should return empty dict on error
    modules = config.modules_enabled
    assert isinstance(modules, dict)
    assert len(modules) == 0

def test_window_settings_error_complete_2(tmp_path, mocker):
    """Test error handling in window_settings property"""
    config_file = tmp_path / "test_config.ini"
    config_file.touch()
    
    config = Config(str(config_file))
    
    # Mock get to raise an error
    mocker.patch.object(config, 'get', side_effect=Exception("Mock error"))
    
    # Should return default values
    settings = config.window_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0

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

def test_get_section_not_found(config_setup):
    """Test get when section is not found."""
    assert config_setup.get('NonexistentSection', 'option', fallback='default') == 'default'

def test_getboolean_section_not_found(config_setup):
    """Test getboolean when section is not found."""
    with pytest.raises(ConfigError, match="Section not found: NonexistentSection"):
        config_setup.getboolean('NonexistentSection', 'option')

def test_getboolean_option_not_found(config_setup):
    """Test getboolean when option is not found."""
    config_setup.config.add_section('TestSection')
    with pytest.raises(ConfigError, match="Option not found: option in section TestSection"):
        config_setup.getboolean('TestSection', 'option')

def test_getint_section_not_found(config_setup):
    """Test getint when section is not found."""
    with pytest.raises(ConfigError, match="Section not found: NonexistentSection"):
        config_setup.getint('NonexistentSection', 'option')

def test_getint_option_not_found(config_setup):
    """Test getint when option is not found."""
    config_setup.config.add_section('TestSection')
    with pytest.raises(ConfigError, match="Option not found: option in section TestSection"):
        config_setup.getint('TestSection', 'option')

def test_getint_invalid_value(config_setup):
    """Test getint with invalid integer value."""
    config_setup.config.add_section('TestSection')
    config_setup.config.set('TestSection', 'option', 'not_an_integer')
    with pytest.raises(ConfigError, match="Failed to get integer value:"):
        config_setup.getint('TestSection', 'option')

def test_set_section_not_found(config_setup):
    """Test set when section is not found."""
    with pytest.raises(ConfigError, match="Section not found: NonexistentSection"):
        config_setup.set('NonexistentSection', 'option', 'value')

def test_config_load_file_not_found():
    """Test loading nonexistent config file."""
    with pytest.raises(ConfigError, match="Configuration file not found: nonexistent.ini"):
        Config("nonexistent.ini")

def test_config_get_value(config_setup):
    """Test getting a config value."""
    config_setup.config.add_section('Test')
    config_setup.config.set('Test', 'option', 'value')
    assert config_setup.get('Test', 'option') == 'value'

def test_config_get_value_with_fallback(config_setup):
    """Test getting a config value with fallback."""
    assert config_setup.get('Test', 'option', fallback='default') == 'default'

def test_config_getboolean(config_setup):
    """Test getting a boolean config value."""
    config_setup.config.add_section('Test')
    config_setup.config.set('Test', 'option', 'true')
    assert config_setup.getboolean('Test', 'option') is True

def test_config_getint(config_setup):
    """Test getting an integer config value."""
    config_setup.config.add_section('Test')
    config_setup.config.set('Test', 'option', '42')
    assert config_setup.getint('Test', 'option') == 42

def test_config_set(config_setup):
    """Test setting a config value."""
    config_setup.config.add_section('Test')
    config_setup.set('Test', 'option', 'value')
    assert config_setup.get('Test', 'option') == 'value'

def test_app_info(empty_config):
    """Test getting application information."""
    empty_config.config.add_section('Application')
    empty_config.config.set('Application', 'Name', 'Test App')
    empty_config.config.set('Application', 'Version', '1.0.0')
    empty_config.config.set('Application', 'Debug', 'true')
    
    info = empty_config.app_info
    assert isinstance(info, dict)
    assert info['name'] == 'Test App'
    assert info['version'] == '1.0.0'
    assert info['debug'] is True

def test_app_info_error_complete(empty_config, mocker):
    """Test complete error handling in app_info."""
    mocker.patch.object(empty_config, 'get', side_effect=Exception("Mock error"))
    mocker.patch.object(empty_config, 'getboolean', side_effect=Exception("Mock error"))
    
    info = empty_config.app_info
    assert isinstance(info, dict)
    assert len(info) == 0

def test_application_settings(empty_config):
    """Test getting application settings."""
    empty_config.config.add_section('Application')
    empty_config.config.set('Application', 'name', 'Test App')
    empty_config.config.set('Application', 'debug', 'True')
    
    settings = empty_config.application_settings
    assert isinstance(settings, dict)
    assert settings['name'] == 'Test App'
    assert settings['debug'] == 'True'

def test_application_settings_error_complete(empty_config, mocker):
    """Test complete error handling in application_settings."""
    mocker.patch.object(empty_config, 'get', side_effect=Exception("Mock error"))
    
    settings = empty_config.application_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0

def test_window_settings(empty_config):
    """Test getting and setting window settings."""
    empty_config.config.add_section('Window')
    empty_config.config.set('Window', 'start_maximized', 'true')
    empty_config.config.set('Window', 'screen_width', '800')
    empty_config.config.set('Window', 'screen_height', '600')
    empty_config.config.set('Window', 'theme', 'dark')
    
    settings = empty_config.window_settings
    assert isinstance(settings, dict)
    assert settings['start_maximized'] is True
    assert settings['screen_width'] == 800
    assert settings['screen_height'] == 600
    assert settings['theme'] == 'dark'

def test_window_settings_error_complete(empty_config, mocker):
    """Test complete error handling in window_settings."""
    mocker.patch.object(empty_config, 'getboolean', side_effect=Exception("Mock error"))
    mocker.patch.object(empty_config, 'getint', side_effect=Exception("Mock error"))
    mocker.patch.object(empty_config, 'get', side_effect=Exception("Mock error"))
    
    settings = empty_config.window_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0

def test_window_settings_save_error_complete(empty_config, mocker):
    """Test complete error handling in window_settings setter."""
    mocker.patch.object(empty_config, 'save_config', side_effect=ConfigError("Mock error"))
    
    with pytest.raises(ConfigError, match="Failed to set window settings"):
        empty_config.window_settings = {'start_maximized': True}

def test_about_settings(empty_config):
    """Test getting about settings."""
    empty_config.config.add_section('About')
    empty_config.config.set('About', 'Author', 'Test Author')
    empty_config.config.set('About', 'Description', 'Test Description')
    
    settings = empty_config.about_settings
    assert isinstance(settings, dict)
    assert settings['author'] == 'Test Author'
    assert settings['description'] == 'Test Description'

def test_about_settings_error_complete(empty_config, mocker):
    """Test complete error handling in about_settings."""
    mocker.patch.object(empty_config, 'get', side_effect=Exception("Mock error"))
    
    settings = empty_config.about_settings
    assert isinstance(settings, dict)
    assert len(settings) == 0

def test_modules_enabled(empty_config):
    """Test getting enabled modules."""
    empty_config.config.add_section('Modules')
    empty_config.config.set('Modules', 'logging', 'true')
    empty_config.config.set('Modules', 'database', 'false')
    empty_config.config.set('Modules', 'menu', 'true')
    empty_config.config.set('Modules', 'toolbar', 'false')
    empty_config.config.set('Modules', 'status_bar', 'true')
    
    modules = empty_config.modules_enabled
    assert isinstance(modules, dict)
    assert modules['logging'] is True
    assert modules['database'] is False
    assert modules['menu'] is True
    assert modules['toolbar'] is False
    assert modules['status_bar'] is True

def test_modules_enabled_error_complete(empty_config, mocker):
    """Test complete error handling in modules_enabled."""
    mocker.patch.object(empty_config, 'getboolean', side_effect=Exception("Mock error"))
    
    modules = empty_config.modules_enabled
    assert isinstance(modules, dict)
    assert len(modules) == 0
