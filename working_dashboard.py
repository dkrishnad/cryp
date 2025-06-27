import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import requests

# Create working dashboard from scratch
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Working layout
app.layout = dbc.Container([
    dcc.Store(id="selected-symbol-store", storage_type="memory"),
    
    html.H1("🚀 Crypto Bot Dashboard - WORKING VERSION", className="text-center mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Symbol Selection"),
            dcc.Dropdown(
                id="sidebar-symbol",
                options=[
                    {"label": "Bitcoin (BTC)", "value": "BTCUSDT"},
                    {"label": "Ethereum (ETH)", "value": "ETHUSDT"},
                    {"label": "Solana (SOL)", "value": "SOLUSDT"}
                ],
                value="BTCUSDT"
            ),
        ], width=4),
        
        dbc.Col([
            html.H3("Live Price"),
            html.Div(id="live-price", className="text-success", 
                    style={"fontSize": "24px", "fontWeight": "bold"}),
        ], width=4),
        
        dbc.Col([
            html.H3("Trade Actions"),
            dbc.Button("🔼 Open Long", id="open-long-btn", color="success", className="me-2"),
            dbc.Button("🔽 Open Short", id="open-short-btn", color="danger"),
            html.Div(id="trade-result", className="mt-2")
        ], width=4)
    ]),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            html.H3("Technical Indicators"),
            html.Div(id="indicators-display")
        ], width=6),
        
        dbc.Col([
            html.H3("System Status"),
            html.Div(id="status-display"),
            dcc.Interval(id="status-interval", interval=2000, n_intervals=0)
        ], width=6)
    ])
], fluid=True)

# Working callbacks
@app.callback(
    Output('status-display', 'children'),
    Input('status-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_status(n):
    print(f"[WORKING] Status callback triggered: {n}")
    return html.Div([
        html.P(f"✅ Dashboard Running - Update #{n}", className="text-success"),
        html.P(f"🔄 Auto-refresh every 2 seconds", className="text-info")
    ])

@app.callback(
    Output('selected-symbol-store', 'data'),
    Input('sidebar-symbol', 'value'),
    prevent_initial_call=False
)
def store_symbol(symbol):
    print(f"[WORKING] Symbol selected: {symbol}")
    return symbol

@app.callback(
    Output('live-price', 'children'),
    Input('selected-symbol-store', 'data'),
    prevent_initial_call=False
)
def update_price(symbol):
    if not symbol:
        symbol = "BTCUSDT"
    
    print(f"[WORKING] Fetching price for: {symbol}")
    try:
        resp = requests.get(f"http://localhost:8000/price", params={"symbol": symbol}, timeout=5)
        if resp.ok:
            data = resp.json()
            price = data.get("price", 0)
            print(f"[WORKING] Got price: {price}")
            return f"{symbol}: ${price:,.2f}"
        else:
            print(f"[WORKING] API error: {resp.status_code}")
            return f"{symbol}: API Error ({resp.status_code})"
    except Exception as e:
        print(f"[WORKING] Price fetch error: {e}")
        return f"{symbol}: Connection Error"

@app.callback(
    Output('indicators-display', 'children'),
    Input('selected-symbol-store', 'data'),
    prevent_initial_call=False
)
def update_indicators(symbol):
    if not symbol:
        symbol = "BTCUSDT"
        
    print(f"[WORKING] Fetching indicators for: {symbol}")
    try:
        resp = requests.get(f"http://localhost:8000/features/indicators", params={"symbol": symbol}, timeout=5)
        if resp.ok:
            data = resp.json()
            print(f"[WORKING] Got indicators: {data}")
            return html.Div([
                html.P(f"📊 Regime: {data.get('regime', 'N/A')}", className="mb-1"),
                html.P(f"📈 RSI: {data.get('rsi', 'N/A')}", className="mb-1"),
                html.P(f"🌊 MACD: {data.get('macd', 'N/A')}", className="mb-1"),
            ])
        else:
            return html.P("Indicators: API Error", className="text-danger")
    except Exception as e:
        print(f"[WORKING] Indicators error: {e}")
        return html.P("Indicators: Connection Error", className="text-danger")

@app.callback(
    Output('trade-result', 'children'),
    [Input('open-long-btn', 'n_clicks'), Input('open-short-btn', 'n_clicks')],
    State('selected-symbol-store', 'data'),
    prevent_initial_call=True
)
def handle_trade(long_clicks, short_clicks, symbol):
    ctx = callback_context
    if not ctx.triggered:
        return ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    direction = "LONG" if button_id == "open-long-btn" else "SHORT"
    symbol = symbol or "BTCUSDT"
    
    print(f"[WORKING] Trade button clicked: {direction} for {symbol}")
    
    try:
        trade_data = {
            "symbol": symbol,
            "direction": direction,
            "amount": 0.1,
            "entry_price": 0,
            "tp_pct": 2.0,
            "sl_pct": 1.0
        }
        
        resp = requests.post(f"http://localhost:8000/trade", json=trade_data, timeout=5)
        if resp.ok:
            result = resp.json()
            print(f"[WORKING] Trade success: {result}")
            return dbc.Alert(f"✅ {direction} trade opened for {symbol}!", color="success", dismissable=True)
        else:
            print(f"[WORKING] Trade failed: {resp.text}")
            return dbc.Alert(f"❌ Trade failed: {resp.status_code}", color="danger", dismissable=True)
    except Exception as e:
        print(f"[WORKING] Trade error: {e}")
        return dbc.Alert(f"❌ Error: {str(e)}", color="danger", dismissable=True)

if __name__ == "__main__":
    print("🚀 Starting WORKING dashboard on port 8052...")
    app.run(debug=True, port=8052)
