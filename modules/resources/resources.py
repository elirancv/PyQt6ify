"""
Resource management implementation for PyQt6ify Pro.
"""

import os
from pathlib import Path
from loguru import logger

def create_resources():
    """Create necessary resource directories and files."""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Create resource directories
        paths = [
            os.path.join(base_dir, 'resources'),
            os.path.join(base_dir, 'resources', 'icons'),
            os.path.join(base_dir, 'logs'),
            os.path.join(base_dir, 'config'),
            os.path.join(base_dir, 'database')
        ]
        
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info(f"Created directory: {path}")
                
        # Create .gitkeep files to ensure empty directories are tracked
        for path in paths:
            gitkeep_file = os.path.join(path, '.gitkeep')
            if not os.path.exists(gitkeep_file):
                Path(gitkeep_file).touch()
                
    except Exception as e:
        logger.error(f"Error creating resources: {str(e)}")
        raise
