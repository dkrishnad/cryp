#!/usr/bin/env python3
"""
Minimal dashboard startup - no callbacks to test layout only
"""
import dash
import dash_bootstrap_components as dbc
import sys
import os

# Fix encoding issues on Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(message):
    """Print message with encoding safety"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        print(message.encode('ascii', 'replace').decode('ascii'))

try:
    safe_print("Starting minimal dashboard test...")
    
    # Create app
    app = dash.Dash(
        __name__, 
        suppress_callback_exceptions=True,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
        ]
    )
    
    safe_print("Loading layout...")
    from layout import layout
    
    app.layout = layout
    
    safe_print("Layout loaded successfully!")
    if hasattr(layout, 'children') and layout.children:
        safe_print(f"Layout has {len(layout.children)} main components")
    
    safe_print("Starting server on http://localhost:8050...")
    app.run(debug=False, host="127.0.0.1", port=8050)
    
except Exception as e:
    safe_print(f"Error: {e}")
    import traceback
    traceback.print_exc()
