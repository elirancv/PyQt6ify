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

def test_config_set_invalid_section():
    """Test setting value in invalid section"""
    config = Config()
    with pytest.raises(ConfigError):
        config.set('InvalidSection', 'Key', 'Value')

def test_config_boolean_values():
    """Test getting boolean values"""
    config = Config()
    assert config.getboolean('Application', 'Debug') is True
    config.set('Application', 'Debug', 'False')
    assert config.getboolean('Application', 'Debug') is False

def test_config_int_values():
    """Test getting integer values"""
    config = Config()
    assert config.getint('Window', 'screen_width') == 1024
    config.set('Window', 'screen_width', '800')
    assert config.getint('Window', 'screen_width') == 800

def test_config_invalid_bool():
    """Test getting invalid boolean value"""
    config = Config()
    config.set('Application', 'Debug', 'NotABool')
    with pytest.raises(ConfigError):
        config.getboolean('Application', 'Debug')

def test_config_invalid_int():
    """Test getting invalid integer value"""
    config = Config()
    config.set('Window', 'screen_width', 'NotANumber')
    with pytest.raises(ConfigError):
        config.getint('Window', 'screen_width')

def test_modules_enabled(tmp_path):
    """Test getting enabled modules configuration"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Modules]\nlogging = True\ndatabase = False\nmenu = True\ntoolbar = True\nstatus_bar = True\n")
    
    config = Config(str(config_file))
    modules = config.modules_enabled
    assert modules['logging'] is True
    assert modules['database'] is False
    assert modules['menu'] is True
    assert modules['toolbar'] is True
    assert modules['status_bar'] is True

def test_about_info(tmp_path):
    """Test getting about dialog information"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nVersion = 1.0.0\n")
        f.write("[About]\nAuthor = Test Author\nDescription = Test Description\n")
        f.write("Website = https://test.com\nIcon = test.png\n")
    
    config = Config(str(config_file))
    about = config.about_info
    assert about['name'] == 'Test App'
    assert about['version'] == '1.0.0'
    assert about['author'] == 'Test Author'
    assert about['description'] == 'Test Description'
    assert about['website'] == 'https://test.com'
    assert about['icon'] == 'test.png'

def test_app_info(tmp_path):
    """Test getting application information"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nVersion = 1.0.0\nDebug = True\n")
    
    config = Config(str(config_file))
    app = config.app_info
    assert app['name'] == 'Test App'
    assert app['version'] == '1.0.0'
    assert app['debug'] is True

def test_app_info_error(tmp_path):
    """Test error handling in app_info"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nDebug = Invalid\n")  # Invalid boolean value
    
    config = Config(str(config_file))
    app = config.app_info
    # Should return empty dict when there's an error
    assert app == {}

def test_application_settings(tmp_path):
    """Test getting application settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\nVersion = 1.0.0\nDebug = True\n")
    
    config = Config(str(config_file))
    settings = config.application_settings
    assert settings['Name'] == 'Test App'
    assert settings['Version'] == '1.0.0'
    assert settings['Debug'] == 'True'

def test_window_settings(tmp_path):
    """Test getting and setting window settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nstart_maximized = True\nscreen_width = 1024\n")
        f.write("screen_height = 768\ntheme = dark\n")
    
    config = Config(str(config_file))
    settings = config.window_settings
    assert settings['start_maximized'] is True
    assert settings['screen_width'] == 1024
    assert settings['screen_height'] == 768
    assert settings['theme'] == 'dark'

    # Test setting window settings
    new_settings = {
        'start_maximized': False,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'light'
    }
    config.window_settings = new_settings
    
    # Verify settings were saved
    config2 = Config(str(config_file))
    settings = config2.window_settings
    assert settings['start_maximized'] is False
    assert settings['screen_width'] == 800
    assert settings['screen_height'] == 600
    assert settings['theme'] == 'light'

