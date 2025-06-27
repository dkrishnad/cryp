#!/usr/bin/env python3
"""
Analyze duplicate callback outputs in dashboard/callbacks.py
"""
import re
from collections import Counter

def analyze_callback_duplicates():
    file_path = 'dashboard/callbacks.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    
    # Find all Output elements and their target IDs
    output_pattern = r'Output\([\'\"](.*?)[\'\"]'
    outputs = re.findall(output_pattern, content)
    
    # Count occurrences
    output_counts = Counter(outputs)
    
    print('=== DUPLICATE OUTPUT TARGETS ===')
    duplicates = {k: v for k, v in output_counts.items() if v > 1}
    for output_id, count in sorted(duplicates.items()):
        print(f'{output_id}: {count} times')
    
    print(f'\nTotal unique outputs: {len(output_counts)}')
    print(f'Total duplicate outputs: {len(duplicates)}')
    
    # Find the specific callback functions that have duplicates
    print('\n=== CALLBACK FUNCTIONS WITH DUPLICATES ===')
    for output_id in sorted(duplicates.keys()):
        print(f'\nSearching for callbacks targeting: {output_id}')
        
        # Find callback functions that target this output
        callback_pattern = rf'@app\.callback\([\s\S]*?Output\([\'\"]{re.escape(output_id)}[\'\"][\s\S]*?\)[\s\S]*?def\s+(\w+)'
        matches = re.findall(callback_pattern, content, re.MULTILINE)
        
        if matches:
            print(f'  Found in functions: {", ".join(matches)}')
        else:
            # Try a simpler search
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if f'Output(\'{output_id}\'' in line or f'Output("{output_id}"' in line:
                    # Look backwards for the function name
                    for j in range(i, max(0, i-20), -1):
                        if 'def ' in lines[j]:
                            func_name = lines[j].split('def ')[1].split('(')[0]
                            print(f'  Found around line {i+1} in function: {func_name}')
                            break

if __name__ == '__main__':
    analyze_callback_duplicates()
