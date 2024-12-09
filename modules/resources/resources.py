"""
Resource management implementation for PyQt6ify Pro.
"""

import os
from pathlib import Path
from loguru import logger

class ResourceError(Exception):
    """Exception raised for resource-related errors."""
    pass

def get_resource_path(resource_name):
    """
    Get the absolute path to a resource.
    
    Args:
        resource_name (str): Name of the resource (e.g. 'icons/app_icon.png')
        
    Returns:
        str: Absolute path to the resource
        
    Raises:
        ResourceError: If resource_name is invalid or resource doesn't exist
    """
    if not resource_name:
        raise ResourceError("Resource name cannot be empty or None")
        
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        resource_path = os.path.join(base_dir, 'resources', resource_name)
        
        if not os.path.exists(resource_path):
            raise ResourceError(f"Resource not found: {resource_name}")
            
        return resource_path
    except Exception as e:
        raise ResourceError(f"Error accessing resource: {str(e)}")

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
