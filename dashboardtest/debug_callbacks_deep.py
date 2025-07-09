#!/usr/bin/env python3
"""
Dashboard Callback Debugging Script
Deep dive into why buttons aren't working despite working endpoints
"""

import requests
import json
import os
from datetime import datetime

def check_callback_registration():
    """Check if callbacks are properly registered"""
    print("🔍 CHECKING CALLBACK REGISTRATION")
    print("="*50)
    
    try:
        # Check if callbacks.py can be imported
        import sys
        sys.path.append('.')
        
        print("1. Testing callback file import...")
        import callbacks
        print("   ✅ callbacks.py imported successfully")
        
        # Check if app is imported in callbacks
        if hasattr(callbacks, 'app'):
            print("   ✅ app object found in callbacks")
        else:
            print("   ❌ app object NOT found in callbacks")
            
        # Check if make_api_call function exists
        if hasattr(callbacks, 'make_api_call'):
            print("   ✅ make_api_call function found")
        else:
            print("   ❌ make_api_call function NOT found")
            
        return True
    except Exception as e:
        print(f"   ❌ Failed to import callbacks: {e}")
        return False

def check_layout_button_ids():
    """Check if button IDs exist in layout"""
    print("\n🔍 CHECKING LAYOUT BUTTON IDs")
    print("="*50)
    
    try:
        # Read layout file and check for common button IDs
        with open('layout.py', 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        critical_button_ids = [
            'sidebar-analytics-btn',
            'test-ml-btn', 
            'reset-balance-btn',
            'sidebar-predict-btn',
            'execute-signal-btn',
            'refresh-model-versions',
            'quick-predict-btn'
        ]
        
        found_buttons = []
        missing_buttons = []
        
        for button_id in critical_button_ids:
            if button_id in layout_content:
                found_buttons.append(button_id)
                print(f"   ✅ Found: {button_id}")
            else:
                missing_buttons.append(button_id)
                print(f"   ❌ Missing: {button_id}")
        
        print(f"\n📊 Button IDs: {len(found_buttons)}/{len(critical_button_ids)} found")
        return len(missing_buttons) == 0
        
    except Exception as e:
        print(f"   ❌ Failed to read layout.py: {e}")
        return False

def check_callback_button_mapping():
    """Check if callbacks are mapped to correct button IDs"""
    print("\n🔍 CHECKING CALLBACK-BUTTON MAPPING")
    print("="*50)
    
    try:
        # Read callbacks file and check for button ID mappings
        with open('callbacks.py', 'r', encoding='utf-8') as f:
            callbacks_content = f.read()
        
        # Count @app.callback decorators
        callback_count = callbacks_content.count('@app.callback')
        print(f"   📊 Total @app.callback decorators: {callback_count}")
        
        # Check for specific button inputs
        button_inputs = [
            'sidebar-analytics-btn',
            'test-ml-btn',
            'reset-balance-btn',
            'sidebar-predict-btn'
        ]
        
        mapped_buttons = []
        unmapped_buttons = []
        
        for button_id in button_inputs:
            if f"Input('{button_id}'" in callbacks_content or f'Input("{button_id}"' in callbacks_content:
                mapped_buttons.append(button_id)
                print(f"   ✅ Callback mapped: {button_id}")
            else:
                unmapped_buttons.append(button_id)
                print(f"   ❌ No callback: {button_id}")
        
        print(f"\n📊 Mapped callbacks: {len(mapped_buttons)}/{len(button_inputs)}")
        return len(unmapped_buttons) == 0
        
    except Exception as e:
        print(f"   ❌ Failed to read callbacks.py: {e}")
        return False

def check_debug_logging():
    """Check if debug logging is working"""
    print("\n🔍 CHECKING DEBUG LOGGING")
    print("="*50)
    
    try:
        # Check if debug log file exists and has recent entries
        log_files = ['dashboard_debug.log', 'debug.log']
        
        for log_file in log_files:
            if os.path.exists(log_file):
                print(f"   ✅ Found log file: {log_file}")
                
                # Check file size and recent content
                size = os.path.getsize(log_file)
                print(f"   📊 Log size: {size} bytes")
                
                if size > 0:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        print(f"   📊 Log lines: {len(lines)}")
                        
                        # Show last few lines
                        if lines:
                            print("   📝 Recent log entries:")
                            for line in lines[-3:]:
                                print(f"      {line.strip()}")
                else:
                    print("   ⚠️  Log file is empty")
            else:
                print(f"   ❌ Log file not found: {log_file}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to check debug logs: {e}")
        return False

def check_dash_app_configuration():
    """Check Dash app configuration"""
    print("\n🔍 CHECKING DASH APP CONFIGURATION")
    print("="*50)
    
    try:
        # Check dash_app.py
        if os.path.exists('dash_app.py'):
            with open('dash_app.py', 'r', encoding='utf-8') as f:
                dash_app_content = f.read()
            
            print("   ✅ dash_app.py exists")
            
            # Check for suppress_callback_exceptions
            if 'suppress_callback_exceptions=True' in dash_app_content:
                print("   ✅ suppress_callback_exceptions=True found")
            else:
                print("   ⚠️  suppress_callback_exceptions not set to True")
                
            # Check for external stylesheets
            if 'external_stylesheets' in dash_app_content:
                print("   ✅ external_stylesheets configured")
            else:
                print("   ⚠️  external_stylesheets not found")
                
        else:
            print("   ❌ dash_app.py not found")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to check dash app: {e}")
        return False

def test_simple_callback():
    """Test if a simple callback would work"""
    print("\n🔍 TESTING SIMPLE CALLBACK SIMULATION")
    print("="*50)
    
    try:
        # Simulate what happens when a button is clicked
        print("   🧪 Simulating button click process...")
        
        # Test API call mechanism
        print("   1. Testing make_api_call function...")
        import requests
        
        # Test the exact same call that buttons would make
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("   ✅ Direct API call works")
            else:
                print(f"   ❌ Direct API call failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Direct API call error: {e}")
            
        # Test session creation
        print("   2. Testing session creation...")
        session = requests.Session()
        try:
            response = session.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("   ✅ Session-based API call works")
            else:
                print(f"   ❌ Session-based API call failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Session-based API call error: {e}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Callback simulation failed: {e}")
        return False

def main():
    print("🔍 DASHBOARD CALLBACK DEEP DIVE ANALYSIS")
    print("="*70)
    print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Working Directory:", os.getcwd())
    
    # Run all checks
    checks = [
        ("Callback Registration", check_callback_registration),
        ("Layout Button IDs", check_layout_button_ids), 
        ("Callback-Button Mapping", check_callback_button_mapping),
        ("Debug Logging", check_debug_logging),
        ("Dash App Configuration", check_dash_app_configuration),
        ("Simple Callback Test", test_simple_callback)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n" + "="*70)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print(f"\n" + "="*70)
    print("📊 ANALYSIS SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {check_name}")
    
    print(f"\n📊 Overall: {passed}/{total} checks passed")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("="*70)
    
    if passed == total:
        print("🎯 All checks passed! The issue might be:")
        print("   1. JavaScript errors in browser console")
        print("   2. Dash clientside callback conflicts")
        print("   3. Callback output components not found in layout")
        print("   4. Debug decorators preventing callback execution")
    else:
        print("🔧 Issues found! Priority fixes:")
        for check_name, result in results:
            if not result:
                print(f"   • Fix: {check_name}")

if __name__ == "__main__":
    main()
