#!/usr/bin/env python3
"""
Emergency Minimal Dashboard
Tests basic Dash functionality without complex components
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

from minimal_dash_app import app
from dash import html, dcc, Input, Output
import time

# Simple test layout
app.layout = html.Div([
    html.H1("🚀 Emergency Dashboard Test", style={'textAlign': 'center'}),
    html.Div([
        html.Button("Test Button", id="test-btn", n_clicks=0),
        html.Div(id="test-output", children="Click the button to test interactivity"),
    ], style={'margin': '20px', 'textAlign': 'center'})
])

# Simple test callback
@app.callback(
    Output('test-output', 'children'),
    Input('test-btn', 'n_clicks')
)
def test_callback(n_clicks):
    if n_clicks > 0:
        return f"✅ SUCCESS! Button clicked {n_clicks} times. Callbacks are working!"
    return "Click the button to test interactivity"

if __name__ == '__main__':
    print("🚀 Starting Emergency Dashboard...")
    print("📊 Testing basic Dash functionality...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=True,
            host='localhost',
            port=8050,
            dev_tools_ui=True,
            dev_tools_props_check=True
        )
    except Exception as e:
        print(f"❌ Error starting emergency dashboard: {e}")
