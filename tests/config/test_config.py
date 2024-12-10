"""
Unit tests for the configuration module.
"""

from modules.config import Config


def test_about_info(tmp_path):
    """Test getting about information."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Set some about info
    config.set('About', 'author', 'Test Author')
    config.set('About', 'version', '1.0.0')

    # Get about info
    about = config.about_info
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
    app = {
        'name': config.get('Application', 'name'),
        'version': config.get('Application', 'version')
    }
    assert app['name'] == 'Test App'
    assert app['version'] == '1.0.0'


def test_window_settings(tmp_path):
    """Test getting and setting window settings."""
    config_file = tmp_path / "test_config.ini"
    config = Config(str(config_file))

    # Test setting window settings
    settings = {'screen_width': '1280', 'screen_height': '720'}
    config.set_window_settings(settings)

    # Test getting window settings
    loaded = config.get_window_settings()
    assert loaded['screen_width'] == '1280'
    assert loaded['screen_height'] == '720'
