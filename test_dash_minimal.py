#!/usr/bin/env python3
"""
Minimal Dash test to check if callbacks work
"""
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.H1("Minimal Dash Test"),
    dbc.Button("Test Button", id="test-btn", color="primary"),
    html.Div(id="test-output", style={"marginTop": "20px", "fontSize": "18px"})
])

@app.callback(
    Output('test-output', 'children'),
    Input('test-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_callback(n_clicks):
    if n_clicks:
        return f"Button clicked {n_clicks} times!"
    return "Button not clicked yet"

if __name__ == "__main__":
    print("Starting minimal Dash test on port 8051...")
    app.run(debug=True, port=8051, host='127.0.0.1')
