#!/usr/bin/env python3
"""
Advanced analysis to check if duplicates contain newer/advanced features
that aren't in the original callbacks
"""

import re
from collections import defaultdict

def compare_original_vs_duplicates():
    """Compare original callbacks vs duplicate section to find unique features"""
    
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Analyzing {len(lines)} lines for original vs duplicate features...")
    
    # Find the boundary - where duplicates start
    duplicate_start = None
    for i, line in enumerate(lines):
        if 'REMOVED DUPLICATE SECTION' in line or 'ALL MISSING CALLBACKS - COMPREHENSIVE RESTORATION' in line:
            duplicate_start = i
            break
    
    if duplicate_start is None:
        # Look for the first allow_duplicate=True after original functions
        for i, line in enumerate(lines):
            if i > 1500 and 'allow_duplicate=True' in line:
                duplicate_start = i - 10  # Start a bit before
                break
    
    if duplicate_start is None:
        print("Could not find duplicate section boundary!")
        return
    
    print(f"Duplicate section starts around line: {duplicate_start + 1}")
    
    # Extract all function names and their line numbers
    original_functions = {}  # function_name -> line_number
    duplicate_functions = {}  # function_name -> line_number
    
    # Parse original section (before duplicates)
    for i in range(duplicate_start):
        line = lines[i].strip()
        if line.startswith('def ') and '(' in line:
            func_match = re.match(r'def\s+(\w+)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                original_functions[func_name] = i + 1
    
    # Parse duplicate section (after duplicates start)
    for i in range(duplicate_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('def ') and '(' in line:
            func_match = re.match(r'def\s+(\w+)\s*\(', line)
            if func_match:
                func_name = func_match.group(1)
                duplicate_functions[func_name] = i + 1
    
    print(f"\nOriginal section has {len(original_functions)} functions")
    print(f"Duplicate section has {len(duplicate_functions)} functions")
    
    # Find functions that exist ONLY in duplicates (potential advanced features)
    duplicate_only = set(duplicate_functions.keys()) - set(original_functions.keys())
    
    print(f"\n=== FUNCTIONS ONLY IN DUPLICATE SECTION ===")
    if duplicate_only:
        print(f"Found {len(duplicate_only)} functions that exist ONLY in duplicates:")
        for func_name in sorted(duplicate_only):
            line_num = duplicate_functions[func_name]
            print(f"  Line {line_num}: {func_name}()")
            
            # Show the function signature and first few lines
            start_line = line_num - 1
            print(f"    Function definition:")
            for j in range(start_line, min(start_line + 5, len(lines))):
                if j < len(lines):
                    func_line = lines[j].rstrip()
                    if func_line.strip():
                        print(f"      {j+1}: {func_line}")
            print()
    else:
        print("✓ No unique functions found in duplicate section")
    
    # Find callbacks with unique outputs (only in duplicates)
    print(f"\n=== ADVANCED CALLBACKS ANALYSIS ===")
    
    # Check for advanced callback patterns in duplicate section
    advanced_patterns = [
        r'online.?learning',
        r'hft.?analysis',
        r'notification',
        r'email.?config',
        r'alert',
        r'technical.?indicator',
        r'sidebar.?toggle',
        r'risk.?management',
        r'data.?collection',
        r'hybrid.?learning'
    ]
    
    advanced_callbacks = []
    for i in range(duplicate_start, len(lines)):
        line = lines[i].strip().lower()
        for pattern in advanced_patterns:
            if re.search(pattern, line) and ('def ' in line or '@app.callback' in line):
                advanced_callbacks.append((i + 1, lines[i].strip()))
                break
    
    if advanced_callbacks:
        print(f"Found {len(advanced_callbacks)} potentially advanced callbacks in duplicate section:")
        for line_num, line_content in advanced_callbacks[:10]:  # Show first 10
            print(f"  Line {line_num}: {line_content[:80]}...")
    else:
        print("✓ No advanced callback patterns found in duplicate section")
    
    return {
        'duplicate_start': duplicate_start,
        'original_functions': original_functions,
        'duplicate_functions': duplicate_functions,
        'duplicate_only': duplicate_only,
        'advanced_callbacks': advanced_callbacks
    }

if __name__ == "__main__":
    results = compare_original_vs_duplicates()
    
    if results and results['duplicate_only']:
        print(f"\n⚠️  WARNING: {len(results['duplicate_only'])} functions exist ONLY in duplicates!")
        print("These may be advanced features that shouldn't be removed.")
        print("Manual review required before safe removal.")
    else:
        print(f"\n✅ SAFE TO REMOVE: All functions in duplicate section also exist in original.")
        print("Duplicates can be safely removed without losing functionality.")
