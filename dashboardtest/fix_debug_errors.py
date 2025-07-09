#!/usr/bin/env python3
"""
Script to fix all debugger.log_callback_error calls in callbacks.py
Changes error_msg to e to pass the exception object instead of string
"""

import re

def fix_debug_errors():
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    # Read the file
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find debugger.log_callback_error calls with error_msg
    pattern = r"debugger\.log_callback_error\(([^,]+),\s*error_msg\)"
    
    # Replace with e instead of error_msg
    replacement = r"debugger.log_callback_error(\1, e)"
    
    # Count matches before replacement
    matches = re.findall(pattern, content)
    print(f"Found {len(matches)} debugger.log_callback_error calls to fix")
    
    # Perform replacement
    fixed_content = re.sub(pattern, replacement, content)
    
    # Write back to file
    with open(callbacks_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed {len(matches)} debugger.log_callback_error calls")
    print("Replacement complete!")

if __name__ == "__main__":
    fix_debug_errors()
