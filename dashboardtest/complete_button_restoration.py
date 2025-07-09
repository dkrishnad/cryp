#!/usr/bin/env python3
"""
Complete Button Functionality Restoration
Creates callbacks for all orphaned buttons to restore full functionality
"""

import re
import os
import json

# Define button groups and their API endpoints
BUTTON_MAPPING = {
    # Sidebar amount buttons
    'sidebar-amount-50': {'endpoint': '/balance/set', 'data': {'amount': 50}},
    'sidebar-amount-100': {'endpoint': '/balance/set', 'data': {'amount': 100}},
    'sidebar-amount-250': {'endpoint': '/balance/set', 'data': {'amount': 250}},
    'sidebar-amount-500': {'endpoint': '/balance/set', 'data': {'amount': 500}},
    'sidebar-amount-1000': {'endpoint': '/balance/set', 'data': {'amount': 1000}},
    'sidebar-amount-max': {'endpoint': '/balance/set', 'data': {'amount': 'max'}},
    'sidebar-amount-50-btn': {'endpoint': '/balance/set', 'data': {'amount': 50}},
    'sidebar-amount-100-btn': {'endpoint': '/balance/set', 'data': {'amount': 100}},
    'sidebar-amount-250-btn': {'endpoint': '/balance/set', 'data': {'amount': 250}},
    'sidebar-amount-500-btn': {'endpoint': '/balance/set', 'data': {'amount': 500}},
    'sidebar-amount-1000-btn': {'endpoint': '/balance/set', 'data': {'amount': 1000}},
    'sidebar-amount-max-btn': {'endpoint': '/balance/set', 'data': {'amount': 'max'}},
    
    # Amount buttons
    'amount-50-btn': {'endpoint': '/balance/set', 'data': {'amount': 50}},
    'amount-100-btn': {'endpoint': '/balance/set', 'data': {'amount': 100}},
    'amount-250-btn': {'endpoint': '/balance/set', 'data': {'amount': 250}},
    'amount-500-btn': {'endpoint': '/balance/set', 'data': {'amount': 500}},
    'amount-1000-btn': {'endpoint': '/balance/set', 'data': {'amount': 1000}},
    'amount-max-btn': {'endpoint': '/balance/set', 'data': {'amount': 'max'}},
    
    # Core functionality buttons
    'sidebar-predict-btn': {'endpoint': '/ml/predict', 'data': {'symbol': 'BTCUSDT'}},
    'sidebar-analytics-btn': {'endpoint': '/model/analytics', 'data': {}},
    'reset-balance-btn': {'endpoint': '/balance/reset', 'data': {}},
    'test-ml-btn': {'endpoint': '/ml/test', 'data': {}},
    'get-prediction-btn': {'endpoint': '/ml/predict', 'data': {'symbol': 'BTCUSDT'}},
    'quick-prediction-btn': {'endpoint': '/ml/predict', 'data': {'symbol': 'BTCUSDT', 'quick': True}},
    
    # Trading buttons
    'buy-btn': {'endpoint': '/trading/buy', 'data': {'symbol': 'BTCUSDT'}},
    'sell-btn': {'endpoint': '/trading/sell', 'data': {'symbol': 'BTCUSDT'}},
    'trade-execute-btn': {'endpoint': '/trading/execute', 'data': {}},
    'trades-list-btn': {'endpoint': '/trades', 'data': {}},
    
    # Auto trading buttons
    'auto-trading-toggle-btn': {'endpoint': '/auto_trading/toggle', 'data': {}},
    'auto-trading-settings-btn': {'endpoint': '/auto_trading/settings', 'data': {}},
    'auto-trading-signals-btn': {'endpoint': '/auto_trading/signals', 'data': {}},
    'auto-trading-status-refresh-btn': {'endpoint': '/auto_trading/status', 'data': {}},
    'start-advanced-auto-trading-btn': {'endpoint': '/auto_trading/start', 'data': {'mode': 'advanced'}},
    'stop-advanced-auto-trading-btn': {'endpoint': '/auto_trading/stop', 'data': {}},
    'check-advanced-auto-trading-btn': {'endpoint': '/auto_trading/status', 'data': {'mode': 'advanced'}},
    
    # Futures trading buttons
    'futures-execute-signal-btn': {'endpoint': '/futures/execute', 'data': {}},
    'futures-history-btn': {'endpoint': '/futures/history', 'data': {}},
    'futures-open-btn': {'endpoint': '/futures/open', 'data': {}},
    'binance-auto-execute-btn': {'endpoint': '/binance/auto_execute', 'data': {}},
    
    # Chart buttons
    'show-price-chart-btn': {'endpoint': '/charts/price', 'data': {}},
    'show-indicators-chart-btn': {'endpoint': '/charts/indicators', 'data': {}},
    'refresh-charts-btn': {'endpoint': '/charts/refresh', 'data': {}},
    'chart-refresh-btn': {'endpoint': '/charts/refresh', 'data': {}},
    'chart-bollinger-btn': {'endpoint': '/charts/bollinger', 'data': {}},
    'chart-momentum-btn': {'endpoint': '/charts/momentum', 'data': {}},
    'chart-volume-btn': {'endpoint': '/charts/volume', 'data': {}},
    'chart-show-indicators-btn': {'endpoint': '/charts/indicators', 'data': {}},
    'chart-show-price-btn': {'endpoint': '/charts/price', 'data': {}},
    'show-bollinger-btn': {'endpoint': '/charts/bollinger', 'data': {}},
    'show-momentum-btn': {'endpoint': '/charts/momentum', 'data': {}},
    'show-volume-btn': {'endpoint': '/charts/volume', 'data': {}},
    
    # Sidebar ML buttons
    'sidebar-ml-predict-btn': {'endpoint': '/ml/predict', 'data': {'symbol': 'BTCUSDT'}},
    'sidebar-ml-status-btn': {'endpoint': '/ml/status', 'data': {}},
    'sidebar-feature-importance-btn': {'endpoint': '/ml/feature_importance', 'data': {}},
    'sidebar-volume-chart-btn': {'endpoint': '/charts/volume', 'data': {}},
    'sidebar-momentum-chart-btn': {'endpoint': '/charts/momentum', 'data': {}},
    'sidebar-bollinger-btn': {'endpoint': '/charts/bollinger', 'data': {}},
    
    # Toggle buttons
    'toggle-hft-tools': {'endpoint': '/ui/toggle', 'data': {'section': 'hft-tools'}},
    'toggle-data-collection': {'endpoint': '/ui/toggle', 'data': {'section': 'data-collection'}},
    'toggle-online-learning': {'endpoint': '/ui/toggle', 'data': {'section': 'online-learning'}},
    'toggle-risk-management': {'endpoint': '/ui/toggle', 'data': {'section': 'risk-management'}},
    'toggle-notifications': {'endpoint': '/ui/toggle', 'data': {'section': 'notifications'}},
    'toggle-email-alerts': {'endpoint': '/ui/toggle', 'data': {'section': 'email-alerts'}},
    'toggle-analytics': {'endpoint': '/ui/toggle', 'data': {'section': 'analytics'}},
    'toggle-ml-tools': {'endpoint': '/ui/toggle', 'data': {'section': 'ml-tools'}},
    'toggle-charts': {'endpoint': '/ui/toggle', 'data': {'section': 'charts'}},
    'toggle-dev-tools': {'endpoint': '/ui/toggle', 'data': {'section': 'dev-tools'}},
    
    # HFT buttons
    'start-hft-analysis-btn': {'endpoint': '/hft/start', 'data': {}},
    'stop-hft-analysis-btn': {'endpoint': '/hft/stop', 'data': {}},
    'hft-analytics-btn': {'endpoint': '/hft/analytics', 'data': {}},
    'hft-config-btn': {'endpoint': '/hft/config', 'data': {}},
    'hft-opportunities-btn': {'endpoint': '/hft/opportunities', 'data': {}},
    'hft-start-btn': {'endpoint': '/hft/start', 'data': {}},
    'hft-stop-btn': {'endpoint': '/hft/stop', 'data': {}},
    'hft-status-btn': {'endpoint': '/hft/status', 'data': {}},
    'hft-analytics-refresh-btn': {'endpoint': '/hft/analytics', 'data': {}},
    
    # Data collection buttons
    'start-data-collection-btn-duplicate': {'endpoint': '/data/start', 'data': {}},
    'stop-data-collection-btn-duplicate': {'endpoint': '/data/stop', 'data': {}},
    
    # Online learning buttons
    'enable-online-learning-btn': {'endpoint': '/ml/online/enable', 'data': {}},
    'disable-online-learning-btn': {'endpoint': '/ml/online/disable', 'data': {}},
    'optimize-learning-rates-btn': {'endpoint': '/ml/online/optimize', 'data': {}},
    'reset-learning-rates-btn': {'endpoint': '/ml/online/reset', 'data': {}},
    'ml-online-config-btn': {'endpoint': '/ml/online/config', 'data': {}},
    'ml-online-performance-btn': {'endpoint': '/ml/online/performance', 'data': {}},
    
    # Risk management buttons
    'calculate-position-size-btn': {'endpoint': '/risk/position_size', 'data': {}},
    'check-trade-risk-btn': {'endpoint': '/risk/check', 'data': {}},
    'update-risk-settings-btn': {'endpoint': '/risk/settings', 'data': {}},
    'risk-position-size-btn': {'endpoint': '/risk/position_size', 'data': {}},
    'risk-trade-check-btn': {'endpoint': '/risk/check', 'data': {}},
    'risk-portfolio-metrics-btn': {'endpoint': '/risk/portfolio', 'data': {}},
    'risk-stop-loss-btn': {'endpoint': '/risk/stop_loss', 'data': {}},
    
    # Notification buttons
    'refresh-notifications-btn': {'endpoint': '/notifications/refresh', 'data': {}},
    'clear-notifications-btn': {'endpoint': '/notifications/clear', 'data': {}},
    'notifications-clear-btn': {'endpoint': '/notifications/clear', 'data': {}},
    'notifications-mark-read-btn': {'endpoint': '/notifications/mark_read', 'data': {}},
    'clear-all-notifications-btn': {'endpoint': '/notifications/clear_all', 'data': {}},
    'mark-all-read-btn': {'endpoint': '/notifications/mark_all_read', 'data': {}},
    'manual-alert-btn': {'endpoint': '/notifications/manual', 'data': {}},
    'send-manual-alert-btn': {'endpoint': '/notifications/send', 'data': {}},
    
    # Email buttons
    'test-email-btn': {'endpoint': '/email/test', 'data': {}},
    'send-test-alert-btn': {'endpoint': '/email/test_alert', 'data': {}},
    'email-config-btn': {'endpoint': '/email/config', 'data': {}},
    'email-test-btn': {'endpoint': '/email/test', 'data': {}},
    'email-notifications-toggle-btn': {'endpoint': '/email/toggle', 'data': {}},
    'email-address-update-btn': {'endpoint': '/email/update', 'data': {}},
    'test-email-alert-btn': {'endpoint': '/email/test_alert', 'data': {}},
    'test-email-system-btn': {'endpoint': '/email/test_system', 'data': {}},
    
    # ML buttons
    'ml-compatibility-check-btn': {'endpoint': '/ml/compatibility/check', 'data': {}},
    'ml-compatibility-fix-btn': {'endpoint': '/ml/compatibility/fix', 'data': {}},
    'ml-recommendations-btn': {'endpoint': '/ml/recommendations', 'data': {}},
    'force-model-update-btn': {'endpoint': '/ml/force_update', 'data': {}},
    
    # Performance buttons
    'performance-dashboard-btn': {'endpoint': '/performance/dashboard', 'data': {}},
    'performance-metrics-btn': {'endpoint': '/performance/metrics', 'data': {}},
    'portfolio-btn': {'endpoint': '/portfolio', 'data': {}},
    
    # Settings buttons
    'load-auto-settings-btn': {'endpoint': '/settings/load', 'data': {}},
    'save-auto-settings-btn': {'endpoint': '/settings/save', 'data': {}},
    
    # Trade integration buttons
    'enable-trade-integration-btn': {'endpoint': '/trading/enable', 'data': {}},
    'disable-trade-integration-btn': {'endpoint': '/trading/disable', 'data': {}},
    
    # Virtual balance buttons
    'virtual-balance-reset-btn': {'endpoint': '/balance/reset', 'data': {}},
    
    # Test buttons
    'test-db-btn': {'endpoint': '/test/database', 'data': {}},
}

