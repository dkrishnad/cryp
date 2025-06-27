#!/usr/bin/env python3
"""
Final comprehensive duplicate callback check for callbacks.py
Checks for any remaining duplicate Output declarations
"""

import re
from collections import defaultdict, Counter

def analyze_callbacks(file_path):
    """Analyze all callbacks in the file for duplicates"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Total file length: {len(content.splitlines())} lines")
    
    # Find all @app.callback decorators and their following Output declarations
    callback_pattern = r'@app\.callback\((.*?)\)'
    output_pattern = r'Output\([\'"]([^\'"]+)[\'"],\s*[\'"]([^\'"]+)[\'"](?:,\s*allow_duplicate=True)?\)'
    
    callbacks = []
    lines = content.splitlines()
    
    # Track outputs and their line numbers
    output_tracking = defaultdict(list)
    function_tracking = defaultdict(list)
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('@app.callback'):
            # Found a callback, collect the full decorator
            callback_start = i
            decorator_lines = [line]
            i += 1
            
            # Continue collecting decorator lines until we hit the function definition
            while i < len(lines) and not lines[i].strip().startswith('def '):
                if lines[i].strip():  # Skip empty lines
                    decorator_lines.append(lines[i].strip())
                i += 1
            
            # Get the function name
            if i < len(lines):
                func_line = lines[i].strip()
                func_match = re.match(r'def\s+(\w+)\s*\(', func_line)
                func_name = func_match.group(1) if func_match else "unknown"
            else:
                func_name = "unknown"
            
            # Join all decorator lines and extract outputs
            full_decorator = ' '.join(decorator_lines)
            outputs = re.findall(output_pattern, full_decorator)
            
            callback_info = {
                'line_start': callback_start + 1,  # 1-indexed
                'function_name': func_name,
                'outputs': outputs,
                'full_decorator': full_decorator
            }
            callbacks.append(callback_info)
            
            # Track outputs and functions
            for output_id, output_prop in outputs:
                output_key = f"{output_id}.{output_prop}"
                output_tracking[output_key].append((callback_start + 1, func_name))
            
            function_tracking[func_name].append((callback_start + 1, outputs))
        
        i += 1
    
    print(f"\nFound {len(callbacks)} total callbacks")
    
    # Check for duplicate outputs
    duplicate_outputs = {k: v for k, v in output_tracking.items() if len(v) > 1}
    duplicate_functions = {k: v for k, v in function_tracking.items() if len(v) > 1}
    
    print(f"\n=== DUPLICATE OUTPUTS ANALYSIS ===")
    if duplicate_outputs:
        print(f"Found {len(duplicate_outputs)} duplicate outputs:")
        for output, locations in duplicate_outputs.items():
            print(f"  {output}:")
            for line_num, func_name in locations:
                print(f"    Line {line_num}: {func_name}()")
    else:
        print("✓ No duplicate outputs found!")
    
    print(f"\n=== DUPLICATE FUNCTION NAMES ===")
    if duplicate_functions:
        print(f"Found {len(duplicate_functions)} duplicate function names:")
        for func_name, locations in duplicate_functions.items():
            print(f"  {func_name}():")
            for line_num, outputs in locations:
                output_strs = [f"{oid}.{oprop}" for oid, oprop in outputs]
                print(f"    Line {line_num}: outputs {output_strs}")
    else:
        print("✓ No duplicate function names found!")
    
    # Check for allow_duplicate=True usage
    allow_duplicate_pattern = r'allow_duplicate\s*=\s*True'
    allow_duplicate_matches = []
    for i, line in enumerate(lines):
        if re.search(allow_duplicate_pattern, line):
            allow_duplicate_matches.append(i + 1)
    
    print(f"\n=== ALLOW_DUPLICATE=TRUE USAGE ===")
    if allow_duplicate_matches:
        print(f"Found {len(allow_duplicate_matches)} instances of allow_duplicate=True:")
        for line_num in allow_duplicate_matches:
            print(f"  Line {line_num}: {lines[line_num-1].strip()}")
    else:
        print("✓ No allow_duplicate=True found (good - indicates duplicates were removed)")
    
    return {
        'total_callbacks': len(callbacks),
        'duplicate_outputs': duplicate_outputs,
        'duplicate_functions': duplicate_functions,
        'allow_duplicate_usage': allow_duplicate_matches,
        'callbacks': callbacks
    }

if __name__ == "__main__":
    file_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py"
    results = analyze_callbacks(file_path)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total callbacks: {results['total_callbacks']}")
    print(f"Duplicate outputs: {len(results['duplicate_outputs'])}")
    print(f"Duplicate functions: {len(results['duplicate_functions'])}")
    print(f"Allow_duplicate usage: {len(results['allow_duplicate_usage'])}")
    
    if not results['duplicate_outputs'] and not results['duplicate_functions']:
        print("\n🎉 SUCCESS: No duplicates detected! File appears clean.")
    else:
        print("\n⚠️  WARNING: Duplicates still exist and need to be addressed.")
