#!/usr/bin/env python3
"""
Minimal dashboard test to see if intervals work
"""
import dash
from dash import dcc, html, Input, Output, callback

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Minimal Interval Test"),
    html.Div(id="test-output", children="Waiting for interval..."),
    dcc.Interval(id="test-interval", interval=2000, n_intervals=0)  # 2 seconds
])

@app.callback(
    Output('test-output', 'children'),
    Input('test-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_test(n):
    print(f"🔥 INTERVAL CALLBACK TRIGGERED: n={n}")
    return f"Interval triggered {n} times"

if __name__ == "__main__":
    print("🚀 Starting minimal interval test on port 8051...")
    app.run(debug=True, port=8051)
