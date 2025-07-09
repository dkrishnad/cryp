#!/usr/bin/env python3
"""
Fix syntax errors in callbacks.py - specifically trailing commas before allow_duplicate=True
"""

import re

def fix_callback_syntax():
    file_path = r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find problematic trailing commas before allow_duplicate=True
    # This matches: ],\n,\n    allow_duplicate=True
    pattern = r'(\]\s*\n),\s*\n(\s*allow_duplicate=True)'
    replacement = r'\1\n\2'
    
    # Fix the pattern
    fixed_content = re.sub(pattern, replacement, content)
    
    # Also fix pattern: [State(...)]\n,\n    allow_duplicate=True
    pattern2 = r'(\[State\([^]]+\]\s*\n),\s*\n(\s*allow_duplicate=True)'
    fixed_content = re.sub(pattern2, replacement, fixed_content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed callback syntax errors in callbacks.py")
    print("Removed trailing commas before allow_duplicate=True")

if __name__ == "__main__":
    fix_callback_syntax()
