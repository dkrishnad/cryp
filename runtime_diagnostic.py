#!/usr/bin/env python3
"""
Runtime Dashboard Diagnostic Script
This script will start the dashboard and capture actual runtime errors
"""
import sys
import os
import traceback
import threading
import time
import requests
from io import StringIO

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboardtest'))

def capture_app_errors():
    """Capture errors from the running app"""
    
    # Capture stderr to catch Dash errors
    old_stderr = sys.stderr
    captured_stderr = StringIO()
    
    try:
        # Import and start the app
        print("🔧 Importing dashboard components...")
        from dashboardtest.dash_app import app
        from dashboardtest.layout import layout
        import dashboardtest.callbacks
        
        app.layout = layout
        
        print("🚀 Starting dashboard with error capture...")
        
        # Redirect stderr to capture errors
        sys.stderr = captured_stderr
        
        # Start the app in a separate thread with error handling
        def run_app():
            try:
                app.run(
                    debug=True,  # Enable debug mode to see more errors
                    host='localhost',
                    port=8051,  # Use different port to avoid conflicts
                    dev_tools_ui=True,
                    dev_tools_props_check=True,
                    use_reloader=False  # Prevent reloader issues
                )
            except Exception as e:
                print(f"❌ App startup error: {e}")
                traceback.print_exc()
        
        app_thread = threading.Thread(target=run_app, daemon=True)
        app_thread.start()
        
        # Wait for app to start
        time.sleep(3)
        
        # Test the app endpoints
        print("🧪 Testing app endpoints...")
        
        try:
            # Test main page
            response = requests.get('http://localhost:8051', timeout=10)
            print(f"Main page status: {response.status_code}")
            if response.status_code != 200:
                print(f"Main page error: {response.text[:500]}")
                
        except Exception as e:
            print(f"❌ Failed to connect to dashboard: {e}")
        
        # Test callback endpoints
        try:
            # Test a simple callback by making a POST request
            callback_data = {
                'inputs': [{'id': 'live-price-interval', 'property': 'n_intervals', 'value': 1}],
                'state': [],
                'output': 'live-price-display.children'
            }
            
            response = requests.post(
                'http://localhost:8051/_dash-update-component',
                json=callback_data,
                timeout=10
            )
            print(f"Callback test status: {response.status_code}")
            if response.status_code != 200:
                print(f"Callback error: {response.text[:500]}")
                
        except Exception as e:
            print(f"❌ Callback test failed: {e}")
        
        # Keep running for a bit to capture any async errors
        print("🔍 Monitoring for runtime errors (10 seconds)...")
        time.sleep(10)
        
        # Restore stderr and show captured errors
        sys.stderr = old_stderr
        captured_errors = captured_stderr.getvalue()
        
        if captured_errors:
            print("\n❌ CAPTURED RUNTIME ERRORS:")
            print("=" * 60)
            print(captured_errors)
            print("=" * 60)
        else:
            print("✅ No runtime errors captured")
            
    except Exception as e:
        sys.stderr = old_stderr
        print(f"❌ Error during diagnostic: {e}")
        traceback.print_exc()

def test_individual_callbacks():
    """Test individual callback functions for errors"""
    
    print("\n🔧 Testing individual callback functions...")
    
    try:
        # Import the callbacks module
        import dashboardtest.callbacks as callbacks_module
        
        # Get all callback functions
        callback_functions = [
            name for name in dir(callbacks_module) 
            if callable(getattr(callbacks_module, name)) 
            and not name.startswith('_')
            and hasattr(getattr(callbacks_module, name), '__call__')
        ]
        
        print(f"Found {len(callback_functions)} callback functions")
        
        # Test a few key callbacks with dummy data
        test_callbacks = [
            'update_live_price',
            'update_prediction_display',
            'handle_buy_click',
            'handle_sell_click'
        ]
        
        for callback_name in test_callbacks:
            if hasattr(callbacks_module, callback_name):
                try:
                    callback_func = getattr(callbacks_module, callback_name)
                    print(f"✅ {callback_name} function exists")
                    
                    # Try to inspect the function signature
                    import inspect
                    sig = inspect.signature(callback_func)
                    print(f"   Parameters: {list(sig.parameters.keys())}")
                    
                except Exception as e:
                    print(f"❌ {callback_name} error: {e}")
            else:
                print(f"⚠️  {callback_name} not found")
                
    except Exception as e:
        print(f"❌ Error testing callbacks: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Starting Runtime Dashboard Diagnostic...")
    print("=" * 60)
    
    # Test callback functions first
    test_individual_callbacks()
    
    # Capture runtime errors
    capture_app_errors()
    
    print("\n📋 DIAGNOSTIC COMPLETE")
    print("Check the output above for any runtime errors or issues.")
