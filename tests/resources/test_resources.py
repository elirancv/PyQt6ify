"""
Test resources module functionality.
"""

import os
import pytest
from modules.resources.resources import get_resource_path, ResourceError

def test_get_resource_path():
    """Test getting path to existing resource"""
    # Test with a known resource
    path = get_resource_path('icons/app.png')
    assert os.path.exists(path)
    assert path.endswith('icons/app.png')

def test_get_resource_path_nonexistent():
    """Test getting path to non-existent resource"""
    with pytest.raises(ResourceError):
        get_resource_path('nonexistent/file.txt')

def test_get_resource_path_empty():
    """Test getting path with empty resource name"""
    with pytest.raises(ResourceError):
        get_resource_path('')

def test_get_resource_path_none():
    """Test getting path with None resource name"""
    with pytest.raises(ResourceError):
        get_resource_path(None)

def test_get_resource_path_directory():
    """Test getting path to resource directory"""
    path = get_resource_path('icons')
    assert os.path.isdir(path)
    assert os.path.exists(path)
