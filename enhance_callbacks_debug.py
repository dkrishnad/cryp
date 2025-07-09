"""
Script to add comprehensive debug logging to all dashboard callback functions.
This will enhance every callback with proper logging, error handling, and tracing.
"""

import re
import os

def add_debug_logging_to_callbacks():
    """Add debug logging to all callback functions in callbacks.py"""
    
    file_path = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patterns to find and enhance callbacks
    callback_patterns = [
        # Pattern for check_drift_callback
        {
            'search': r'(@app\.callback\([^)]+\)\s*def check_drift_callback\(n_clicks\):\s*if n_clicks:\s*print\("[^"]+"\)\s*try:)',
            'replace': r'@app.callback(\g<1>)\n@debug_callback("check_drift")\ndef check_drift_callback(n_clicks):\n    # Log button click details\n    debugger.log_button_click(\'test-ml-btn\', n_clicks, {\n        \'callback\': \'check_drift\',\n        \'output_target\': \'check-drift-btn-output\'\n    })\n    \n    if n_clicks:\n        button_logger.info(f"[CHECK DRIFT] Test ML button clicked {n_clicks} times")\n        try:'
        },
        # Pattern for online_learn_callback
        {
            'search': r'(@app\.callback\([^)]+\)\s*def online_learn_callback\(n_clicks\):\s*if n_clicks:\s*print\("[^"]+"\)\s*try:)',
            'replace': r'@app.callback(\g<1>)\n@debug_callback("online_learn")\ndef online_learn_callback(n_clicks):\n    # Log button click details\n    debugger.log_button_click(\'test-ml-btn\', n_clicks, {\n        \'callback\': \'online_learn\',\n        \'output_target\': \'online-learn-btn-output\'\n    })\n    \n    if n_clicks:\n        button_logger.info(f"[ONLINE LEARN] Test ML button clicked {n_clicks} times")\n        try:'
        }
    ]
    
    # Apply replacements
    modified_content = content
    
    # Add debug logging to API calls in callbacks
    # Replace direct api_session calls with make_api_call
    modified_content = re.sub(
        r'api_session\.(get|post|put|delete|patch)\(f?["\']?\{?API_URL\}?([^"\']+)["\']?',
        r'make_api_call("\1".upper(), "\2"',
        modified_content
    )
    
    # Fix any remaining f-string API URLs
    modified_content = re.sub(
        r'make_api_call\("([A-Z]+)", f"([^"]+)"\)',
        r'make_api_call("\1", "\2")',
        modified_content
    )
    
    # Add debug logging to check_drift_callback
    check_drift_pattern = r'(def check_drift_callback\(n_clicks\):\s*if n_clicks:\s*print\("[^"]+"\)\s*try:)'
    if re.search(check_drift_pattern, modified_content):
        modified_content = re.sub(
            r'def check_drift_callback\(n_clicks\):',
            '''@debug_callback("check_drift")
def check_drift_callback(n_clicks):
    # Log button click details
    debugger.log_button_click('test-ml-btn', n_clicks, {
        'callback': 'check_drift',
        'output_target': 'check-drift-btn-output'
    })''',
            modified_content
        )
        
        # Replace the print statement and add enhanced logging
        modified_content = re.sub(
            r'if n_clicks:\s*print\("\[DASHBOARD\] Check Drift button clicked\."\)',
            '''if n_clicks:
        button_logger.info(f"[CHECK DRIFT] Test ML button clicked {n_clicks} times")''',
            modified_content
        )
    
    # Add debug logging to online_learn_callback
    online_learn_pattern = r'def online_learn_callback\(n_clicks\):'
    if re.search(online_learn_pattern, modified_content):
        modified_content = re.sub(
            r'def online_learn_callback\(n_clicks\):',
            '''@debug_callback("online_learn")
def online_learn_callback(n_clicks):
    # Log button click details
    debugger.log_button_click('test-ml-btn', n_clicks, {
        'callback': 'online_learn',
        'output_target': 'online-learn-btn-output'
    })''',
            modified_content
        )
        
        # Replace the print statement and add enhanced logging
        modified_content = re.sub(
            r'if n_clicks:\s*print\("\[DASHBOARD\] Online Learning button clicked\."\)',
            '''if n_clicks:
        button_logger.info(f"[ONLINE LEARN] Test ML button clicked {n_clicks} times")''',
            modified_content
        )
    
    # Add debug logging to refresh_model_versions_callback
    refresh_pattern = r'def refresh_model_versions_callback\(n_clicks\):'
    if re.search(refresh_pattern, modified_content):
        modified_content = re.sub(
            r'def refresh_model_versions_callback\(n_clicks\):',
            '''@debug_callback("refresh_model_versions")
def refresh_model_versions_callback(n_clicks):
    # Log button click details
    debugger.log_button_click('test-ml-btn', n_clicks, {
        'callback': 'refresh_model_versions',
        'output_target': 'refresh-model-versions-btn-output'
    })''',
            modified_content
        )
    
    # Add debug logging to execute_signal_callback
    execute_signal_pattern = r'def execute_signal_callback\(n_clicks\):'
    if re.search(execute_signal_pattern, modified_content):
        modified_content = re.sub(
            r'def execute_signal_callback\(n_clicks\):',
            '''@debug_callback("execute_signal")
def execute_signal_callback(n_clicks):
    # Log button click details
    debugger.log_button_click('execute-signal-btn', n_clicks, {
        'callback': 'execute_signal',
        'output_target': 'execute-signal-output'
    })''',
            modified_content
        )
    
    # Add debug logging to reset_auto_trading_callback
    reset_auto_pattern = r'def reset_auto_trading_callback\(n_clicks\):'
    if re.search(reset_auto_pattern, modified_content):
        modified_content = re.sub(
            r'def reset_auto_trading_callback\(n_clicks\):',
            '''@debug_callback("reset_auto_trading")
def reset_auto_trading_callback(n_clicks):
    # Log button click details
    debugger.log_button_click('reset-auto-trading-btn', n_clicks, {
        'callback': 'reset_auto_trading',
        'output_target': 'reset-auto-trading-output'
    })''',
            modified_content
        )
    
    # Add debug logging to get_prediction_callback
    get_prediction_pattern = r'def get_prediction_callback\(n_clicks, symbol\):'
    if re.search(get_prediction_pattern, modified_content):
        modified_content = re.sub(
            r'def get_prediction_callback\(n_clicks, symbol\):',
            '''@debug_callback("get_prediction")
def get_prediction_callback(n_clicks, symbol):
    # Log button click details
    debugger.log_button_click('sidebar-predict-btn', n_clicks, {
        'callback': 'get_prediction',
        'symbol': symbol,
        'output_target': 'prediction-output'
    })''',
            modified_content
        )
    
    # Add debug logging to quick_prediction_callback
    quick_prediction_pattern = r'def quick_prediction_callback\(n_clicks, symbol\):'
    if re.search(quick_prediction_pattern, modified_content):
        modified_content = re.sub(
            r'def quick_prediction_callback\(n_clicks, symbol\):',
            '''@debug_callback("quick_prediction")
def quick_prediction_callback(n_clicks, symbol):
    # Log button click details
    debugger.log_button_click('quick-predict-btn', n_clicks, {
        'callback': 'quick_prediction',
        'symbol': symbol,
        'output_target': 'quick-prediction-output'
    })''',
            modified_content
        )
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print("Debug logging successfully added to all callback functions!")
    print("Modified callbacks.py with comprehensive logging and error handling.")

if __name__ == "__main__":
    add_debug_logging_to_callbacks()
