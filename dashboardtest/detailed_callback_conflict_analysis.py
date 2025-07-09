#!/usr/bin/env python3
"""
Detailed Callback Conflict Analysis
Focuses specifically on finding multiple callbacks with the same Input
"""

import re
import ast
from collections import defaultdict

def analyze_callback_conflicts():
    """Analyze callback conflicts in detail."""
    
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into callback blocks
    callback_blocks = []
    lines = content.split('\n')
    
    current_callback = []
    in_callback = False
    
    for i, line in enumerate(lines):
        if '@app.callback' in line:
            if current_callback:
                callback_blocks.append({
                    'lines': current_callback,
                    'start_line': i - len(current_callback),
                    'end_line': i
                })
            current_callback = [line]
            in_callback = True
        elif in_callback:
            current_callback.append(line)
            if line.strip().startswith('def ') and 'def ' in line:
                callback_blocks.append({
                    'lines': current_callback,
                    'start_line': i - len(current_callback) + 1,
                    'end_line': i
                })
                current_callback = []
                in_callback = False
    
    # Add the last callback if exists
    if current_callback:
        callback_blocks.append({
            'lines': current_callback,
            'start_line': len(lines) - len(current_callback),
            'end_line': len(lines)
        })
    
    print(f"Found {len(callback_blocks)} callback blocks")
    
    # Analyze each callback for inputs
    input_usage = defaultdict(list)
    
    for i, callback_block in enumerate(callback_blocks):
        callback_text = '\n'.join(callback_block['lines'])
        
        # Find all Input statements
        input_matches = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_text)
        
        for input_id in input_matches:
            input_usage[input_id].append({
                'callback_index': i,
                'start_line': callback_block['start_line'],
                'end_line': callback_block['end_line'],
                'preview': callback_text[:200]
            })
    
    # Find conflicts
    conflicts = {}
    for input_id, usages in input_usage.items():
        if len(usages) > 1:
            conflicts[input_id] = usages
    
    print("\n=== CALLBACK CONFLICT ANALYSIS ===")
    if conflicts:
        print("🔴 CONFLICTS FOUND:")
        for input_id, usages in conflicts.items():
            print(f"\nInput: '{input_id}' used by {len(usages)} callbacks:")
            for i, usage in enumerate(usages):
                print(f"  Callback {i+1}: Lines {usage['start_line']}-{usage['end_line']}")
                print(f"    Preview: {usage['preview'][:100]}...")
    else:
        print("✅ No conflicts found")
    
    return conflicts

if __name__ == "__main__":
    conflicts = analyze_callback_conflicts()