def generate_callback_code(button_id, config):
    """Generate callback code for a button"""
    
    # Create safe function name
    func_name = button_id.replace('-', '_').replace('btn_', '').replace('_btn', '')
    
    # Determine output ID
    output_id = f"{button_id}-output"
    
    callback_code = f'''
@app.callback(
    Output('{output_id}', 'children'),
    Input('{button_id}', 'n_clicks'),
    prevent_initial_call=True
)
def {func_name}_callback(n_clicks):
    """Callback for {button_id}"""
    if not n_clicks:
        return ""
    
    try:
        debugger.log_button_click('{button_id}', n_clicks, {{}})
        
        # Make API call
        response = make_api_call("POST", "{config['endpoint']}", {json.dumps(config['data'])})
        
        if response and response.get('success', True):
            result = f"[OK] {{response.get('message', 'Success')}}"
        else:
            result = f"[ERROR] {{response.get('error', 'Failed')}}"
        
        debugger.log_callback_result('{button_id}', result)
        return result
        
    except Exception as e:
        error_msg = f"[ERROR] {{str(e)}}"
        debugger.log_callback_error('{button_id}', error_msg)
        return error_msg
'''
    
    return callback_code

def create_missing_outputs_in_layout():
    """Create missing output divs in layout.py"""
    
    # Read current layout
    with open('layout.py', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Find all button IDs that need output divs
    missing_outputs = []
    
    for button_id in BUTTON_MAPPING.keys():
        output_id = f"{button_id}-output"
        if output_id not in layout_content:
            missing_outputs.append(output_id)
    
    if not missing_outputs:
        print("All output divs already exist in layout")
        return
    
    print(f"Adding {len(missing_outputs)} missing output divs to layout")
    
    # Add missing output divs to the layout
    # Find a good place to add them (before the closing of main layout)
    
    # Create output divs code
    output_divs_code = "\n        # Button output divs\n"
    for output_id in missing_outputs:
        output_divs_code += f"        html.Div(id='{output_id}', style={{'display': 'none'}}),\n"
    
    # Find where to insert (look for the end of children list)
    # Insert before the last closing bracket
    insertion_point = layout_content.rfind(']')
    if insertion_point != -1:
        layout_content = layout_content[:insertion_point] + output_divs_code + layout_content[insertion_point:]
    
    # Write back
    with open('layout.py', 'w', encoding='utf-8') as f:
        f.write(layout_content)
    
    print(f"✅ Added {len(missing_outputs)} output divs to layout")

def restore_all_button_functionality():
    """Restore functionality for all orphaned buttons"""
    
    print("=== RESTORING ALL BUTTON FUNCTIONALITY ===")
    
    # Read orphaned buttons from analysis report
    with open('comprehensive_analysis_report.json', 'r') as f:
        report = json.load(f)
    
    orphaned_buttons = report.get('orphaned_buttons', [])
    
    print(f"Found {len(orphaned_buttons)} orphaned buttons to fix")
    
    # Filter to only buttons we have mapping for
    buttons_to_fix = [btn for btn in orphaned_buttons if btn in BUTTON_MAPPING]
    
    print(f"Creating callbacks for {len(buttons_to_fix)} buttons")
    
    # Generate callback code for each button
    all_callback_code = []
    
    for button_id in buttons_to_fix:
        config = BUTTON_MAPPING[button_id]
        callback_code = generate_callback_code(button_id, config)
        all_callback_code.append(callback_code)
    
    # Read current callbacks.py
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        callbacks_content = f.read()
    
    # Add new callbacks at the end
    new_callbacks_section = f"""

# === RESTORED BUTTON FUNCTIONALITY ===
# Auto-generated callbacks for orphaned buttons
{''.join(all_callback_code)}

# === END RESTORED FUNCTIONALITY ===
"""
    
    # Write back
    with open('callbacks.py', 'w', encoding='utf-8') as f:
        f.write(callbacks_content + new_callbacks_section)
    
    print(f"✅ Added {len(buttons_to_fix)} button callbacks")
    
    # Create missing output divs
    create_missing_outputs_in_layout()
    
    print("✅ ALL BUTTON FUNCTIONALITY RESTORED!")
    print(f"Total buttons fixed: {len(buttons_to_fix)}")
    print("\nNext steps:")
    print("1. Restart the dashboard")
    print("2. Test all buttons")
    print("3. Check dashboard logs for any errors")

if __name__ == "__main__":
    restore_all_button_functionality()
