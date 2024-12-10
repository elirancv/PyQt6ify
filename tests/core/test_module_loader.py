"""Test module for module loader."""
import os
import sys
from unittest.mock import patch, MagicMock
import pytest
from modules.core.module_loader import ModuleLoader

@pytest.fixture
def module_loader():
    """Create a ModuleLoader instance for testing."""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return ModuleLoader(base_path)

def test_is_module_file(module_loader, tmp_path):
    """Test _is_module_file method."""
    # Create test files
    valid_module = tmp_path / "test_module.py"
    init_file = tmp_path / "__init__.py"
    non_python = tmp_path / "test.txt"

    valid_module.write_text("")
    init_file.write_text("")
    non_python.write_text("")

    # Test valid module file
    assert module_loader._is_module_file(str(valid_module)) is True

    # Test __init__.py file
    assert module_loader._is_module_file(str(init_file)) is False

    # Test non-Python file
    assert module_loader._is_module_file(str(non_python)) is False

def test_get_module_name(module_loader, tmp_path):
    """Test _get_module_name method."""
    # Create a mock module path
    module_path = os.path.join(module_loader.base_path, "modules", "test", "test_module.py")

    # Test module name generation
    expected_name = "modules.test.test_module"
    assert module_loader._get_module_name(module_path) == expected_name

@patch('importlib.util.spec_from_file_location')
@patch('importlib.util.module_from_spec')
def test_load_module_success(mock_module_from_spec, mock_spec_from_file_location, module_loader):
    """Test successful module loading."""
    # Setup mocks
    mock_spec = MagicMock()
    mock_module = MagicMock()

    mock_spec_from_file_location.return_value = mock_spec
    mock_module_from_spec.return_value = mock_module

    # Test loading a module
    test_path = os.path.join(module_loader.base_path, "modules", "test", "test_module.py")
    module_loader.load_module(test_path)

    # Verify the module was loaded correctly
    assert "modules.test.test_module" in sys.modules
    mock_spec.loader.exec_module.assert_called_once_with(mock_module)

@patch('importlib.util.spec_from_file_location')
def test_load_module_failure(mock_spec_from_file_location, module_loader):
    """Test module loading failure."""
    # Setup mock to return None (simulating failure)
    mock_spec_from_file_location.return_value = None

    # Test loading a non-existent module
    test_path = os.path.join(module_loader.base_path, "modules", "test", "non_existent.py")
    module_loader.load_module(test_path)

    # Verify the module was not loaded
    assert "modules.test.non_existent" not in sys.modules

def test_load_all_modules(module_loader, tmp_path):
    """Test loading all modules from a directory."""
    # Create test directory structure
    test_dir = tmp_path / "modules"
    test_dir.mkdir()

    # Create some test modules
    (test_dir / "test_module1.py").write_text("")
    (test_dir / "test_module2.py").write_text("")
    (test_dir / "__init__.py").write_text("")

    # Patch os.path.relpath to handle different drive letters in Windows
    with patch('os.path.relpath') as mock_relpath:
        mock_relpath.side_effect = lambda p, s: os.path.basename(p).replace('.py', '')
        with patch.object(module_loader, 'load_module') as mock_load_module:
            mock_module = MagicMock()
            mock_load_module.return_value = mock_module

            # Test loading all modules
            module_loader.load_all_modules(str(test_dir))

            # Verify correct number of modules were attempted to load
            assert mock_load_module.call_count == 2  # Should try to load two modules

            # Verify the modules were stored
            assert len(module_loader.loaded_modules) == 2

def test_skip_already_loaded_module(module_loader):
    """Test that already loaded modules are skipped."""
    # Create a mock module
    mock_module = MagicMock()
    module_name = "test_module"
    test_path = os.path.join(module_loader.base_path, "modules", "test", "test_module.py")

    # Add module to loaded_modules
    module_loader.loaded_modules[module_name] = mock_module

    # Patch _get_module_name to return our test module name
    with patch.object(module_loader, '_get_module_name', return_value=module_name):
        # Try to load the module again
        module_loader.load_module(test_path)

        # Test with sys.modules
        sys.modules[module_name] = mock_module
        module_loader.load_module(test_path)
