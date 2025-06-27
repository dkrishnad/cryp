import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from layout import layout
import sys
import traceback

# Create app with debug enabled
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

try:
    app.layout = layout
    print("Layout loaded successfully")
except Exception as e:
    print(f"ERROR: Failed to load layout: {e}")
    traceback.print_exc()
    # Create a simple fallback layout
    app.layout = html.Div([
        html.H1("Layout Error"),
        html.P(f"Error: {str(e)}")
    ])

# Add a simple test callback
@callback(
    Output("interval-prediction", "children"),
    Input("interval-indicators", "n_intervals")
)
def test_callback(n_intervals):
    print(f"TEST CALLBACK TRIGGERED: {n_intervals}")
    return f"Callback working! Interval: {n_intervals}"

if __name__ == "__main__":
    print("Starting debug app on port 8053...")
    app.run(host="0.0.0.0", port=8053, debug=True)
