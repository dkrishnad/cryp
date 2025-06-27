#!/usr/bin/env python3
"""
Minimal dashboard test - just check if basic app works
"""
import dash
from dash import html
import dash_bootstrap_components as dbc

print("Creating minimal test app...")

# Create a minimal app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Simple layout
app.layout = html.Div([
    html.H1("Dashboard Test"),
    html.P("If you can see this, the dashboard is working!")
])

if __name__ == "__main__":
    print("Starting minimal test dashboard on port 8051...")
    try:
        app.run(debug=False, port=8051, host="127.0.0.1")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
