#!/usr/bin/env python3
"""
Fix duplicate callbacks by adding allow_duplicate=True to callbacks
"""

# Read the file
with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the callback patterns that need allow_duplicate=True
fixes = [
    # Pattern: find callback decorators without allow_duplicate
    {
        'find': "@app.callback(\n    Output('current-signal-display', 'children'),\n    [Input('refresh-current-signal', 'n_clicks')]\n)",
        'replace': "@app.callback(\n    Output('current-signal-display', 'children'),\n    [Input('refresh-current-signal', 'n_clicks')],\n    allow_duplicate=True\n)"
    },
    {
        'find': "@app.callback(\n    Output('auto-balance-display', 'children'),\n    Input('auto-trading-interval', 'n_clicks'),",
        'replace': "@app.callback(\n    Output('auto-balance-display', 'children'),\n    Input('auto-trading-interval', 'n_clicks'),\n    allow_duplicate=True,"
    }
]

# Apply fixes
for fix in fixes:
    content = content.replace(fix['find'], fix['replace'])

print("Manual fix script created. Run this manually to fix duplicates.")
