"""
Test runner for PyQt6ify Pro
"""
import os
import sys
import pytest
import shutil
from pathlib import Path

def main():
    """Run the test suite"""
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    # Clean up previous test artifacts
    cleanup_dirs = ['logs', 'database', 'temp', 'htmlcov', '.pytest_cache', '.coverage']
    for dir_name in cleanup_dirs:
        path = project_root / dir_name
        if path.is_file():
            path.unlink(missing_ok=True)
        elif path.is_dir():
            shutil.rmtree(path, ignore_errors=True)

    # Create necessary directories
    for dir_name in ['logs', 'database', 'temp']:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)

    # Configure test arguments
    pytest_args = [
        'tests',                    # test directory
        '-v',                       # verbose output
        '--tb=short',              # shorter traceback format
        '--cov=modules',           # measure coverage for modules
        '--cov-branch',            # measure branch coverage
        '--cov-report=term-missing:skip-covered',  # show missing lines in terminal
        '--cov-report=html',       # generate HTML coverage report
        '--cov-config=.coveragerc',  # coverage configuration
        '--no-cov-on-fail',        # don't report coverage if tests fail
    ]

    # Run the tests
    exit_code = pytest.main(pytest_args)

    # Clean up temporary files but keep coverage report
    temp_dir = project_root / 'temp'
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)

    return exit_code

if __name__ == '__main__':
    sys.exit(main())