def test_window_settings_error(tmp_path):
    """Test error handling in window settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nscreen_width = Invalid\n")  # Invalid integer value
    
    config = Config(str(config_file))
    settings = config.window_settings
    # Should return empty dict when there's an error
    assert settings == {}

def test_window_settings_section_error(tmp_path):
    """Test error handling in window settings when section is missing"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")  # Missing Window section
    
    config = Config(str(config_file))
    settings = config.window_settings
    # Should use default values when section is missing
    assert settings['start_maximized'] is True  # getboolean converts 'True' to True
    assert settings['screen_width'] == 1024  # getint converts '1024' to 1024
    assert settings['screen_height'] == 768  # getint converts '768' to 768
    assert settings['theme'] == 'light'  # theme stays as string

def test_window_settings_setter_section_error(tmp_path):
    """Test error handling in window settings setter when section is missing"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")  # Missing Window section
    
    config = Config(str(config_file))
    settings = {
        'start_maximized': True,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'dark'
    }
    # Should create Window section and save settings
    config.window_settings = settings
    
    # Verify settings were saved
    config2 = Config(str(config_file))
    saved_settings = config2.window_settings
    assert saved_settings['start_maximized'] is True
    assert saved_settings['screen_width'] == 800
    assert saved_settings['screen_height'] == 600
    assert saved_settings['theme'] == 'dark'

def test_about_settings(tmp_path):
    """Test getting about settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\nDescription = Test Description\n")
        f.write("Website = https://test.com\nIcon = test.png\n")
    
    config = Config(str(config_file))
    settings = config.about_settings
    assert settings['author'] == 'Test Author'
    assert settings['description'] == 'Test Description'
    assert settings['website'] == 'https://test.com'
    assert settings['icon'] == 'test.png'

def test_about_settings_error(tmp_path):
    """Test error handling in about settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nInvalid = Value\n")  # Missing required fields
    
    config = Config(str(config_file))
    settings = config.about_settings
    # Should use default values for missing fields
    assert settings == {
        'author': config.default_config['About']['Author'],
        'description': config.default_config['About']['Description'],
        'website': config.default_config['About']['Website'],
        'icon': config.default_config['About']['Icon']
    }

def test_modules_enabled_error(tmp_path):
    """Test error handling in modules_enabled"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Modules]\nlogging = Invalid\n")  # Invalid boolean value
    
    config = Config(str(config_file))
    modules = config.modules_enabled
    # Should return default values when there's an error
    assert modules == config.default_config['Modules']

def test_about_info_error(tmp_path):
    """Test error handling in about_info"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\n")  # Missing required sections
    
    config = Config(str(config_file))
    about = config.about_info
    # Should use fallback values for missing fields
    assert about['author'] == 'Test Author'
    assert about['description'] == config.default_config['About']['Description']
    assert about['website'] == config.default_config['About']['Website']
    assert about['icon'] == config.default_config['About']['Icon']

def test_window_settings_setter_error(tmp_path):
    """Test error handling in window settings setter"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nstart_maximized = True\n")
        
    config = Config(str(config_file))
    
    # Setting invalid settings (missing required keys)
    invalid_settings = {'invalid_key': 'value'}
    config.window_settings = invalid_settings
    
    # Verify settings were not saved
    config2 = Config(str(config_file))
    settings = config2.window_settings
    assert settings != invalid_settings

def test_save_config_error(tmp_path):
    """Test error when saving config file"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    os.chmod(config_file, 0o444)  # Read-only
    
    config = Config(str(config_file))
    config.set('Application', 'Name', 'New App')
    with pytest.raises(ConfigError):
        config.save_config()
    
    # Reset file permissions
    os.chmod(config_file, 0o666)

def test_config_not_found_error():
    """Test error when config file not found"""
    with pytest.raises(ConfigError):
        Config("nonexistent.ini")

def test_config_load_error(tmp_path):
    """Test error handling when loading config file fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Invalid Config File")  # Invalid config file format
    
    with pytest.raises(ConfigError):
        Config(str(config_file))

