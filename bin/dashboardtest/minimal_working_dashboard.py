#!/usr/bin/env python3
"""
MINIMAL WORKING DASHBOARD - Step 1
Basic dashboard with just core components to verify Dash is working
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Core imports
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Minimal layout
app.layout = html.Div([
    dbc.Container([
        html.H1("🚀 Crypto Trading Bot Dashboard", className="text-center mb-4"),
        
        dbc.Alert([
            html.H4("✅ Dashboard is Working!", className="alert-heading"),
            html.P("This is a minimal test to verify Dash is functioning properly."),
            html.Hr(),
            html.P("If you can see this, the core dashboard framework is working."),
        ], color="success"),
        
        dbc.Card([
            dbc.CardHeader("Test Controls"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Test Button", id="test-btn", color="primary", className="mb-2"),
                        html.Div(id="test-output", className="mt-2")
                    ], width=6),
                    dbc.Col([
                        dcc.Dropdown(
                            id="test-dropdown",
                            options=[
                                {"label": "Option 1", "value": "opt1"},
                                {"label": "Option 2", "value": "opt2"},
                                {"label": "Option 3", "value": "opt3"}
                            ],
                            value="opt1",
                            placeholder="Select an option"
                        ),
                        html.Div(id="dropdown-output", className="mt-2")
                    ], width=6)
                ])
            ])
        ], className="mb-4"),
        
        dbc.Card([
            dbc.CardHeader("Backend Connectivity Test"),
            dbc.CardBody([
                dbc.Button("Test Backend", id="backend-test-btn", color="info"),
                html.Div(id="backend-output", className="mt-2")
            ])
        ])
    ], fluid=True)
])

# Test callbacks
@callback(
    Output("test-output", "children"),
    Input("test-btn", "n_clicks"),
    prevent_initial_call=True
)
def test_button_callback(n_clicks):
    return dbc.Alert(f"✅ Button clicked {n_clicks} times! Callbacks are working.", color="success")

@callback(
    Output("dropdown-output", "children"), 
    Input("test-dropdown", "value")
)
def test_dropdown_callback(value):
    return dbc.Alert(f"✅ Selected: {value}. Dropdown callbacks working.", color="info")

@callback(
    Output("backend-output", "children"),
    Input("backend-test-btn", "n_clicks"),
    prevent_initial_call=True
)
def test_backend_callback(n_clicks):
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            return dbc.Alert("✅ Backend is responding! API connectivity works.", color="success")
        else:
            return dbc.Alert(f"⚠️ Backend responded with status {response.status_code}", color="warning")
    except Exception as e:
        return dbc.Alert(f"❌ Backend connection failed: {e}", color="danger")

if __name__ == "__main__":
    print("🚀 Starting Minimal Dashboard Test...")
    print("📊 Dashboard URL: http://localhost:8050")
    
    app.run(
        debug=True,
        host='localhost', 
        port=8050,
        dev_tools_ui=True,
        dev_tools_props_check=True
    )
