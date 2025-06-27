#!/usr/bin/env python3
"""
Fix the hybrid_learning_layout.py indentation issues
"""

# Read the current file
file_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard\hybrid_learning_layout.py"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    print("Looking for problematic lines...")
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Check for lines with unexpected indentation
        if line.strip() and len(line) - len(line.lstrip()) > 20:
            print(f"Line {i}: Suspicious indentation ({len(line) - len(line.lstrip())} spaces)")
            print(f"  Content: {repr(line[:50])}")
        
        # Look for specific problems
        if "return stats_items" in line and len(line) - len(line.lstrip()) != 8:
            print(f"Line {i}: Found problematic return statement")
            print(f"  Current: {repr(line)}")
            print(f"  Should be: {repr('        return stats_items')}")
        
        if "except Exception as e:" in line and len(line) - len(line.lstrip()) > 12:
            print(f"Line {i}: Found problematic except statement")
            print(f"  Current: {repr(line)}")
    
    print("\nDone analyzing file.")
    
except Exception as e:
    print(f"Error reading file: {e}")