def test_config_save_permission_error(tmp_path):
    """Test error handling when saving config file fails due to permissions"""
    config_file = tmp_path / "test_config.ini"
    os.makedirs(tmp_path, exist_ok=True)
    
    # Create a read-only config file
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    os.chmod(config_file, 0o444)  # Read-only
    
    config = Config(str(config_file))
    config.set('Application', 'Name', 'New App')
    
    # Try to save config
    with pytest.raises(ConfigError):
        config.save_config()
    
    # Reset file permissions
    os.chmod(config_file, 0o666)

def test_config_set_error(tmp_path):
    """Test error handling when setting config value fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    
    config = Config(str(config_file))
    with pytest.raises(ConfigError):
        config.set('NonExistentSection', 'Name', 'New App')

def test_config_get_error(tmp_path):
    """Test error handling when getting config value fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    
    config = Config(str(config_file))
    # get method now returns fallback instead of raising error
    assert config.get('NonExistentSection', 'Name') is None
    assert config.get('NonExistentSection', 'Name', fallback='default') == 'default'

def test_config_get_bool_error(tmp_path):
    """Test error handling when getting boolean value fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    
    config = Config(str(config_file))
    with pytest.raises(ConfigError):
        config.getboolean('NonExistentSection', 'Name')

def test_config_get_int_error(tmp_path):
    """Test error handling when getting integer value fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    
    config = Config(str(config_file))
    with pytest.raises(ConfigError):
        config.getint('NonExistentSection', 'Name')

def test_window_settings_setter_invalid_settings(tmp_path):
    """Test error handling when setting invalid window settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nstart_maximized = True\n")
    
    config = Config(str(config_file))
    settings = {
        'invalid_key': 'value'  # Invalid key
    }
    
    # Should silently ignore invalid settings
    config.window_settings = settings
    
    # Verify original settings were not changed
    config2 = Config(str(config_file))
    assert config2.window_settings['start_maximized'] is True

def test_about_settings_missing_section(tmp_path):
    """Test getting about settings when section is missing"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")  # Missing About section
    
    config = Config(str(config_file))
    settings = config.about_settings
    # Should use default values when section is missing
    assert settings == {
        'author': config.default_config['About']['Author'],
        'description': config.default_config['About']['Description'],
        'website': config.default_config['About']['Website'],
        'icon': config.default_config['About']['Icon']
    }

def test_get_fallback_error(tmp_path):
    """Test error handling when getting value with fallback"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Application]\nName = Test App\n")
    
    config = Config(str(config_file))
    # get method now returns fallback instead of raising error
    assert config.get('NonExistentSection', 'Name') is None
    assert config.get('NonExistentSection', 'Name', fallback='default') == 'default'

def test_window_settings_setter_error(tmp_path):
    """Test error handling when setting window settings fails"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[Window]\nstart_maximized = True\n")
    os.chmod(config_file, 0o444)  # Read-only
    
    config = Config(str(config_file))
    settings = {
        'start_maximized': False,
        'screen_width': 800,
        'screen_height': 600,
        'theme': 'dark'
    }
    
    # Should handle error when saving settings
    config.window_settings = settings
    
    # Reset file permissions
    os.chmod(config_file, 0o666)

def test_about_settings_error_handling(tmp_path):
    """Test error handling in about settings"""
    config_file = tmp_path / "test_config.ini"
    with open(config_file, 'w') as f:
        f.write("[About]\nAuthor = Test Author\n")  # Missing other fields
    
    config = Config(str(config_file))
    settings = config.about_settings
    # Should use default values for missing fields
    assert settings['author'] == 'Test Author'  # Use value from file
    assert settings['description'] == config.default_config['About']['Description']  # Use default
    assert settings['website'] == config.default_config['About']['Website']  # Use default
    assert settings['icon'] == config.default_config['About']['Icon']  # Use default
