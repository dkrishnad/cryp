#!/usr/bin/env python3
"""
Connect additional unused backend endpoints to the frontend
Priority: Auto trading controls, email settings, notification management
"""

import os
import re

def connect_auto_trading_endpoints():
    """Add callbacks for auto trading control endpoints"""
    auto_trading_callbacks = '''

# Auto Trading Controls Callbacks
@app.callback(
    Output('auto-trading-toggle-status', 'children'),
    [Input('auto-trading-toggle-btn', 'n_clicks')]
)
def toggle_auto_trading(n_clicks):
    if n_clicks is None:
        return "Auto trading not toggled"
    
    try:
        response = requests.post(f"{BASE_URL}/auto_trading/toggle")
        if response.status_code == 200:
            data = response.json()
            return f"Auto Trading: {data.get('status', 'Unknown')}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('auto-trading-settings-data', 'children'),
    [Input('auto-trading-settings-btn', 'n_clicks')]
)
def get_auto_trading_settings(n_clicks):
    if n_clicks is None:
        return "Settings not loaded"
    
    try:
        response = requests.get(f"{BASE_URL}/auto_trading/settings")
        if response.status_code == 200:
            data = response.json()
            return f"Auto Trading Settings: Risk={data.get('risk_level', 'N/A')}, Max Trades={data.get('max_trades', 'N/A')}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('auto-trading-signals-data', 'children'),
    [Input('auto-trading-signals-btn', 'n_clicks')]
)
def get_auto_trading_signals(n_clicks):
    if n_clicks is None:
        return "No signals data"
    
    try:
        response = requests.get(f"{BASE_URL}/auto_trading/signals")
        if response.status_code == 200:
            data = response.json()
            return f"Trading Signals: {len(data.get('signals', []))} active signals"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('auto-trading-status-display', 'children'),
    [Input('auto-trading-status-refresh-btn', 'n_clicks')]
)
def get_auto_trading_status(n_clicks):
    if n_clicks is None:
        return "Status not refreshed"
    
    try:
        response = requests.get(f"{BASE_URL}/auto_trading/status")
        if response.status_code == 200:
            data = response.json()
            return f"Auto Trading Status: {data.get('enabled', False)}, Trades Today: {data.get('trades_today', 0)}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('futures-execute-signal-status', 'children'),
    [Input('futures-execute-signal-btn', 'n_clicks')]
)
def execute_futures_signal(n_clicks):
    if n_clicks is None:
        return "No signal executed"
    
    try:
        response = requests.post(f"{BASE_URL}/auto_trading/execute_futures_signal")
        if response.status_code == 200:
            data = response.json()
            return f"Futures Signal Executed: {data.get('result', 'Unknown')}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

'''
    return auto_trading_callbacks

def connect_email_endpoints():
    """Add callbacks for email configuration endpoints"""
    email_callbacks = '''

# Email Configuration Callbacks
@app.callback(
    Output('email-config-status', 'children'),
    [Input('email-config-btn', 'n_clicks')]
)
def get_email_config(n_clicks):
    if n_clicks is None:
        return "Email config not loaded"
    
    try:
        response = requests.get(f"{BASE_URL}/email/config")
        if response.status_code == 200:
            data = response.json()
            return f"Email Config: SMTP={data.get('smtp_enabled', False)}, Address={data.get('email_address', 'Not set')}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('email-test-status', 'children'),
    [Input('email-test-btn', 'n_clicks')]
)
def send_test_email(n_clicks):
    if n_clicks is None:
        return "No test email sent"
    
    try:
        response = requests.post(f"{BASE_URL}/email/send_test")
        if response.status_code == 200:
            return "Test email sent successfully"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('email-address-status', 'children'),
    [Input('email-address-update-btn', 'n_clicks'),
     Input('email-address-input', 'value')]
)
def update_email_address(n_clicks, email_address):
    if n_clicks is None:
        return "Email address not updated"
    
    try:
        data = {'email_address': email_address or ''}
        response = requests.post(f"{BASE_URL}/settings/email_address", json=data)
        if response.status_code == 200:
            return f"Email address updated: {email_address}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('email-notifications-status', 'children'),
    [Input('email-notifications-toggle-btn', 'n_clicks')]
)
def toggle_email_notifications(n_clicks):
    if n_clicks is None:
        return "Email notifications not toggled"
    
    try:
        response = requests.post(f"{BASE_URL}/settings/email_notifications")
        if response.status_code == 200:
            data = response.json()
            return f"Email Notifications: {data.get('enabled', False)}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

'''
    return email_callbacks

