#!/usr/bin/env python3
"""
Simple test to isolate the callback error
"""
from dash_app import app
from layout import layout
from dash import Input, Output, callback
import requests

# Set layout
app.layout = layout

# Simple test callback without backend calls
@app.callback(
    Output("test-output", "children", allow_duplicate=True),
    Input("interval-indicators", "n_intervals"),
    prevent_initial_call=True
)
def simple_test_callback(n_intervals):
    try:
        print(f"[SIMPLE TEST] Callback triggered: {n_intervals}")
        return f"Simple test working: {n_intervals}"
    except Exception as e:
        print(f"[SIMPLE TEST] Error: {e}")
        return f"Error: {str(e)}"

# Test backend connection callback
@app.callback(
    Output("test-output", "children", allow_duplicate=True),
    Input("sidebar-symbol", "value"),
    prevent_initial_call=True
)
def test_backend_connection(symbol):
    try:
        print(f"[BACKEND TEST] Testing symbol: {symbol}")
        # Test with a simple timeout
        resp = requests.get("http://localhost:8000/health", timeout=5)
        print(f"[BACKEND TEST] Health check: {resp.status_code}")
        
        if resp.status_code == 200:
            # Now test indicators
            resp2 = requests.get(f"http://localhost:8000/features/indicators", 
                               params={"symbol": symbol or "btcusdt"}, timeout=5)
            print(f"[BACKEND TEST] Indicators: {resp2.status_code}")
            if resp2.status_code == 200:
                data = resp2.json()
                return f"Backend working! Symbol: {symbol}, RSI: {data.get('rsi', 'N/A')}"
            else:
                return f"Backend indicators failed: {resp2.status_code}"
        else:
            return f"Backend health failed: {resp.status_code}"
            
    except requests.exceptions.Timeout:
        print("[BACKEND TEST] Request timeout")
        return "Backend timeout error"
    except Exception as e:
        print(f"[BACKEND TEST] Exception: {e}")
        return f"Backend error: {str(e)}"

if __name__ == "__main__":
    print("Starting simple test dashboard...")
    print("This will test callbacks step by step to isolate the issue")
    app.run(debug=True, port=8051, host="0.0.0.0")  # Use different port
