#!/usr/bin/env python3
"""
Script to find duplicate function definitions in callbacks.py
"""

import re

def find_duplicate_functions():
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    # Read the file
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all function definitions
    functions = {}
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def '):
            # Extract function name
            match = re.match(r'\s*def\s+(\w+)\s*\(', line)
            if match:
                func_name = match.group(1)
                line_num = i + 1
                
                if func_name in functions:
                    print(f"DUPLICATE: {func_name}")
                    print(f"  First definition at line {functions[func_name]}")
                    print(f"  Second definition at line {line_num}")
                    print(f"  Line content: {line.strip()}")
                    print()
                else:
                    functions[func_name] = line_num
    
    # Check for specific functions from the error report
    error_functions = [
        'sidebar_amount_50_callback',
        'sidebar_amount_100_callback', 
        'sidebar_amount_1000_callback',
        'sidebar_amount_250_callback',
        'sidebar_amount_500_callback',
        'sidebar_amount_max_callback'
    ]
    
    print("Looking for error-reported functions:")
    for func in error_functions:
        if func in functions:
            print(f"Found {func} at line {functions[func]}")
        else:
            print(f"NOT FOUND: {func}")

if __name__ == "__main__":
    find_duplicate_functions()
