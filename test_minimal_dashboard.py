import dash
from dash import html, dcc, Input, Output, callback_context
import dash_bootstrap_components as dbc

# Create a minimal test app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Simple layout
app.layout = html.Div([
    html.H1("Dashboard Test"),
    html.Div(id="selected-symbol-store", style={"display": "none"}),
    dcc.Dropdown(
        id="sidebar-symbol",
        options=[
            {"label": "BTC", "value": "btcusdt"},
            {"label": "ETH", "value": "ethusdt"}
        ],
        value="btcusdt"
    ),
    html.Div(id="live-price", children="Price: --"),
    dbc.Button("Open Long", id="open-long-btn", color="success"),
    html.Div(id="trade-result", children="No trades yet"),
    dcc.Interval(id="test-interval", interval=2000, n_intervals=0),
    html.Div(id="test-output", children="Test: 0")
])

# Test callbacks
@app.callback(
    Output('test-output', 'children'),
    Input('test-interval', 'n_intervals'),
    prevent_initial_call=False
)
def test_callback(n):
    print(f"[TEST] Interval callback triggered: {n}")
    return f"Test: {n}"

@app.callback(
    Output('trade-result', 'children'),
    Input('open-long-btn', 'n_clicks'),
    prevent_initial_call=True
)
def button_callback(n_clicks):
    print(f"[TEST] Button callback triggered: {n_clicks}")
    return f"Button clicked {n_clicks} times"

@app.callback(
    Output('live-price', 'children'),
    Input('sidebar-symbol', 'value'),
    prevent_initial_call=False
)
def symbol_callback(symbol):
    print(f"[TEST] Symbol callback triggered: {symbol}")
    return f"Price for {symbol}: $50000"

if __name__ == "__main__":
    print("Starting minimal test dashboard...")
    app.run(debug=True, port=8051)