def connect_notification_endpoints():
    """Add callbacks for notification management endpoints"""
    notification_callbacks = '''

# Notification Management Callbacks
@app.callback(
    Output('notifications-clear-status', 'children'),
    [Input('notifications-clear-btn', 'n_clicks')]
)
def clear_notifications(n_clicks):
    if n_clicks is None:
        return "Notifications not cleared"
    
    try:
        response = requests.post(f"{BASE_URL}/notifications/clear")
        if response.status_code == 200:
            return "All notifications cleared"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('notifications-mark-read-status', 'children'),
    [Input('notifications-mark-read-btn', 'n_clicks')]
)
def mark_notifications_read(n_clicks):
    if n_clicks is None:
        return "Notifications not marked as read"
    
    try:
        response = requests.post(f"{BASE_URL}/notifications/mark_read")
        if response.status_code == 200:
            return "All notifications marked as read"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('manual-alert-status', 'children'),
    [Input('manual-alert-btn', 'n_clicks'),
     Input('manual-alert-message', 'value')]
)
def send_manual_alert(n_clicks, message):
    if n_clicks is None:
        return "No manual alert sent"
    
    try:
        data = {'message': message or 'Test alert'}
        response = requests.post(f"{BASE_URL}/alerts/send_manual", json=data)
        if response.status_code == 200:
            return f"Manual alert sent: {message}"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('test-email-alert-status', 'children'),
    [Input('test-email-alert-btn', 'n_clicks')]
)
def test_email_alert(n_clicks):
    if n_clicks is None:
        return "No test email alert sent"
    
    try:
        response = requests.post(f"{BASE_URL}/alerts/test_email")
        if response.status_code == 200:
            return "Test email alert sent successfully"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

'''
    return notification_callbacks

def connect_indicator_endpoints():
    """Add callbacks for indicator configuration endpoints"""
    indicator_callbacks = '''

# Indicator Configuration Callbacks
@app.callback(
    Output('indicators-config-data', 'children'),
    [Input('indicators-config-btn', 'n_clicks')]
)
def get_indicators_config(n_clicks):
    if n_clicks is None:
        return "Indicators config not loaded"
    
    try:
        response = requests.get(f"{BASE_URL}/indicators/config")
        if response.status_code == 200:
            data = response.json()
            return f"Indicators Config: {len(data.get('indicators', []))} indicators configured"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('indicators-refresh-status', 'children'),
    [Input('indicators-refresh-btn', 'n_clicks')]
)
def refresh_indicators(n_clicks):
    if n_clicks is None:
        return "Indicators not refreshed"
    
    try:
        response = requests.post(f"{BASE_URL}/indicators/refresh")
        if response.status_code == 200:
            return "Indicators refreshed successfully"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

'''
    return indicator_callbacks

def connect_amount_endpoints():
    """Add callbacks for sidebar amount endpoints"""
    amount_callbacks = '''

# Sidebar Amount Selection Callbacks
@app.callback(
    Output('amount-50-status', 'children'),
    [Input('amount-50-btn', 'n_clicks')]
)
def set_amount_50(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/50")
        if response.status_code == 200:
            return "Amount set to $50"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('amount-100-status', 'children'),
    [Input('amount-100-btn', 'n_clicks')]
)
def set_amount_100(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/100")
        if response.status_code == 200:
            return "Amount set to $100"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('amount-250-status', 'children'),
    [Input('amount-250-btn', 'n_clicks')]
)
def set_amount_250(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/250")
        if response.status_code == 200:
            return "Amount set to $250"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('amount-500-status', 'children'),
    [Input('amount-500-btn', 'n_clicks')]
)
def set_amount_500(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/500")
        if response.status_code == 200:
            return "Amount set to $500"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('amount-1000-status', 'children'),
    [Input('amount-1000-btn', 'n_clicks')]
)
def set_amount_1000(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/1000")
        if response.status_code == 200:
            return "Amount set to $1000"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.callback(
    Output('amount-max-status', 'children'),
    [Input('amount-max-btn', 'n_clicks')]
)
def set_amount_max(n_clicks):
    if n_clicks is None:
        return "Amount not set"
    
    try:
        response = requests.post(f"{BASE_URL}/sidebar/amount/max")
        if response.status_code == 200:
            return "Amount set to maximum balance"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

'''
    return amount_callbacks

def apply_callbacks_to_file():
    """Apply all new callbacks to the callbacks.py file"""
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    # Read current file
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add all new callbacks
    new_callbacks = ""
    new_callbacks += connect_auto_trading_endpoints()
    new_callbacks += connect_email_endpoints()
    new_callbacks += connect_notification_endpoints()
    new_callbacks += connect_indicator_endpoints()
    new_callbacks += connect_amount_endpoints()
    
    # Append to file
    content += new_callbacks
    
    # Write back
    with open(callbacks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added callbacks for auto trading controls, email settings, notifications, indicators, and amount selection")
    print(f"📊 Added approximately 20+ new endpoint connections")

if __name__ == "__main__":
    apply_callbacks_to_file()
    print("🎯 Second batch of endpoint connections complete!")
