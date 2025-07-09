# Create a simplified callbacks.py for debugging
print('>>> SIMPLIFIED callbacks.py imported and executing')
import dash
from dash.dependencies import Input, Output, State
from dash import ctx, callback_context
from app import app
import requests

API_URL = "http://localhost:8000"

# --- MOST BASIC TEST ---
@app.callback(
    Output('test-output', 'children'),
    Input('interval-prediction', 'n_intervals'),
    prevent_initial_call=False
)
def test_callback(n):
    print(f"[DASH SIMPLE TEST] test_callback triggered, n={n}")
    return f"✅ Working! Test: {n}"

# --- SYMBOL SELECTION ---
@app.callback(
    Output('selected-symbol-store', 'data'),
    Input('sidebar-symbol', 'value'),
    prevent_initial_call=False
)
def update_selected_symbol(symbol):
    print(f"[DASH SIMPLE] Symbol selected: {symbol}")
    return (symbol or 'BTCUSDT').upper()

# --- LIVE PRICE ---
@app.callback(
    Output('live-price', 'children'),
    Input('selected-symbol-store', 'data'),
    prevent_initial_call=False
)
def update_live_price(selected_symbol):
    symbol = selected_symbol or 'BTCUSDT'
    print(f"[DASH SIMPLE] Fetching price for: {symbol}")
    try:
        resp = requests.get(f"{API_URL}/price", params={"symbol": symbol})
        if resp.ok:
            data = resp.json()
            price = data.get("price", 0)
            print(f"[DASH SIMPLE] Got price: {price}")
            return f"{symbol}: ${price:,.2f}"
        else:
            print(f"[DASH SIMPLE] Price API failed: {resp.status_code}")
            return f"{symbol}: API Error"
    except Exception as e:
        print(f"[DASH SIMPLE] Price error: {e}")
        return f"{symbol}: Error"

# --- SIMPLE TRADE BUTTON ---
@app.callback(
    Output('trade-action-result', 'children'),
    Input('open-long-btn', 'n_clicks'),
    State('selected-symbol-store', 'data'),
    prevent_initial_call=True
)
def handle_trade_button(n_clicks, selected_symbol):
    print(f"[DASH SIMPLE] Trade button clicked: {n_clicks}, symbol: {selected_symbol}")
    if n_clicks:
        symbol = selected_symbol or 'BTCUSDT'
        try:
            trade_data = {
                "symbol": symbol,
                "direction": "LONG",
                "amount": 0.1,
                "entry_price": 0,
                "tp_pct": 2.0,
                "sl_pct": 1.0
            }
            resp = requests.post(f"{API_URL}/trade", json=trade_data)
            if resp.ok:
                result = resp.json()
                print(f"[DASH SIMPLE] Trade success: {result}")
                return f"✅ LONG trade opened for {symbol}"
            else:
                print(f"[DASH SIMPLE] Trade failed: {resp.text}")
                return f"❌ Trade failed: {resp.status_code}"
        except Exception as e:
            print(f"[DASH SIMPLE] Trade error: {e}")
            return f"❌ Error: {str(e)}"
    return "Click to trade"

print('[DASH SIMPLE] Simplified callbacks loaded successfully')
