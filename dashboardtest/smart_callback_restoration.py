#!/usr/bin/env python3
"""
Smart Callback Restoration
Re-enables disabled callbacks by creating unique callback patterns
"""

import re
import os
import shutil

def find_active_callbacks():
    """Find callbacks that are still active"""
    
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all active @app.callback decorators
    active_callbacks = []
    callback_pattern = r'@app\.callback\s*\(\s*([^)]+)\)'
    
    matches = re.finditer(callback_pattern, content, re.DOTALL)
    for match in matches:
        callback_content = match.group(1)
        
        # Extract inputs
        inputs = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_content)
        outputs = re.findall(r'Output\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_content)
        
        active_callbacks.append({
            'inputs': inputs,
            'outputs': outputs,
            'full_content': callback_content
        })
    
    return active_callbacks

def restore_critical_callbacks():
    """Restore critical callbacks with unique combinations"""
    
    print("=== RESTORING CRITICAL CALLBACKS ===")
    
    # Create backup first
    backup_path = 'callbacks.py.restore_backup'
    shutil.copy2('callbacks.py', backup_path)
    print(f"Created backup: {backup_path}")
    
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find currently active callbacks
    active_callbacks = find_active_callbacks()
    
    # Find which buttons have active callbacks
    active_inputs = set()
    for callback in active_callbacks:
        active_inputs.update(callback['inputs'])
    
    print(f"Found {len(active_inputs)} active input IDs")
    
    # Critical buttons that need callbacks
    critical_buttons = [
        'sidebar-predict-btn',
        'sidebar-analytics-btn', 
        'test-ml-btn',
        'reset-balance-btn',
        'enable-online-learning-btn'
    ]
    
    missing_buttons = []
    for btn in critical_buttons:
        if btn not in active_inputs:
            missing_buttons.append(btn)
    
    print(f"Missing critical buttons: {missing_buttons}")
    
    # Create simple callbacks for missing buttons
    new_callbacks = []
    
    for btn_id in missing_buttons:
        if btn_id == 'sidebar-predict-btn':
            callback_code = '''
# Sidebar Predict Button
@app.callback(
    Output('sidebar-predict-output', 'children'),
    Input('sidebar-predict-btn', 'n_clicks'),
    State('sidebar-symbol', 'value'),
    prevent_initial_call=True
)
def sidebar_predict_action(n_clicks, symbol):
    """Handle sidebar predict button"""
    if not n_clicks:
        return ""
    
    try:
        symbol = symbol or "BTCUSDT"
        response = make_api_call("GET", f"/ml/predict?symbol={symbol.lower()}")
        
        if response and response.get('success'):
            prediction = response.get('prediction', 'No prediction')
            confidence = response.get('confidence', 0)
            return f"[PREDICT] {prediction} (Confidence: {confidence:.2%})"
        else:
            return f"[ERROR] {response.get('error', 'Prediction failed')}"
            
    except Exception as e:
        return f"[ERROR] {str(e)}"
'''
            new_callbacks.append(callback_code)
            
        elif btn_id == 'sidebar-analytics-btn':
            callback_code = '''
# Sidebar Analytics Button
@app.callback(
    Output('sidebar-analytics-output', 'children'),
    Input('sidebar-analytics-btn', 'n_clicks'),
    prevent_initial_call=True
)
def sidebar_analytics_action(n_clicks):
    """Handle sidebar analytics button"""
    if not n_clicks:
        return ""
    
    try:
        response = make_api_call("GET", "/model/analytics")
        
        if response and response.get('success'):
            analytics = response.get('analytics', {})
            return f"[ANALYTICS] Win Rate: {analytics.get('win_rate', 0):.1%}, Trades: {analytics.get('total_trades', 0)}"
        else:
            return f"[ERROR] {response.get('error', 'Analytics failed')}"
            
    except Exception as e:
        return f"[ERROR] {str(e)}"
'''
            new_callbacks.append(callback_code)
            
        elif btn_id == 'test-ml-btn':
            callback_code = '''
# Test ML Button
@app.callback(
    Output('test-ml-output', 'children'),
    Input('test-ml-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_ml_action(n_clicks):
    """Handle test ML button"""
    if not n_clicks:
        return ""
    
    try:
        response = make_api_call("GET", "/ml/compatibility/check")
        
        if response and response.get('success'):
            return "[OK] ML System Online"
        else:
            return f"[ERROR] {response.get('error', 'ML Test failed')}"
            
    except Exception as e:
        return f"[ERROR] {str(e)}"
'''
            new_callbacks.append(callback_code)
            
        elif btn_id == 'reset-balance-btn':
            callback_code = '''
# Reset Balance Button
@app.callback(
    Output('reset-balance-output', 'children'),
    Input('reset-balance-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_balance_action(n_clicks):
    """Handle reset balance button"""
    if not n_clicks:
        return ""
    
    try:
        response = make_api_call("POST", "/balance/reset", {})
        
        if response and response.get('success'):
            return "[OK] Balance Reset"
        else:
            return f"[ERROR] {response.get('error', 'Reset failed')}"
            
    except Exception as e:
        return f"[ERROR] {str(e)}"
'''
            new_callbacks.append(callback_code)
            
        elif btn_id == 'enable-online-learning-btn':
            callback_code = '''
# Enable Online Learning Button
@app.callback(
    Output('enable-online-learning-output', 'children'),
    Input('enable-online-learning-btn', 'n_clicks'),
    prevent_initial_call=True
)
def enable_online_learning_action(n_clicks):
    """Handle enable online learning button"""
    if not n_clicks:
        return ""
    
    try:
        response = make_api_call("POST", "/ml/online/enable", {})
        
        if response and response.get('success'):
            return "[OK] Online Learning Enabled"
        else:
            return f"[ERROR] {response.get('error', 'Enable failed')}"
            
    except Exception as e:
        return f"[ERROR] {str(e)}"
'''
            new_callbacks.append(callback_code)
    
    # Add new callbacks to file
    if new_callbacks:
        content += '\n\n# === RESTORED CRITICAL CALLBACKS ===\n'
        for callback in new_callbacks:
            content += callback + '\n'
        
        # Write back
        with open('callbacks.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Restored {len(new_callbacks)} critical callbacks")
    else:
        print("✅ All critical callbacks are already active")
    
    # Also need to ensure output divs exist in layout
    print("\n=== CHECKING LAYOUT FOR OUTPUT DIVS ===")
    
    output_divs_needed = [
        'sidebar-predict-output',
        'sidebar-analytics-output',
        'test-ml-output',
        'reset-balance-output',
        'enable-online-learning-output'
    ]
    
    if os.path.exists('layout.py'):
        with open('layout.py', 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        missing_outputs = []
        for div_id in output_divs_needed:
            if div_id not in layout_content:
                missing_outputs.append(div_id)
        
        if missing_outputs:
            print(f"Missing output divs: {missing_outputs}")
            
            # Add missing output divs to layout
            layout_backup = 'layout.py.restore_backup'
            shutil.copy2('layout.py', layout_backup)
            print(f"Created layout backup: {layout_backup}")
            
            # Add output divs at the end of layout
            additional_divs = '\n\n# === RESTORED OUTPUT DIVS ===\n'
            for div_id in missing_outputs:
                additional_divs += f'''
html.Div(id='{div_id}', style={{'display': 'none'}}),
'''
            
            layout_content += additional_divs
            
            with open('layout.py', 'w', encoding='utf-8') as f:
                f.write(layout_content)
            
            print(f"✅ Added {len(missing_outputs)} missing output divs")
        else:
            print("✅ All output divs exist in layout")
    
    print("\n=== RESTORATION COMPLETE ===")
    print("All critical button functionality restored!")

if __name__ == "__main__":
    restore_critical_callbacks()
