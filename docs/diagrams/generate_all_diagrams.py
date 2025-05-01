#!/usr/bin/env python
"""
Main script to generate all diagrams for the Quiz application documentation.

This script runs all the diagram generation scripts to create a complete
set of diagrams for the project documentation.
"""

import os
import subprocess
import sys

def run_script(script_name):
    """Run a Python script and print its output."""
    print(f"\n{'='*80}")
    print(f"Running {script_name}...")
    print(f"{'='*80}")
    
    # Get the absolute path to the script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    try:
        # Run the script and capture its output
        result = subprocess.run([sys.executable, script_path], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True,
                               check=True)
        
        # Print the output
        print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stderr)
        return False

def main():
    """Run all diagram generation scripts."""
    # Create the output directory if it doesn't exist
    os.makedirs('docs/diagrams/output', exist_ok=True)
    
    # List of scripts to run
    scripts = [
        'dfd_diagrams.py',
        'use_case_diagram.py',
        'sequence_diagram.py',
        'component_diagram.py',
        'project_planning.py'
    ]
    
    # Run each script
    success_count = 0
    failed_scripts = []
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            failed_scripts.append(script)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"Diagram Generation Summary")
    print(f"{'='*80}")
    print(f"Total scripts: {len(scripts)}")
    print(f"Successfully completed: {success_count}")
    
    if failed_scripts:
        print(f"Failed scripts: {len(failed_scripts)}")
        for script in failed_scripts:
            print(f"  - {script}")
    else:
        print("All scripts completed successfully!")
        
    print(f"\nDiagrams have been generated in: docs/diagrams/output/")

if __name__ == "__main__":
    main() 