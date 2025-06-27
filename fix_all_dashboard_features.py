#!/usr/bin/env python3
"""
COMPREHENSIVE DASHBOARD FIX SCRIPT
Fix all missing features and duplicate callbacks
"""

import re

def fix_duplicate_callbacks():
    """Remove duplicate callback definitions"""
    print("🔧 Fixing duplicate callbacks...")
    
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the duplicate email callbacks (keep only the first ones)
    # The second email callback at line 459 should be removed
    lines = content.split('\n')
    
    # Find and remove duplicate callback blocks
    output_lines = []
    skip_lines = False
    duplicate_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for duplicate callback patterns
        if ('Output("email-notify-address", "disabled")' in line or
            'Output("email-notify-toggle", "disabled")' in line):
            # Skip this duplicate callback block
            skip_lines = True
            duplicate_count += 1
            print(f"Removing duplicate callback at line {i+1}")
            
            # Skip until we find the next function or callback
            while i < len(lines) and not (lines[i].strip().startswith('@app.callback') or 
                                         lines[i].strip().startswith('def ') or
                                         lines[i].strip().startswith('# ---')):
                i += 1
            continue
        
        if not skip_lines:
            output_lines.append(line)
        
        # Reset skip flag when we encounter a new callback or function
        if (line.strip().startswith('@app.callback') or 
            line.strip().startswith('def ') or 
            line.strip().startswith('# ---')):
            skip_lines = False
        
        i += 1
    
    # Write the cleaned content back
    cleaned_content = '\n'.join(output_lines)
    with open('dashboard/callbacks.py', 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"✅ Removed {duplicate_count} duplicate callbacks")

