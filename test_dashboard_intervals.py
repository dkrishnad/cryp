#!/usr/bin/env python3
"""
Debug: Test if main dashboard intervals work with simplified layout
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Handle both direct execution and module import
try:
    # Try relative imports first (when run as module)
    from dashboard.dash_app import app, server
except ImportError:
    # Fallback to absolute imports (when run directly)
    from dashboard.dash_app import app, server

# Simple test layout with just the interval
test_layout = html.Div([
    html.H1("Dashboard Interval Debug Test"),
    html.Div(id="test-output-simple", children="Waiting for dashboard interval..."),
    dcc.Interval(id="test-interval-simple", interval=3000, n_intervals=0)  # 3 seconds
])

@app.callback(
    Output('test-output-simple', 'children'),
    Input('test-interval-simple', 'n_intervals'),
    prevent_initial_call=False
)
def update_test_simple(n):
    print(f"🔥 DASHBOARD INTERVAL WORKING: n={n}")
    return f"Dashboard interval triggered {n} times"

app.layout = test_layout

if __name__ == "__main__":
    print("🚀 Starting dashboard interval debug test on port 8052...")
    app.run(debug=True, port=8052)
