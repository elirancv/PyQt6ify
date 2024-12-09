"""
Module loader for PyQt6ify Pro.
"""

import os
import importlib.util
import sys
from loguru import logger

class ModuleLoader:
    """Module loader class for PyQt6ify Pro."""
    
    def __init__(self, base_path):
        """Initialize the module loader."""
        self.base_path = base_path
        self.loaded_modules = {}
        
    def _is_module_file(self, file_path):
        """Check if a file is a valid Python module file."""
        return (
            file_path.endswith('.py') and 
            not os.path.basename(file_path).startswith('__') and
            os.path.isfile(file_path)
        )
        
    def _get_module_name(self, file_path):
        """Get the module name from a file path."""
        rel_path = os.path.relpath(file_path, self.base_path)
        module_path = os.path.splitext(rel_path)[0]
        # Convert path separators to dots and ensure proper module path
        return module_path.replace(os.sep, '.')

    def load_module(self, file_path):
        """
        Load a Python module from a file path.
        
        Args:
            file_path (str): Path to the module file
            
        Returns:
            module: The loaded module or None if loading fails
        """
        try:
            module_name = self._get_module_name(file_path)
            
            # Skip if module is already loaded
            if module_name in sys.modules:
                return sys.modules[module_name]
            
            # Skip if module is in loaded_modules
            if module_name in self.loaded_modules:
                return self.loaded_modules[module_name]
            
            logger.debug(f"Loading module: {module_name} from {file_path}")
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                logger.error(f"Failed to create module spec for: {file_path}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            logger.info(f"Successfully loaded module: {module_name}")
            return module
            
        except Exception as e:
            logger.error(f"Error loading module {file_path}: {str(e)}")
            return None
            
    def load_all_modules(self, directory):
        """
        Load all Python modules from a directory and its subdirectories.
        
        Args:
            directory (str): Directory to search for modules
            
        Returns:
            dict: Dictionary of loaded modules
        """
        try:
            # Find all Python files in the directory
            module_files = []
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self._is_module_file(file_path):
                        module_files.append(file_path)
            
            logger.debug(f"Found modules: {module_files}")
            
            # Load each module
            for file_path in module_files:
                module = self.load_module(file_path)
                if module is not None:
                    module_name = self._get_module_name(file_path)
                    self.loaded_modules[module_name] = module
            
            return self.loaded_modules
            
        except Exception as e:
            logger.error(f"Error loading modules from directory {directory}: {str(e)}")
            return {}
