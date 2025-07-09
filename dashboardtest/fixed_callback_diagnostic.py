#!/usr/bin/env python3
"""
Fixed Dashboard Callback Diagnostic Script
This script tests callback registration and functionality with proper import handling
"""

import sys
import os
import logging
import json
from datetime import datetime
import requests
import time

# Windows-specific encoding setup
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except:
        pass

def safe_print(message):
    """Safely print messages with emoji support"""
    try:
        print(message)
        sys.stdout.flush()
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🔧": "[CONFIG]", "✅": "[OK]", "❌": "[ERROR]", "🚀": "[START]",
            "📊": "[DASHBOARD]", "💎": "[SUCCESS]", "🎉": "[READY]", "🐛": "[DEBUG]",
            "⚡": "[CALLBACK]", "🔍": "[TEST]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Add parent directory to path
sys.path.append(os.path.dirname(dashboard_dir))

def test_simple_app_import():
    """Test simple app import without callbacks"""
    safe_print("🔍 Testing simple app import...")
    
    try:
        # Test importing the main dash app first
        from dash_app import app
        safe_print("✅ Successfully imported app from dash_app")
        
        # Check if it's a proper Dash app
        if hasattr(app, 'callback'):
            safe_print("✅ App has callback method")
        else:
            safe_print("❌ App does not have callback method")
            return False
            
        if hasattr(app, 'layout'):
            safe_print("✅ App has layout attribute")
        else:
            safe_print("⚠️ App does not have layout attribute yet")
            
        return True
        
    except Exception as e:
        safe_print(f"❌ App import failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_layout_import():
    """Test layout import"""
    safe_print("🔍 Testing layout import...")
    
    try:
        from layout import layout
        safe_print("✅ Successfully imported layout")
        
        # Check if layout is not None
        if layout is not None:
            safe_print("✅ Layout is not None")
        else:
            safe_print("❌ Layout is None")
            return False
            
        return True
        
    except Exception as e:
        safe_print(f"❌ Layout import failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_callbacks_import():
    """Test callbacks import separately"""
    safe_print("🔍 Testing callbacks import...")
    
    try:
        # Import callbacks module
        import callbacks
        safe_print("✅ Successfully imported callbacks module")
        return True
        
    except Exception as e:
        safe_print(f"❌ Callbacks import failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_complete_app_setup():
    """Test complete app setup with layout and callbacks"""
    safe_print("🔍 Testing complete app setup...")
    
    try:
        # Import app
        from dash_app import app
        safe_print("✅ App imported")
        
        # Import layout
        from layout import layout
        safe_print("✅ Layout imported")
        
        # Set layout
        app.layout = layout
        safe_print("✅ Layout assigned to app")
        
        # Import callbacks (this should register them)
        import callbacks
        safe_print("✅ Callbacks imported")
        
        # Check if callbacks were registered
        if hasattr(app, 'callback_map'):
            callback_count = len(app.callback_map)
            safe_print(f"⚡ Callbacks registered: {callback_count}")
            
            if callback_count > 0:
                safe_print("✅ Callbacks successfully registered")
                return True
            else:
                safe_print("❌ No callbacks were registered")
                return False
        else:
            safe_print("❌ App doesn't have callback_map attribute")
            return False
        
    except Exception as e:
        safe_print(f"❌ Complete app setup failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_dashboard_response():
    """Test if dashboard is responding"""
    safe_print("🔍 Testing dashboard response...")
    
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        if response.status_code == 200:
            safe_print("✅ Dashboard is responding to HTTP requests")
            
            # Check if the response contains expected elements
            content = response.text
            if "crypto" in content.lower() or "dashboard" in content.lower():
                safe_print("✅ Dashboard content looks correct")
            else:
                safe_print("⚠️ Dashboard content may be incomplete")
            
            return True
        else:
            safe_print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        safe_print("❌ Cannot connect to dashboard - is it running?")
        return False
    except Exception as e:
        safe_print(f"❌ Dashboard response test failed: {e}")
        return False

def test_callback_endpoints():
    """Test if callback endpoints are accessible"""
    safe_print("🔍 Testing callback endpoints...")
    
    callback_endpoints = [
        "/_dash-layout",
        "/_dash-dependencies"
    ]
    
    results = {}
    
    for endpoint in callback_endpoints:
        try:
            url = f"http://localhost:8050{endpoint}"
            response = requests.get(url, timeout=5)
            results[endpoint] = {
                "status_code": response.status_code,
                "accessible": response.status_code in [200, 302]
            }
            
            if results[endpoint]["accessible"]:
                safe_print(f"✅ {endpoint}: accessible")
            else:
                safe_print(f"❌ {endpoint}: not accessible ({response.status_code})")
                
        except Exception as e:
            safe_print(f"❌ {endpoint}: error - {e}")
            results[endpoint] = {
                "status_code": None,
                "accessible": False,
                "error": str(e)
            }
    
    return results

def run_comprehensive_diagnostic():
    """Run all diagnostic tests"""
    safe_print("🚀 Starting Fixed Callback Diagnostic...")
    safe_print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test 1: Simple App Import
    safe_print("\n📋 Test 1: Simple App Import")
    results["tests"]["app_import"] = test_simple_app_import()
    
    # Test 2: Layout Import
    safe_print("\n📋 Test 2: Layout Import")
    results["tests"]["layout_import"] = test_layout_import()
    
    # Test 3: Callbacks Import
    safe_print("\n📋 Test 3: Callbacks Import")
    results["tests"]["callbacks_import"] = test_callbacks_import()
    
    # Test 4: Complete App Setup
    safe_print("\n📋 Test 4: Complete App Setup")
    results["tests"]["complete_setup"] = test_complete_app_setup()
    
    # Test 5: Dashboard Response
    safe_print("\n📋 Test 5: Dashboard Response")
    results["tests"]["dashboard_response"] = test_dashboard_response()
    
    # Test 6: Callback Endpoints
    safe_print("\n📋 Test 6: Callback Endpoints")
    results["tests"]["callback_endpoints"] = test_callback_endpoints()
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 DIAGNOSTIC SUMMARY")
    safe_print("=" * 60)
    
    passed_tests = 0
    total_tests = len(results["tests"])
    
    for test_name, result in results["tests"].items():
        if result is True:
            passed_tests += 1
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        elif isinstance(result, dict):
            # For callback_endpoints test
            if all(endpoint.get("accessible", False) for endpoint in result.values()):
                passed_tests += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
        else:
            status = "⚠️ UNKNOWN"
            
        safe_print(f"{test_name}: {status}")
    
    safe_print(f"\nTests Passed: {passed_tests}/{total_tests}")
    
    # Save results
    with open("fixed_callback_diagnostic_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    safe_print(f"\n💾 Results saved to: fixed_callback_diagnostic_results.json")
    
    # Recommendations
    safe_print("\n🔧 RECOMMENDATIONS:")
    if not results["tests"]["app_import"]:
        safe_print("1. Fix app import issues in dash_app.py")
    if not results["tests"]["layout_import"]:
        safe_print("2. Fix layout import issues in layout.py")
    if not results["tests"]["callbacks_import"]:
        safe_print("3. Fix callback import issues in callbacks.py")
    if not results["tests"]["complete_setup"]:
        safe_print("4. Fix callback registration - this is the main issue")
    if not results["tests"]["dashboard_response"]:
        safe_print("5. Ensure dashboard server is running on port 8050")
    
    safe_print("\n🎉 Fixed diagnostic complete!")
    return results

if __name__ == "__main__":
    run_comprehensive_diagnostic()
