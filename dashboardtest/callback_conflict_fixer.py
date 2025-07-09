#!/usr/bin/env python3
"""
Callback Conflict Fixer
Automatically fixes duplicate callback inputs by consolidating or removing duplicates
"""

import re
import os
import shutil
from collections import defaultdict

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")

def fix_callbacks():
    """Fix callback conflicts in callbacks.py"""
    
    file_path = 'callbacks.py'
    
    # Create backup
    backup_file(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== FIXING CALLBACK CONFLICTS ===")
    
    # Fix 1: Remove duplicate inputs in the same callback (lines 2581-2583)
    print("1. Fixing duplicate inputs in same callback...")
    
    # Find and fix the specific duplicate input pattern
    duplicate_pattern = r'\[Input\(\'sidebar-predict-btn\', \'n_clicks\'\),\s*\n\s*Input\(\'sidebar-predict-btn\', \'n_clicks\'\),\s*\n\s*Input\(\'sidebar-predict-btn\', \'n_clicks\'\)\]'
    
    replacement = "[Input('sidebar-predict-btn', 'n_clicks')]"
    
    content = re.sub(duplicate_pattern, replacement, content, flags=re.MULTILINE)
    
    # Fix 2: Comment out duplicate callbacks that use the same inputs
    print("2. Commenting out duplicate callbacks...")
    
    # Let's identify and comment out specific problematic callbacks
    # We'll keep the main functional callbacks and comment out the duplicates
    
    # Find all callback blocks
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
                    'end_line': i,
                    'content': '\n'.join(current_callback)
                })
            current_callback = [line]
            in_callback = True
        elif in_callback:
            current_callback.append(line)
            if line.strip().startswith('def ') and 'def ' in line:
                callback_blocks.append({
                    'lines': current_callback,
                    'start_line': i - len(current_callback) + 1,
                    'end_line': i,
                    'content': '\n'.join(current_callback)
                })
                current_callback = []
                in_callback = False
    
    # Add the last callback if exists
    if current_callback:
        callback_blocks.append({
            'lines': current_callback,
            'start_line': len(lines) - len(current_callback),
            'end_line': len(lines),
            'content': '\n'.join(current_callback)
        })
    
    # Analyze inputs and find duplicates
    input_usage = defaultdict(list)
    
    for i, callback_block in enumerate(callback_blocks):
        callback_text = callback_block['content']
        
        # Find all Input statements
        input_matches = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_text)
        
        for input_id in input_matches:
            input_usage[input_id].append(i)
    
    # Find callbacks to disable (keep the first one, disable the rest)
    callbacks_to_disable = []
    
    for input_id, callback_indices in input_usage.items():
        if len(callback_indices) > 1:
            # Keep the first callback, disable the rest
            for callback_idx in callback_indices[1:]:
                callbacks_to_disable.append(callback_idx)
    
    callbacks_to_disable = list(set(callbacks_to_disable))  # Remove duplicates
    
    print(f"Found {len(callbacks_to_disable)} callbacks to disable")
    
    # Comment out the duplicate callbacks
    lines = content.split('\n')
    
    for callback_idx in callbacks_to_disable:
        if callback_idx < len(callback_blocks):
            callback_block = callback_blocks[callback_idx]
            start_line = callback_block['start_line']
            end_line = callback_block['end_line']
            
            # Comment out this callback
            for line_idx in range(start_line, min(end_line, len(lines))):
                if line_idx < len(lines):
                    lines[line_idx] = '# DISABLED_DUPLICATE: ' + lines[line_idx]
    
    # Write the fixed content
    fixed_content = '\n'.join(lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Callback conflicts fixed!")
    print(f"Disabled {len(callbacks_to_disable)} duplicate callbacks")
    
    # Fix 3: Remove duplicate component IDs in layout.py
    print("3. Fixing duplicate component IDs in layout.py...")
    
    layout_path = 'layout.py'
    if os.path.exists(layout_path):
        backup_file(layout_path)
        
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # Fix duplicate start-data-collection-btn
        layout_content = re.sub(
            r'id\s*=\s*[\'"]start-data-collection-btn[\'"]',
            'id="start-data-collection-btn-duplicate"',
            layout_content,
            count=1  # Only replace the first occurrence
        )
        
        # Fix duplicate stop-data-collection-btn
        layout_content = re.sub(
            r'id\s*=\s*[\'"]stop-data-collection-btn[\'"]',
            'id="stop-data-collection-btn-duplicate"',
            layout_content,
            count=1  # Only replace the first occurrence
        )
        
        with open(layout_path, 'w', encoding='utf-8') as f:
            f.write(layout_content)
        
        print("✅ Duplicate component IDs fixed!")
    
    print("\n=== FIXES COMPLETE ===")
    print("Next steps:")
    print("1. Test the dashboard")
    print("2. Check if buttons work now")
    print("3. Review disabled callbacks and re-enable if needed")

if __name__ == "__main__":
    fix_callbacks()
