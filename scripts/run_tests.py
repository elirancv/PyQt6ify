#!/usr/bin/env python3
"""
Test runner script for PyQt6ify Pro
"""
import subprocess
import sys

def run_tests():
    """Run all tests with coverage report"""
    print("Running PyQt6ify Pro Tests...\n")

    # Run pytest with coverage
    result = subprocess.run([
        "pytest",
        "-v",
        "--cov=modules",
        "--cov-report=term-missing",
        "tests/"
    ])

    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
