#!/usr/bin/env python3
"""
Minimal Dashboard Test - Isolate the 500 error issue
"""
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Create a minimal Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Simple layout
app.layout = html.Div([
    html.H1("Dashboard Test", style={"textAlign": "center"}),
    html.Hr(),
    dbc.Button("Test Backend Connection", id="test-btn", color="primary", className="mb-3"),
    html.Div(id="test-output", className="mt-3"),
    html.Hr(),
    html.P("If you can see this page, the dashboard basic setup is working."),
    html.P("The 500 error is likely in the callbacks or imports.")
])

# Simple callback to test backend
@app.callback(
    Output('test-output', 'children'),
    Input('test-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_backend_connection(n_clicks):
    if n_clicks:
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return html.Div([
                    html.H5("✅ Backend Connection Successful", style={"color": "green"}),
                    html.P(f"Status: {data.get('status', 'Unknown')}"),
                    html.P(f"Message: {data.get('message', 'No message')}")
                ])
            else:
                return html.Div([
                    html.H5("❌ Backend Connection Failed", style={"color": "red"}),
                    html.P(f"HTTP Status: {response.status_code}")
                ])
        except Exception as e:
            return html.Div([
                html.H5("❌ Backend Connection Error", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return "Click the button to test backend connection"

if __name__ == '__main__':
    print("Starting minimal dashboard test...")
    print("Visit: http://localhost:8051")
    app.run(
        debug=True,
        host='localhost',
        port=8051,  # Different port to avoid conflict
        dev_tools_ui=True,
        dev_tools_props_check=True
    )
