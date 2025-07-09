#!/usr/bin/env python3
"""
Test actual callback execution to find why dashboard is static
"""

import sys
import os
import json
import requests
import time

# Windows-specific encoding setup
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

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

def test_callback_simulation():
    """Test actual callback execution by simulating button clicks"""
    safe_print("🔍 Testing actual callback execution...")
    
    try:
        # Get dependencies to find callbacks
        deps_response = requests.get("http://localhost:8050/_dash-dependencies", timeout=10)
        if deps_response.status_code != 200:
            safe_print(f"❌ Cannot get dependencies: {deps_response.status_code}")
            return False
        
        deps_data = deps_response.json()
        safe_print(f"✅ Found {len(deps_data)} callback dependencies")
        
        # Look for simple button callbacks
        button_callbacks = []
        for i, dep in enumerate(deps_data):
            if 'inputs' in dep and dep['inputs']:
                for input_item in dep['inputs']:
                    if isinstance(input_item, dict) and input_item.get('property') == 'n_clicks':
                        button_callbacks.append({
                            'index': i,
                            'input_id': input_item.get('id'),
                            'output_id': dep.get('output', {}).get('id'),
                            'output_property': dep.get('output', {}).get('property'),
                            'dependency': dep
                        })
        
        safe_print(f"⚡ Found {len(button_callbacks)} button callbacks")
        
        if not button_callbacks:
            safe_print("❌ No button callbacks found to test")
            return False
        
        # Test the first few button callbacks
        test_count = min(5, len(button_callbacks))
        successful_tests = 0
        
        for i in range(test_count):
            callback = button_callbacks[i]
            safe_print(f"\n🔍 Testing callback {i+1}: {callback['input_id']}")
            
            # Prepare callback payload
            payload = {
                "inputs": [
                    {
                        "id": callback['input_id'],
                        "property": "n_clicks",
                        "value": 1
                    }
                ],
                "state": [],
                "output": f"{callback['output_id']}.{callback['output_property']}"
            }
            
            safe_print(f"📤 Sending payload: {json.dumps(payload, indent=2)}")
            
            # Make the callback request
            response = requests.post(
                "http://localhost:8050/_dash-update-component",
                json=payload,
                timeout=30,
                headers={
                    'Content-Type': 'application/json',
                    'X-CSRFToken': 'fake'  # Some Dash apps require this
                }
            )
            
            safe_print(f"📥 Response status: {response.status_code}")
            safe_print(f"📥 Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    safe_print(f"✅ Callback executed successfully!")
                    safe_print(f"📊 Response data: {json.dumps(response_data, indent=2)}")
                    successful_tests += 1
                except json.JSONDecodeError:
                    safe_print(f"⚠️ Response not JSON: {response.text[:200]}...")
            else:
                safe_print(f"❌ Callback failed with status {response.status_code}")
                safe_print(f"📄 Response: {response.text[:500]}...")
        
        safe_print(f"\n📊 Summary: {successful_tests}/{test_count} callbacks executed successfully")
        return successful_tests > 0
        
    except Exception as e:
        safe_print(f"❌ Callback simulation failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_websocket_connection():
    """Test if WebSocket connection is working"""
    safe_print("🔍 Testing WebSocket connection...")
    
    try:
        # Check if there are WebSocket endpoints
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        if "_dash-renderer" in content:
            safe_print("✅ Dash renderer script found in page")
        else:
            safe_print("❌ Dash renderer script not found")
            return False
        
        if "ws://" in content or "wss://" in content:
            safe_print("✅ WebSocket connection setup found")
        else:
            safe_print("⚠️ No WebSocket setup found in page source")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ WebSocket test failed: {e}")
        return False

def test_plotly_js_loading():
    """Test if Plotly.js is loading correctly"""
    safe_print("🔍 Testing Plotly.js loading...")
    
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        # Check for Plotly script tags
        if "plotly" in content.lower():
            safe_print("✅ Plotly reference found in page")
        else:
            safe_print("❌ No Plotly reference found")
            return False
        
        # Check for plot containers
        if 'id="' in content and 'plot' in content.lower():
            safe_print("✅ Plot containers found in page")
        else:
            safe_print("⚠️ No plot containers found")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Plotly.js test failed: {e}")
        return False

def test_browser_console_simulation():
    """Simulate browser console issues"""
    safe_print("🔍 Testing for browser console issues...")
    
    try:
        # Check the page source for common issues
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        issues = []
        
        # Check for JavaScript errors patterns
        error_patterns = [
            "error", "Error", "ERROR",
            "undefined", "null is not",
            "cannot read property",
            "is not a function"
        ]
        
        for pattern in error_patterns:
            if pattern in content:
                issues.append(f"Potential JS error pattern: {pattern}")
        
        # Check for missing resources
        if "404" in content:
            issues.append("404 errors found in page")
        
        if "500" in content:
            issues.append("500 errors found in page")
        
        if issues:
            safe_print("⚠️ Potential browser console issues:")
            for issue in issues:
                safe_print(f"   - {issue}")
            return False
        else:
            safe_print("✅ No obvious browser console issues detected")
            return True
        
    except Exception as e:
        safe_print(f"❌ Browser console test failed: {e}")
        return False

def run_execution_tests():
    """Run all callback execution tests"""
    safe_print("🚀 Starting Callback Execution Tests...")
    safe_print("=" * 60)
    
    results = {
        "callback_simulation": test_callback_simulation(),
        "websocket_connection": test_websocket_connection(),
        "plotly_js_loading": test_plotly_js_loading(),
        "browser_console": test_browser_console_simulation()
    }
    
    safe_print("\n" + "=" * 60)
    safe_print("📊 EXECUTION TEST SUMMARY")
    safe_print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        safe_print(f"{test_name}: {status}")
    
    # Analysis
    safe_print("\n🔧 ANALYSIS:")
    if not results["callback_simulation"]:
        safe_print("🎯 MAIN ISSUE: Callbacks are not executing when triggered!")
        safe_print("   This explains why the dashboard appears static.")
    
    if not results["websocket_connection"]:
        safe_print("🎯 ISSUE: WebSocket connection problems may prevent real-time updates")
    
    if not results["plotly_js_loading"]:
        safe_print("🎯 ISSUE: Plotly.js loading problems may prevent chart interactivity")
    
    if not results["browser_console"]:
        safe_print("🎯 ISSUE: Browser console errors may block JavaScript execution")
    
    safe_print("\n🎉 Execution diagnostic complete!")
    return results

if __name__ == "__main__":
    run_execution_tests()