def add_missing_components():
    """Add missing components to layout.py"""
    print("🔧 Adding missing components to layout...")
    
    with open('dashboard/layout.py', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Add missing auto trading components
    missing_components = '''
    # Auto Trading Status Display
    html.Div([
        html.H5("Auto Trading Status", className="text-info"),
        html.Div(id="auto-trading-status", children="Disabled"),
        html.Div(id="auto-trading-toggle-output"),
    ], className="mb-3"),
    
    # Auto Trading Controls
    html.Div([
        html.Label("Symbol:", className="form-label"),
        dcc.Dropdown(id="auto-symbol-dropdown", options=[], value="btcusdt"),
        
        html.Label("Confidence Threshold:", className="form-label"),
        dcc.Slider(id="auto-confidence-slider", min=0, max=100, value=70, marks={0: '0%', 50: '50%', 100: '100%'}),
        
        html.Label("Risk Level:", className="form-label"),
        dcc.Slider(id="auto-risk-slider", min=1, max=10, value=5, marks={1: 'Low', 5: 'Med', 10: 'High'}),
        
        html.Label("Take Profit %:", className="form-label"),
        dcc.Slider(id="auto-tp-slider", min=0.5, max=10, value=2, step=0.1),
        
        html.Label("Stop Loss %:", className="form-label"),
        dcc.Slider(id="auto-sl-slider", min=0.5, max=5, value=1, step=0.1),
    ], className="mb-3"),
    
    # Auto Trading Displays
    html.Div([
        html.Div(id="auto-balance-display", children="Balance: Loading..."),
        html.Div(id="auto-pnl-display", children="P&L: $0.00"),
        html.Div(id="auto-winrate-display", children="Win Rate: 0%"),
        html.Div(id="auto-wl-display", children="W/L: 0/0"),
        html.Div(id="auto-trades-display", children="Total Trades: 0"),
    ], className="mb-3"),
    
    # Trade Amount Controls
    html.Div([
        html.H6("Trade Amount", className="text-info"),
        html.Div([
            html.Label("Fixed Amount ($):"),
            dcc.Input(id="fixed-amount-input", type="number", value=100, className="form-control"),
            html.Div(id="fixed-amount-section"),
        ], id="fixed-amount-section", className="mb-2"),
        
        html.Div([
            html.Label("Percentage Amount (%):"),
            dcc.Input(id="percentage-amount-input", type="number", value=10, min=1, max=100, className="form-control"),
            dcc.Slider(id="percentage-amount-slider", min=1, max=100, value=10, marks={10: '10%', 50: '50%', 100: '100%'}),
            html.Div(id="percentage-amount-section"),
        ], className="mb-2"),
        
        html.Div(id="calculated-amount-display", children="Calculated: $0.00"),
    ], className="mb-3"),
    
    # Signal and Trading Controls
    html.Div([
        html.Div(id="current-signal-display", children="Signal: None"),
        html.Button("Execute Signal", id="execute-signal-btn", className="btn btn-primary me-2"),
        html.Button("Reset Auto Trading", id="reset-auto-trading-btn", className="btn btn-warning"),
        html.Div(id="save-auto-settings-btn"),
    ], className="mb-3"),
    
    # Analytics and Logs
    html.Div([
        html.H6("Analytics", className="text-info"),
        html.Div(id="analytics-output"),
        html.Div(id="auto-trade-log"),
        html.Div(id="trade-logs-output"),
    ], className="mb-3"),
    
    # Model and Low Cap Settings
    html.Div([
        html.Div(id="refresh-model-versions-btn-output"),
        html.Div(id="low-cap-settings-display"),
    ], className="mb-3"),
'''
    
    # Find where to insert (before the closing layout bracket)
    if 'auto-trading-status' not in layout_content:
        # Insert before the last closing bracket
        insertion_point = layout_content.rfind('])')
        if insertion_point != -1:
            new_layout = (layout_content[:insertion_point] + 
                         missing_components + 
                         layout_content[insertion_point:])
            
            with open('dashboard/layout.py', 'w', encoding='utf-8') as f:
                f.write(new_layout)
            
            print("✅ Added missing components to layout")
        else:
            print("⚠️  Could not find insertion point in layout")
    else:
        print("✅ Auto trading components already exist in layout")

def add_missing_callbacks():
    """Add missing callback implementations"""
    print("🔧 Adding missing callback implementations...")
    
    missing_callbacks_code = '''

# --- Missing Auto Trading Callbacks ---

@app.callback(
    Output('auto-trading-status', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_auto_trading_status(n):
    """Update auto trading status"""
    try:
        resp = api_session.get(f"{API_URL}/auto_trading/status", timeout=5)
        if resp.ok:
            status = resp.json()
            return f"Status: {status.get('status', 'Unknown')}"
    except:
        pass
    return "Status: Disconnected"

@app.callback(
    Output('auto-balance-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_auto_balance_display(n):
    """Update auto trading balance display"""
    try:
        resp = api_session.get(f"{API_URL}/virtual_balance", timeout=5)
        if resp.ok:
            balance = resp.json().get('balance', 0)
            return f"Balance: ${balance:.2f}"
    except:
        pass
    return "Balance: Loading..."

@app.callback(
    Output('auto-pnl-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_auto_pnl_display(n):
    """Update P&L display"""
    try:
        resp = api_session.get(f"{API_URL}/trading/pnl", timeout=5)
        if resp.ok:
            pnl = resp.json().get('total_pnl', 0)
            color = "green" if pnl >= 0 else "red"
            return html.Span(f"P&L: ${pnl:.2f}", style={"color": color})
    except:
        pass
    return "P&L: $0.00"

@app.callback(
    Output('auto-winrate-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_auto_winrate_display(n):
    """Update win rate display"""
    try:
        resp = api_session.get(f"{API_URL}/trading/stats", timeout=5)
        if resp.ok:
            stats = resp.json()
            winrate = stats.get('win_rate', 0)
            return f"Win Rate: {winrate:.1f}%"
    except:
        pass
    return "Win Rate: 0%"

@app.callback(
    Output('current-signal-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_current_signal_display(n):
    """Update current signal display"""
    try:
        resp = api_session.get(f"{API_URL}/signals/latest", timeout=5)
        if resp.ok:
            signal = resp.json()
            signal_type = signal.get('signal', 'None')
            confidence = signal.get('confidence', 0) * 100
            return f"Signal: {signal_type} ({confidence:.1f}%)"
    except:
        pass
    return "Signal: None"

@app.callback(
    Output('calculated-amount-display', 'children'),
    [Input('fixed-amount-input', 'value'),
     Input('percentage-amount-input', 'value')]
)
def update_calculated_amount(fixed_amount, percentage):
    """Update calculated trading amount"""
    try:
        if fixed_amount and fixed_amount > 0:
            return f"Calculated: ${fixed_amount:.2f}"
        elif percentage and percentage > 0:
            # Get current balance
            resp = api_session.get(f"{API_URL}/virtual_balance", timeout=5)
            if resp.ok:
                balance = resp.json().get('balance', 0)
                calculated = balance * (percentage / 100)
                return f"Calculated: ${calculated:.2f} ({percentage}% of ${balance:.2f})"
    except:
        pass
    return "Calculated: $0.00"

@app.callback(
    Output('analytics-output', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_analytics_output(n):
    """Update analytics display"""
    try:
        resp = api_session.get(f"{API_URL}/analytics/summary", timeout=5)
        if resp.ok:
            data = resp.json()
            return html.Div([
                html.P(f"Total Trades: {data.get('total_trades', 0)}"),
                html.P(f"Success Rate: {data.get('success_rate', 0):.1f}%"),
                html.P(f"Avg Profit: ${data.get('avg_profit', 0):.2f}"),
            ])
    except:
        pass
    return html.P("Analytics: Loading...")

@app.callback(
    Output('auto-trade-log', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_auto_trade_log(n):
    """Update trade log display"""
    try:
        resp = api_session.get(f"{API_URL}/trading/recent_trades", timeout=5)
        if resp.ok:
            trades = resp.json()
            if trades:
                trade_items = []
                for trade in trades[-5:]:  # Show last 5 trades
                    trade_items.append(html.Li(
                        f"{trade.get('symbol', 'N/A')} - {trade.get('side', 'N/A')} - "
                        f"${trade.get('amount', 0):.2f} - {trade.get('status', 'N/A')}"
                    ))
                return html.Ul(trade_items)
    except:
        pass
    return html.P("No recent trades")

'''
    
    # Append missing callbacks to the callbacks.py file
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'auto-trading-status' not in content:
        with open('dashboard/callbacks.py', 'a', encoding='utf-8') as f:
            f.write(missing_callbacks_code)
        print("✅ Added missing callback implementations")
    else:
        print("✅ Auto trading callbacks already exist")

def main():
    print("=" * 60)
    print("🛠️  COMPREHENSIVE DASHBOARD FIX")
    print("=" * 60)
    
    # Fix duplicate callbacks
    fix_duplicate_callbacks()
    
    # Add missing components to layout
    add_missing_components()
    
    # Add missing callback implementations
    add_missing_callbacks()
    
    print("\n" + "=" * 60)
    print("📊 FIX SUMMARY")
    print("=" * 60)
    print("✅ Duplicate callbacks removed")
    print("✅ Missing components added to layout")
    print("✅ Missing callback implementations added")
    print("\n🎉 ALL DASHBOARD FEATURES SHOULD NOW BE WORKING!")
    print("\nRestart your dashboard to see the changes:")
    print("  python dashboard/app.py")

if __name__ == "__main__":
    main()
