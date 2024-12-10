"""Script to remove trailing whitespace from Python files."""
import os
import sys

def remove_trailing_whitespace(file_path):
    """Remove trailing whitespace from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8', newline='\n') as file:
        for line in lines:
            file.write(line.rstrip() + '\n')

def process_directory(directory):
    """Process all Python files in a directory recursively."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                remove_trailing_whitespace(file_path)

if __name__ == '__main__':
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Process modules and tests directories
    modules_dir = os.path.join(project_root, 'modules')
    tests_dir = os.path.join(project_root, 'tests')

    print("Removing trailing whitespace from Python files...")
    process_directory(modules_dir)
    process_directory(tests_dir)
    print("Done!")
