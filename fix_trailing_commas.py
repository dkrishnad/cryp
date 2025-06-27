#!/usr/bin/env python3
"""
Fix trailing comma syntax errors in callbacks.py
"""
import re

def fix_trailing_commas():
    callbacks_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py"
    
    with open(callbacks_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the problematic syntax: "]" + newline + "," + newline + "allow_duplicate=True)"
    pattern = r'(\])\s*\n\s*,\s*\n\s*(allow_duplicate=True\))'
    replacement = r'\1,\n    \2'
    
    # Apply the fix
    fixed_content = re.sub(pattern, replacement, content)
    
    # Write back the fixed content
    with open(callbacks_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed trailing comma syntax errors in callbacks.py")

if __name__ == "__main__":
    fix_trailing_commas()
