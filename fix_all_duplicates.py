#!/usr/bin/env python3
"""
Comprehensive fix for all duplicate callback outputs
"""

import re

# Read the file
with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track which outputs we've seen
seen_outputs = set()
modified_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is a callback decorator
    if '@app.callback(' in line:
        # Find the end of this callback decorator
        callback_lines = [line]
        i += 1
        paren_count = line.count('(') - line.count(')')
        
        while i < len(lines) and (paren_count > 0 or not lines[i].strip().startswith('def ')):
            callback_lines.append(lines[i])
            paren_count += lines[i].count('(') - lines[i].count(')')
            i += 1
        
        # Extract output IDs from this callback
        callback_text = ''.join(callback_lines)
        output_matches = re.findall(r"Output\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]", callback_text)
        
        # Check if any outputs are duplicates
        current_outputs = [(match[0], match[1]) for match in output_matches]
        is_duplicate = any(output in seen_outputs for output in current_outputs)
        
        if is_duplicate:
            # Add allow_duplicate=True to this callback
            for j, cb_line in enumerate(callback_lines):
                if ')' in cb_line and 'def ' not in cb_line and j == len(callback_lines) - 1:
                    # This is the closing line of the callback decorator
                    if 'allow_duplicate=True' not in cb_line:
                        callback_lines[j] = cb_line.replace(')', ',\n    allow_duplicate=True)')
                    break
            
            print(f"Added allow_duplicate=True to callback with outputs: {current_outputs}")
        
        # Add all outputs to seen set
        for output in current_outputs:
            seen_outputs.add(output)
        
        # Add the modified callback lines
        modified_lines.extend(callback_lines)
    else:
        modified_lines.append(line)
        i += 1

# Write the modified content back
with open('dashboard/callbacks.py', 'w', encoding='utf-8') as f:
    f.writelines(modified_lines)

print("✅ Fixed all duplicate callback outputs!")
print("🔄 Restart the app to check if all duplicates are resolved.")
