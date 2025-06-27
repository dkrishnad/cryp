#!/usr/bin/env python3
"""
Ultra-simple dashboard starter - no Unicode, pure ASCII
Windows-compatible encoding-safe version
"""
import os
import sys

# Force UTF-8 encoding
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def print_safe(msg):
    """Print safely without encoding errors"""
    try:
        print(msg)
    except:
        print(msg.encode('ascii', 'replace').decode('ascii'))

def main():
    try:
        print_safe("Starting Crypto Trading Bot Dashboard...")
        print_safe("Initializing...")
        
        # Import components
        import dash
        import dash_bootstrap_components as dbc
        
        print_safe("Creating app...")
        app = dash.Dash(
            __name__,
            suppress_callback_exceptions=True,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        
        print_safe("Loading layout...")
        from layout import layout
        app.layout = layout
        
        print_safe("Importing callbacks...")
        import callbacks
        
        print_safe("Dashboard ready!")
        print_safe(f"Callbacks loaded: {len(app.callback_map)}")
        print_safe("")
        print_safe("Starting server on http://localhost:8050")
        print_safe("Press Ctrl+C to stop")
        print_safe("")
        
        # Start server
        app.run(debug=False, port=8050, host="127.0.0.1")
        
    except KeyboardInterrupt:
        print_safe("")
        print_safe("Dashboard stopped by user")
    except Exception as e:
        print_safe(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
