#!/usr/bin/env python3
"""
Quick fix for duplicate callback outputs
Add allow_duplicate=True to specific problematic callbacks
"""

import re

# Read the callbacks file
with open(r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# List of specific patterns to fix
patterns_to_fix = [
    # Pattern 1: Auto trading stats callback
    {
        'pattern': r'(\[Input\(\'auto-trading-interval\', \'n_clicks\'\)\],\s*prevent_initial_call=False)\)',
        'replacement': r'\1,\n    allow_duplicate=True)'
    },
    # Pattern 2: Live price interval callbacks  
    {
        'pattern': r'(\[Input\(\'live-price-interval\', \'n_intervals\'\)\])\)',
        'replacement': r'\1,\n    allow_duplicate=True)'
    },
    # Pattern 3: Current signal callbacks
    {
        'pattern': r'(\[Input\(\'refresh-current-signal\', \'n_clicks\'\)\])\)',
        'replacement': r'\1,\n    allow_duplicate=True)'
    }
]

# Apply fixes
changes_made = 0
for pattern_info in patterns_to_fix:
    matches = re.findall(pattern_info['pattern'], content)
    if matches:
        content = re.sub(pattern_info['pattern'], pattern_info['replacement'], content)
        changes_made += len(matches)
        print(f"Fixed {len(matches)} occurrences of pattern")

# Write back the fixed content
with open(r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fixed {changes_made} duplicate callback issues!")
print("Now run the app again to check for remaining duplicates.")
