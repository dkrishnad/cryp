#!/usr/bin/env python3
"""
DASHBOARD FEATURE ANALYZER
Find missing callbacks for buttons and features
"""

import re
import os

def analyze_button_callbacks():
    """Find all buttons and check if they have callbacks"""
    
    print("🔍 ANALYZING DASHBOARD BUTTONS AND FEATURES")
    print("=" * 60)
    
    # Read layout to find all buttons and interactive components
    with open('dashboard/layout.py', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Read callbacks to see what's implemented
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        callbacks_content = f.read()
    
    # Find all buttons and interactive components
    button_patterns = [
        r'html\.Button\([^,]*id=[\'"]([^\'\"]*)[\'"]',  # html.Button
        r'dbc\.Button\([^,]*id=[\'"]([^\'\"]*)[\'"]',   # dbc.Button
        r'dcc\.Dropdown\([^,]*id=[\'"]([^\'\"]*)[\'"]', # dcc.Dropdown
        r'dcc\.Input\([^,]*id=[\'"]([^\'\"]*)[\'"]',    # dcc.Input
        r'dcc\.Slider\([^,]*id=[\'"]([^\'\"]*)[\'"]',   # dcc.Slider
        r'dcc\.Checklist\([^,]*id=[\'"]([^\'\"]*)[\'"]', # dcc.Checklist
        r'dcc\.Upload\([^,]*id=[\'"]([^\'\"]*)[\'"]',   # dcc.Upload
    ]
    
    interactive_components = set()
    for pattern in button_patterns:
        matches = re.findall(pattern, layout_content)
        interactive_components.update(matches)
    
    print(f"📊 Found {len(interactive_components)} interactive components")
    
    # Check which components have callbacks
    missing_callbacks = []
    working_callbacks = []
    
    for component_id in sorted(interactive_components):
        # Check if component is used as Input in any callback
        input_pattern = f'Input.*[\'\"]{component_id}[\'"]'
        if re.search(input_pattern, callbacks_content):
            working_callbacks.append(component_id)
        else:
            missing_callbacks.append(component_id)
    
    print(f"\n✅ WORKING COMPONENTS ({len(working_callbacks)}):")
    for comp in working_callbacks[:10]:  # Show first 10
        print(f"  • {comp}")
    if len(working_callbacks) > 10:
        print(f"  ... and {len(working_callbacks) - 10} more")
    
    print(f"\n❌ MISSING CALLBACKS ({len(missing_callbacks)}):")
    for comp in missing_callbacks:
        print(f"  • {comp}")
    
    return missing_callbacks, working_callbacks

def check_critical_features():
    """Check critical trading features that must work"""
    
    print("\n" + "=" * 60)
    print("🎯 CRITICAL FEATURES ANALYSIS")
    print("=" * 60)
    
    critical_features = [
        # Trading Controls
        'open-long-btn',
        'open-short-btn', 
        'close-trade-btn',
        'execute-signal-btn',
        
        # Auto Trading
        'auto-trading-toggle',
        'auto-trading-start-btn',
        'auto-trading-stop-btn',
        
        # Settings
        'save-settings-btn',
        'save-auto-settings-btn',
        'reset-balance-btn',
        
        # Analytics
        'run-backtest-btn',
        'refresh-model-analytics-btn',
        'show-analytics-btn',
        
        # ML Features
        'ml-predict-btn',
        'tune-models-btn',
        'online-learn-btn',
    ]
    
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        callbacks_content = f.read()
    
    working_critical = []
    missing_critical = []
    
    for feature in critical_features:
        input_pattern = f'Input.*[\'\"]{feature}[\'"]'
        if re.search(input_pattern, callbacks_content):
            working_critical.append(feature)
        else:
            missing_critical.append(feature)
    
    print(f"✅ WORKING CRITICAL FEATURES ({len(working_critical)}):")
    for feature in working_critical:
        print(f"  • {feature}")
    
    print(f"\n❌ MISSING CRITICAL FEATURES ({len(missing_critical)}):")
    for feature in missing_critical:
        print(f"  • {feature}")
    
    return missing_critical

def generate_missing_callbacks(missing_features):
    """Generate callback code for missing features"""
    
    print("\n" + "=" * 60)
    print("🛠️  GENERATING MISSING CALLBACK IMPLEMENTATIONS")
    print("=" * 60)
    
    callback_templates = {
        'open-long-btn': '''
@app.callback(
    [Output('trade-status-display', 'children'),
     Output('open-long-btn', 'disabled')],
    Input('open-long-btn', 'n_clicks'),
    [State('selected-symbol-store', 'data'),
     State('trade-amount-input', 'value')],
    prevent_initial_call=True
)
def open_long_position(n_clicks, symbol, amount):
    """Open long position"""
    if not n_clicks:
        return dash.no_update, False
    
    try:
        resp = api_session.post(f"{API_URL}/trading/open_long", 
                               json={"symbol": symbol, "amount": amount})
        if resp.ok:
            return "✅ Long position opened", False
        else:
            return "❌ Failed to open long", False
    except Exception as e:
        return f"❌ Error: {str(e)}", False''',

        'open-short-btn': '''
@app.callback(
    [Output('trade-status-display', 'children'),
     Output('open-short-btn', 'disabled')],
    Input('open-short-btn', 'n_clicks'),
    [State('selected-symbol-store', 'data'),
     State('trade-amount-input', 'value')],
    prevent_initial_call=True
)
def open_short_position(n_clicks, symbol, amount):
    """Open short position"""
    if not n_clicks:
        return dash.no_update, False
    
    try:
        resp = api_session.post(f"{API_URL}/trading/open_short", 
                               json={"symbol": symbol, "amount": amount})
        if resp.ok:
            return "✅ Short position opened", False
        else:
            return "❌ Failed to open short", False
    except Exception as e:
        return f"❌ Error: {str(e)}", False''',

        'execute-signal-btn': '''
@app.callback(
    Output('signal-execution-output', 'children'),
    Input('execute-signal-btn', 'n_clicks'),
    prevent_initial_call=True
)
def execute_current_signal(n_clicks):
    """Execute current ML signal"""
    if not n_clicks:
        return dash.no_update
    
    try:
        resp = api_session.post(f"{API_URL}/trading/execute_signal")
        if resp.ok:
            result = resp.json()
            return f"✅ Signal executed: {result.get('action', 'Unknown')}"
        else:
            return "❌ Failed to execute signal"
    except Exception as e:
        return f"❌ Error: {str(e)}"''',

        'run-backtest-btn': '''
@app.callback(
    [Output('backtest-result', 'children'),
     Output('run-backtest-btn', 'disabled')],
    Input('run-backtest-btn', 'n_clicks'),
    [State('backtest-days-input', 'value'),
     State('selected-symbol-store', 'data')],
    prevent_initial_call=True
)
def run_backtest(n_clicks, days, symbol):
    """Run backtesting"""
    if not n_clicks:
        return dash.no_update, False
    
    try:
        resp = api_session.post(f"{API_URL}/backtest/run", 
                               json={"symbol": symbol, "days": days or 30})
        if resp.ok:
            result = resp.json()
            profit = result.get('total_profit', 0)
            trades = result.get('total_trades', 0)
            return f"✅ Backtest: ${profit:.2f} profit, {trades} trades", False
        else:
            return "❌ Backtest failed", False
    except Exception as e:
        return f"❌ Error: {str(e)}", False''',

        'ml-predict-btn': '''
@app.callback(
    [Output('ml-prediction-output', 'children'),
     Output('ml-predict-btn', 'disabled')],
    Input('ml-predict-btn', 'n_clicks'),
    State('selected-symbol-store', 'data'),
    prevent_initial_call=True
)
def get_ml_prediction(n_clicks, symbol):
    """Get ML prediction for symbol"""
    if not n_clicks:
        return dash.no_update, False
    
    try:
        resp = api_session.get(f"{API_URL}/ml/predict", params={"symbol": symbol})
        if resp.ok:
            result = resp.json()
            signal = result.get('signal', 'HOLD')
            confidence = result.get('confidence', 0) * 100
            return f"🤖 Prediction: {signal} ({confidence:.1f}% confidence)", False
        else:
            return "❌ Prediction failed", False
    except Exception as e:
        return f"❌ Error: {str(e)}", False''',

        'reset-balance-btn': '''
@app.callback(
    [Output('virtual-balance', 'children'),
     Output('reset-balance-btn', 'disabled')],
    Input('reset-balance-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_virtual_balance(n_clicks):
    """Reset virtual balance to default"""
    if not n_clicks:
        return dash.no_update, False
    
    try:
        resp = api_session.post(f"{API_URL}/trading/reset_balance")
        if resp.ok:
            result = resp.json()
            balance = result.get('balance', 1000)
            return f"Balance: ${balance:.2f}", False
        else:
            return dash.no_update, False
    except Exception as e:
        return dash.no_update, False''',

        'auto-trading-toggle': '''
@app.callback(
    Output('auto-trading-status', 'children'),
    Input('auto-trading-toggle', 'value'),
    prevent_initial_call=True
)
def toggle_auto_trading(enabled):
    """Toggle auto trading on/off"""
    try:
        action = "start" if enabled else "stop"
        resp = api_session.post(f"{API_URL}/auto_trading/{action}")
        if resp.ok:
            status = "ENABLED" if enabled else "DISABLED"
            color = "green" if enabled else "red"
            return html.Span(f"Auto Trading: {status}", style={"color": color})
        else:
            return "❌ Failed to toggle auto trading"
    except Exception as e:
        return f"❌ Error: {str(e)}"''',
    }
    
    # Write missing callbacks to a file
    missing_code = ""
    for feature in missing_features:
        if feature in callback_templates:
            missing_code += callback_templates[feature] + "\n\n"
    
    if missing_code:
        with open('missing_callbacks_to_add.py', 'w', encoding='utf-8') as f:
            f.write("# MISSING CALLBACK IMPLEMENTATIONS\n")
            f.write("# Add these to dashboard/callbacks.py\n\n")
            f.write(missing_code)
        
        print(f"✅ Generated {len([f for f in missing_features if f in callback_templates])} callback implementations")
        print("📄 Saved to: missing_callbacks_to_add.py")
    
    return missing_code

def main():
    print("🔍 DASHBOARD FEATURE ANALYSIS")
    print("=" * 60)
    
    # Analyze all components
    missing_callbacks, working_callbacks = analyze_button_callbacks()
    
    # Check critical features
    missing_critical = check_critical_features()
    
    # Generate missing callback code
    if missing_critical:
        generate_missing_callbacks(missing_critical)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    
    total_components = len(missing_callbacks) + len(working_callbacks)
    working_percentage = (len(working_callbacks) / total_components * 100) if total_components > 0 else 0
    
    print(f"📈 Overall Status: {working_percentage:.1f}% of features working")
    print(f"✅ Working: {len(working_callbacks)} components")
    print(f"❌ Missing: {len(missing_callbacks)} components")
    print(f"🎯 Critical Missing: {len(missing_critical)} features")
    
    if missing_critical:
        print(f"\n⚠️  PRIORITY: Fix {len(missing_critical)} critical features first!")
        print("🛠️  Use missing_callbacks_to_add.py to implement them")
    else:
        print("\n🎉 All critical features have callbacks!")

if __name__ == "__main__":
    main()
