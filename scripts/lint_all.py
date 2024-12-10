#!/usr/bin/env python3
"""
Simple script to run pylint on modules and tests directories.
"""

import subprocess
import sys
from typing import List, Tuple

def run_pylint(directory: str) -> Tuple[float, str]:
    """Run pylint on a directory and return the score and output."""
    try:
        result = subprocess.run(
            ['pylint', directory],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Extract score from output
        score = 0.0
        for line in result.stdout.split('\n'):
            if 'rated at' in line:
                try:
                    score = float(line.split('rated at')[1].split('/')[0].strip())
                except (IndexError, ValueError):
                    pass
        
        return score, result.stdout
    except subprocess.CalledProcessError as e:
        return 0.0, str(e)

def main():
    """Main function."""
    directories = ['modules', 'tests']
    total_score = 0.0
    count = 0
    
    print("Running pylint...")
    print("=" * 80)
    
    for directory in directories:
        print(f"\nChecking {directory}...")
        print("-" * 80)
        
        score, output = run_pylint(directory)
        print(output)
        
        if score > 0:
            total_score += score
            count += 1
    
    if count > 0:
        average_score = total_score / count
        print("\nOverall Results:")
        print("=" * 80)
        print(f"Average score: {average_score:.2f}/10")
    else:
        print("\nNo directories were successfully linted")

if __name__ == '__main__':
    main()
