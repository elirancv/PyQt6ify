"""
Resource management implementation for PyQt6ify Pro.
"""

import os
from pathlib import Path
from typing import Optional
from loguru import logger

class ResourceError(Exception):
    """Exception raised for resource-related errors."""

def get_resource_path(resource_name: str) -> str:
    """
    Get the absolute path to a resource file.

    Args:
        resource_name (str): Name of the resource file

    Returns:
        str: Absolute path to the resource file
    """
    try:
        # Get the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct path to resource
        resource_path = os.path.join(script_dir, 'resources', resource_name)

        # Check if resource exists
        if not os.path.exists(resource_path):
            raise ResourceError(f'Resource not found: {resource_name}')

        return resource_path
    except Exception as e:
        raise ResourceError(f'Error accessing resource: {str(e)}') from e

def create_resources(base_dir: str) -> Optional[str]:
    """
    Create necessary resource directories.

    Args:
        base_dir (str): Base directory path

    Returns:
        Optional[str]: Path to resources directory if created successfully
    """
    try:
        resources_dir = os.path.join(base_dir, 'resources')
        icons_dir = os.path.join(resources_dir, 'icons')
        themes_dir = os.path.join(resources_dir, 'themes')
        logs_dir = os.path.join(base_dir, 'logs')
        config_dir = os.path.join(base_dir, 'config')
        database_dir = os.path.join(base_dir, 'database')

        # Create directories if they don't exist
        os.makedirs(resources_dir, exist_ok=True)
        os.makedirs(icons_dir, exist_ok=True)
        os.makedirs(themes_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(database_dir, exist_ok=True)

        # Create .gitkeep files to ensure empty directories are tracked
        for path in [resources_dir, icons_dir, themes_dir, logs_dir, config_dir, database_dir]:
            gitkeep_file = os.path.join(path, '.gitkeep')
            if not os.path.exists(gitkeep_file):
                Path(gitkeep_file).touch()

        return resources_dir
    except OSError as e:
        logger.error(f"Error creating resources: {str(e)}")
        raise ResourceError(f"Failed to create resource directories: {str(e)}") from e
