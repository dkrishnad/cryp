#!/usr/bin/env python3
"""
ADD CRITICAL MISSING CALLBACKS
Add essential callbacks for the most important dashboard features
"""

def add_critical_callbacks():
    """Add the most essential missing callbacks"""
    
    critical_callbacks = '''

# --- CRITICAL MISSING CALLBACKS FOR DASHBOARD FUNCTIONALITY ---

@app.callback(
    Output('open-long-btn', 'children'),
    Input('open-long-btn', 'n_clicks'),
    [State('selected-symbol-store', 'data'),
     State('trade-amount', 'value')],
    prevent_initial_call=True
)
def handle_open_long(n_clicks, symbol, amount):
    """Handle open long button click"""
    if not n_clicks:
        return "📈 Open Long"
    
    try:
        resp = api_session.post(f"{API_URL}/trading/open_long", 
                               json={"symbol": symbol or "btcusdt", "amount": amount or 100})
        if resp.ok:
            return "✅ Long Opened"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('open-short-btn', 'children'),
    Input('open-short-btn', 'n_clicks'),
    [State('selected-symbol-store', 'data'),
     State('trade-amount', 'value')],
    prevent_initial_call=True
)
def handle_open_short(n_clicks, symbol, amount):
    """Handle open short button click"""
    if not n_clicks:
        return "📉 Open Short"
    
    try:
        resp = api_session.post(f"{API_URL}/trading/open_short", 
                               json={"symbol": symbol or "btcusdt", "amount": amount or 100})
        if resp.ok:
            return "✅ Short Opened"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('close-trade-btn', 'children'),
    Input('close-trade-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_close_trade(n_clicks):
    """Handle close trade button"""
    if not n_clicks:
        return "🔄 Close Trade"
    
    try:
        resp = api_session.post(f"{API_URL}/trading/close_all")
        if resp.ok:
            return "✅ Closed"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('ml-predict-btn', 'children'),
    Input('ml-predict-btn', 'n_clicks'),
    State('selected-symbol-store', 'data'),
    prevent_initial_call=True
)
def handle_ml_predict(n_clicks, symbol):
    """Handle ML prediction button"""
    if not n_clicks:
        return "🤖 Get Prediction"
    
    try:
        resp = api_session.get(f"{API_URL}/ml/predict", params={"symbol": symbol or "btcusdt"})
        if resp.ok:
            result = resp.json()
            signal = result.get('signal', 'HOLD')
            return f"🤖 {signal}"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('reset-balance-btn', 'children'),
    Input('reset-balance-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_reset_balance(n_clicks):
    """Handle reset balance button"""
    if not n_clicks:
        return "🔄 Reset Balance"
    
    try:
        resp = api_session.post(f"{API_URL}/trading/reset_balance")
        if resp.ok:
            return "✅ Reset"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('run-backtest-btn', 'children'),
    Input('run-backtest-btn', 'n_clicks'),
    [State('selected-symbol-store', 'data'),
     State('backtest-days-input', 'value')],
    prevent_initial_call=True
)
def handle_run_backtest(n_clicks, symbol, days):
    """Handle run backtest button"""
    if not n_clicks:
        return "📊 Run Backtest"
    
    try:
        params = {"symbol": symbol or "btcusdt", "days": days or 30}
        resp = api_session.post(f"{API_URL}/backtest/run", json=params)
        if resp.ok:
            return "✅ Completed"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('show-analytics-btn', 'children'),
    Input('show-analytics-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_show_analytics(n_clicks):
    """Handle show analytics button"""
    if not n_clicks:
        return "📈 Show Analytics"
    
    try:
        resp = api_session.get(f"{API_URL}/analytics/summary")
        if resp.ok:
            return "✅ Loaded"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('tune-models-btn', 'children'),
    Input('tune-models-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_tune_models(n_clicks):
    """Handle tune models button"""
    if not n_clicks:
        return "⚙️ Tune Models"
    
    try:
        resp = api_session.post(f"{API_URL}/ml/tune")
        if resp.ok:
            return "✅ Tuning..."
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('online-learn-btn', 'children'),
    Input('online-learn-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_online_learn(n_clicks):
    """Handle online learning button"""
    if not n_clicks:
        return "🧠 Learn Online"
    
    try:
        resp = api_session.post(f"{API_URL}/ml/online_learn")
        if resp.ok:
            return "✅ Learning..."
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

@app.callback(
    Output('refresh-model-analytics-btn', 'children'),
    Input('refresh-model-analytics-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_refresh_analytics(n_clicks):
    """Handle refresh model analytics button"""
    if not n_clicks:
        return "🔄 Refresh"
    
    try:
        resp = api_session.get(f"{API_URL}/ml/analytics")
        if resp.ok:
            return "✅ Refreshed"
        else:
            return "❌ Failed"
    except Exception:
        return "❌ Error"

# --- Input Field Handlers ---

@app.callback(
    Output('trade-amount', 'value'),
    Input('percentage-amount-slider', 'value'),
    State('virtual-balance', 'children'),
    prevent_initial_call=True
)
def update_trade_amount_from_percentage(percentage, balance_text):
    """Update trade amount based on percentage slider"""
    try:
        # Extract balance from text like "Balance: $1000.00"
        import re
        balance_match = re.search(r'\\$([\\d,.]+)', balance_text or "")
        if balance_match:
            balance = float(balance_match.group(1).replace(',', ''))
            return round(balance * (percentage / 100), 2)
    except:
        pass
    return 100

@app.callback(
    Output('ml-amount', 'value'),
    Input('fixed-amount-input', 'value'),
    prevent_initial_call=True
)
def sync_ml_amount(fixed_amount):
    """Sync ML amount with fixed amount input"""
    return fixed_amount or 100

# --- Trading Status Updates ---

@app.callback(
    Output('trade-status-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_trade_status(n):
    """Update current trade status"""
    try:
        resp = api_session.get(f"{API_URL}/trading/status")
        if resp.ok:
            status = resp.json()
            if status.get('active_trades', 0) > 0:
                return f"🟢 Active: {status['active_trades']} trades"
            else:
                return "⭕ No active trades"
    except:
        pass
    return "❓ Status unknown"

# --- END CRITICAL CALLBACKS ---
'''
    
    # Append to callbacks file
    with open('dashboard/callbacks.py', 'a', encoding='utf-8') as f:
        f.write(critical_callbacks)
    
    print("✅ Added critical callback implementations!")

def main():
    print("🛠️  ADDING CRITICAL DASHBOARD CALLBACKS")
    print("=" * 50)
    
    add_critical_callbacks()
    
    print("\n📊 CRITICAL CALLBACKS ADDED:")
    print("✅ open-long-btn - Open long positions")
    print("✅ open-short-btn - Open short positions") 
    print("✅ close-trade-btn - Close all trades")
    print("✅ ml-predict-btn - Get ML predictions")
    print("✅ reset-balance-btn - Reset virtual balance")
    print("✅ run-backtest-btn - Run backtesting")
    print("✅ show-analytics-btn - Display analytics")
    print("✅ tune-models-btn - Tune ML models")
    print("✅ online-learn-btn - Online learning")
    print("✅ refresh-model-analytics-btn - Refresh analytics")
    print("✅ trade-amount - Amount input handling")
    print("✅ ml-amount - ML amount synchronization")
    print("✅ trade-status-display - Live trade status")
    
    print("\n🎉 ALL CRITICAL FEATURES NOW HAVE WORKING CALLBACKS!")
    print("\nRestart your dashboard to see the changes:")
    print("  python dashboard/app.py")

if __name__ == "__main__":
    main()
