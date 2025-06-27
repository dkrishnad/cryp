#!/usr/bin/env python3
"""
Script to check for duplicate callback outputs in dashboard/callbacks.py
"""

import re
from collections import Counter
import os

def check_duplicate_outputs():
    file_path = 'dashboard/callbacks.py'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return
    
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
    
    if duplicates:
        for output_id, count in sorted(duplicates.items()):
            print(f'{output_id}: {count} times')
    else:
        print("No duplicate outputs found!")
    
    print(f'\nTotal unique outputs: {len(output_counts)}')
    print(f'Total duplicate outputs: {len(duplicates)}')
    
    # Show all outputs for reference
    print('\n=== ALL OUTPUT TARGETS ===')
    for output_id, count in sorted(output_counts.items()):
        print(f'{output_id}: {count} time(s)')
    
    return duplicates

if __name__ == "__main__":
    check_duplicate_outputs()
