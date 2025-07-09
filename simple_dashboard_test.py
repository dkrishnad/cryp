#!/usr/bin/env python3
"""
Simple Dashboard Test - Check if callbacks are working
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import time

# Create a simple test app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Simple layout with one button and one output
app.layout = html.Div([
    html.H1("Dashboard Test", className="text-center mb-4"),
    
    html.Div([
        dbc.Button("Test Button", id="test-btn", color="primary", size="lg", className="me-2"),
        dbc.Button("API Test", id="api-test-btn", color="secondary", size="lg"),
    ], className="text-center mb-4"),
    
    html.Div(id="test-output", className="text-center"),
    html.Div(id="api-output", className="text-center mt-3"),
    
    # Add some stores and intervals like the main app
    dcc.Store(id="test-store", storage_type="memory"),
    dcc.Interval(id="test-interval", interval=3000, n_intervals=0),
])

# Simple callback
@app.callback(
    Output("test-output", "children"),
    Input("test-btn", "n_clicks"),
    prevent_initial_call=True
)
def test_callback(n_clicks):
    if n_clicks:
        return html.Div([
            html.H4(f"Button clicked {n_clicks} times!", className="text-success"),
            html.P(f"Timestamp: {time.strftime('%H:%M:%S')}")
        ])
    return ""

# API test callback
@app.callback(
    Output("api-output", "children"),
    Input("api-test-btn", "n_clicks"),
    prevent_initial_call=True
)
def api_test_callback(n_clicks):
    if n_clicks:
        try:
            import requests
            response = requests.get("http://localhost:8000/status", timeout=5)
            if response.status_code == 200:
                return html.Div([
                    html.H5("✅ Backend API Connected", className="text-success"),
                    html.P(f"Response: {response.json()}")
                ])
            else:
                return html.Div([
                    html.H5("❌ Backend API Error", className="text-danger"),
                    html.P(f"Status: {response.status_code}")
                ])
        except Exception as e:
            return html.Div([
                html.H5("❌ Connection Error", className="text-danger"),
                html.P(f"Error: {str(e)}")
            ])
    return ""

# Interval callback
@app.callback(
    Output("test-store", "data"),
    Input("test-interval", "n_intervals")
)
def update_store(n_intervals):
    return {"timestamp": time.time(), "intervals": n_intervals}

if __name__ == "__main__":
    print("🚀 Starting Simple Dashboard Test...")
    print("📍 URL: http://localhost:8050")
    print("🔍 Check browser console for JavaScript errors")
    app.run(debug=True, port=8050)
