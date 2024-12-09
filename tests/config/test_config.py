"""
Test configuration module functionality.
"""

import os
import pytest
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

def test_application_settings(tmp_path):
    """Test getting application settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nDebug = True\n")
    
    config = Config(str(config_file))
    settings = config.application_settings
    assert settings['name'] == 'Test App'
    assert settings['debug'] == 'True'  # Debug is stored as string

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
    config_file.touch()  # Create empty file
    
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
    config_file.touch()  # Create empty file
    
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
