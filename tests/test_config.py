"""
Test configuration and utilities
"""
import os
import shutil
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def temp_dir():
    """Create a temporary directory and clean it up when done"""
    temp_path = Path('temp_test_dir')
    temp_path.mkdir(exist_ok=True)
    original_cwd = os.getcwd()
    os.chdir(temp_path)
    try:
        yield temp_path
    finally:
        os.chdir(original_cwd)
        if temp_path.exists():
            shutil.rmtree(temp_path)

def create_test_config():
    """Create a test configuration object"""
    from config.app_config import Config
    
    # Create a test config file
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'test_config.ini'
    with open(config_file, 'w') as f:
        f.write('''[APP]
start_maximized = True
screen_width = 1024
screen_height = 768
theme = light
''')
    
    return Config(str(config_file))
