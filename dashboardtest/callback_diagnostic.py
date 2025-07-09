#!/usr/bin/env python3
"""
Comprehensive Dashboard Callback Diagnostic Script
This script tests callback registration and functionality
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

def test_callback_registration():
    """Test callback registration without running the server"""
    safe_print("🔍 Testing callback registration...")
    
    try:
        # Import the debug app
        from debug_dash_app import app
        
        # Load callbacks
        import callbacks
        
        # Load layout
        from layout import layout
        app.layout = layout
        
        # Check callback registration
        callback_count = len(app.callback_map)
        safe_print(f"⚡ Total callbacks registered: {callback_count}")
        
        if callback_count == 0:
            safe_print("❌ No callbacks registered! This is the root issue.")
            return False
        
        # List all registered callbacks
        safe_print("⚡ Registered callbacks:")
        for i, (callback_id, callback_obj) in enumerate(app.callback_map.items(), 1):
            safe_print(f"  {i}. {callback_id}")
            
            # Check callback details
            if hasattr(callback_obj, 'outputs'):
                outputs = callback_obj.outputs
                if isinstance(outputs, list):
                    safe_print(f"     Outputs: {[str(output) for output in outputs]}")
                else:
                    safe_print(f"     Output: {str(outputs)}")
            
            if hasattr(callback_obj, 'inputs'):
                inputs = callback_obj.inputs
                if isinstance(inputs, list):
                    safe_print(f"     Inputs: {[str(input_) for input_ in inputs]}")
                else:
                    safe_print(f"     Input: {str(inputs)}")
        
        safe_print("✅ Callback registration test completed successfully")
        return True
        
    except Exception as e:
        safe_print(f"❌ Callback registration test failed: {e}")
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
        "/_dash-component-suites/",
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
                safe_print(f"✅ {endpoint} is accessible")
            else:
                safe_print(f"❌ {endpoint} returned {response.status_code}")
                
        except Exception as e:
            results[endpoint] = {
                "status_code": None,
                "accessible": False,
                "error": str(e)
            }
            safe_print(f"❌ {endpoint} failed: {e}")
    
    return results

def simulate_callback_trigger():
    """Simulate a callback trigger by making a POST request"""
    safe_print("🔍 Simulating callback trigger...")
    
    try:
        # Try to get the layout first to get component IDs
        layout_response = requests.get("http://localhost:8050/_dash-layout", timeout=5)
        
        if layout_response.status_code != 200:
            safe_print(f"❌ Cannot get layout: {layout_response.status_code}")
            return False
        
        safe_print("✅ Layout endpoint accessible")
        
        # Try to get dependencies
        deps_response = requests.get("http://localhost:8050/_dash-dependencies", timeout=5)
        
        if deps_response.status_code != 200:
            safe_print(f"❌ Cannot get dependencies: {deps_response.status_code}")
            return False
        
        safe_print("✅ Dependencies endpoint accessible")
        
        # Parse dependencies to find a simple callback to test
        try:
            deps_data = deps_response.json()
            if deps_data and len(deps_data) > 0:
                safe_print(f"✅ Found {len(deps_data)} callback dependencies")
                
                # Try to find a simple callback with button input
                for dep in deps_data:
                    if 'inputs' in dep and dep['inputs']:
                        input_info = dep['inputs'][0]
                        if 'id' in input_info and 'property' in input_info:
                            component_id = input_info['id']
                            property_name = input_info['property']
                            
                            if property_name == 'n_clicks':
                                safe_print(f"⚡ Found button callback: {component_id}")
                                
                                # Simulate button click
                                callback_payload = {
                                    "inputs": [{"id": component_id, "property": property_name, "value": 1}],
                                    "state": [],
                                    "output": dep['output']['id'] + '.' + dep['output']['property']
                                }
                                
                                callback_response = requests.post(
                                    "http://localhost:8050/_dash-update-component",
                                    json=callback_payload,
                                    timeout=10
                                )
                                
                                if callback_response.status_code == 200:
                                    safe_print("✅ Callback simulation successful!")
                                    return True
                                else:
                                    safe_print(f"❌ Callback simulation failed: {callback_response.status_code}")
                                    safe_print(f"Response: {callback_response.text}")
                                    
                                break
            else:
                safe_print("❌ No callback dependencies found")
                
        except json.JSONDecodeError:
            safe_print("❌ Cannot parse dependencies JSON")
        
        return False
        
    except Exception as e:
        safe_print(f"❌ Callback simulation failed: {e}")
        return False

def check_browser_console_issues():
    """Check for common browser console issues"""
    safe_print("🔍 Checking for common browser console issues...")
    
    # Check if the dashboard page includes necessary scripts
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        issues = []
        
        # Check for Plotly
        if "plotly" not in content.lower():
            issues.append("Plotly.js may not be loaded")
        else:
            safe_print("✅ Plotly.js appears to be included")
        
        # Check for Dash renderer
        if "_dash-renderer" not in content:
            issues.append("Dash renderer may not be loaded")
        else:
            safe_print("✅ Dash renderer appears to be included")
        
        # Check for React
        if "react" not in content.lower():
            issues.append("React may not be loaded")
        else:
            safe_print("✅ React appears to be included")
        
        if issues:
            safe_print("⚠️ Potential browser console issues:")
            for issue in issues:
                safe_print(f"  - {issue}")
        else:
            safe_print("✅ No obvious browser console issues detected")
        
        return len(issues) == 0
        
    except Exception as e:
        safe_print(f"❌ Browser console check failed: {e}")
        return False

def run_comprehensive_diagnostic():
    """Run all diagnostic tests"""
    safe_print("🚀 Starting Comprehensive Dashboard Callback Diagnostic...")
    safe_print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test 1: Callback Registration
    safe_print("\n📋 Test 1: Callback Registration")
    results["tests"]["callback_registration"] = test_callback_registration()
    
    # Test 2: Dashboard Response
    safe_print("\n📋 Test 2: Dashboard Response")
    results["tests"]["dashboard_response"] = test_dashboard_response()
    
    # Test 3: Callback Endpoints
    safe_print("\n📋 Test 3: Callback Endpoints")
    results["tests"]["callback_endpoints"] = test_callback_endpoints()
    
    # Test 4: Callback Simulation
    safe_print("\n📋 Test 4: Callback Simulation")
    results["tests"]["callback_simulation"] = simulate_callback_trigger()
    
    # Test 5: Browser Console Issues
    safe_print("\n📋 Test 5: Browser Console Issues")
    results["tests"]["browser_console"] = check_browser_console_issues()
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 DIAGNOSTIC SUMMARY")
    safe_print("=" * 60)
    
    passed_tests = sum(1 for test, result in results["tests"].items() 
                      if result is True or (isinstance(result, dict) and 
                      all(endpoint.get("accessible", False) for endpoint in result.values())))
    total_tests = len(results["tests"])
    
    safe_print(f"Tests Passed: {passed_tests}/{total_tests}")
    
    for test_name, result in results["tests"].items():
        status = "✅ PASS" if result is True else "❌ FAIL" if result is False else "⚠️ PARTIAL"
        safe_print(f"{test_name}: {status}")
    
    # Save results
    with open("callback_diagnostic_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    safe_print(f"\n💾 Results saved to: callback_diagnostic_results.json")
    
    # Recommendations
    safe_print("\n🔧 RECOMMENDATIONS:")
    if not results["tests"]["callback_registration"]:
        safe_print("1. Check callback import and registration")
    if not results["tests"]["dashboard_response"]:
        safe_print("2. Ensure dashboard server is running on port 8050")
    if not results["tests"]["callback_simulation"]:
        safe_print("3. Check callback function implementations")
    if not results["tests"]["browser_console"]:
        safe_print("4. Check browser console for JavaScript errors")
    
    safe_print("\n🎉 Diagnostic complete!")

if __name__ == "__main__":
    run_comprehensive_diagnostic()
