#!/usr/bin/env python3
"""
Minimal layout test - just basic structure
"""
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Minimal layout just for testing
minimal_layout = html.Div([
    html.H1("Crypto Bot Dashboard", className="text-center text-success"),
    html.Div(id="test-output", children="Dashboard loading..."),
    dcc.Interval(id="test-interval", interval=1000, n_intervals=0)
])

if __name__ == "__main__":
    print("Testing minimal layout...")
    try:
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.layout = minimal_layout
        print("✓ Minimal layout created successfully")
        print("✅ Layout structure is working")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
