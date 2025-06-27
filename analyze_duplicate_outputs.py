#!/usr/bin/env python3
"""
Analyze dashboard/callbacks.py for duplicate callback outputs
"""
import re
from collections import Counter

def analyze_duplicate_outputs():
    file_path = 'dashboard/callbacks.py'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Find all Output elements and their target IDs
    output_pattern = r'Output\([\'\"](.*?)[\'\"]'
    outputs = re.findall(output_pattern, content)

    # Count occurrences
    output_counts = Counter(outputs)

    print('=== DUPLICATE OUTPUT TARGETS ===')
    duplicates = {k: v for k, v in output_counts.items() if v > 1}
    
    if not duplicates:
        print("No duplicate outputs found!")
        return
    
    for output_id, count in sorted(duplicates.items()):
        print(f'{output_id}: {count} times')

    print(f'\nTotal unique outputs: {len(output_counts)}')
    print(f'Total duplicate outputs: {len(duplicates)}')
    
    # Find line numbers for duplicates
    print('\n=== DUPLICATE LOCATIONS ===')
    lines = content.split('\n')
    for output_id in duplicates.keys():
        print(f'\n{output_id}:')
        for i, line in enumerate(lines, 1):
            if f"'{output_id}'" in line or f'"{output_id}"' in line:
                if 'Output(' in line:
                    print(f'  Line {i}: {line.strip()}')

if __name__ == "__main__":
    analyze_duplicate_outputs()
