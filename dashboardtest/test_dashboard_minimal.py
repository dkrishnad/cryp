#!/usr/bin/env python3
"""
Test Dashboard - Minimal version to test if Dash works
"""
import os
import sys

# Set UTF-8 for Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def main():
    print("🎨 Starting test dashboard...")
    
    try:
        import dash
        from dash import html, dcc
        import dash_bootstrap_components as dbc
        
        print("✅ Dash imports successful")
        
        app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        
        app.layout = html.Div([
            html.H1("🚀 Test Crypto Bot Dashboard"),
            html.P("✨ This is a minimal test dashboard"),
            html.P("🎉 If you see this, Dash is working!")
        ])
        
        print("🌐 Starting test dashboard on http://localhost:8050")
        app.run(debug=False, port=8050, host="127.0.0.1")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
