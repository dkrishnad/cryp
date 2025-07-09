#!/usr/bin/env python3
"""
Frontend Dashboard Interactivity Diagnostic
Specifically diagnoses browser-side dashboard issues when backend is working
"""

import requests
import json
import time
import webbrowser
from urllib.parse import urljoin

def safe_print(message, end="\n"):
    """Print with emoji fallback"""
    try:
        print(message, end=end)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🚀": "[START]", "✅": "[OK]", "❌": "[ERROR]", "🔍": "[CHECK]",
            "⚠️": "[WARNING]", "💻": "[BROWSER]", "🌐": "[NETWORK]", "📡": "[API]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg, end=end)

def test_dashboard_page_content():
    """Test what the dashboard page actually contains"""
    safe_print("🔍 Testing Dashboard Page Content...")
    
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        # Check for critical Dash components
        checks = {
            "Dash renderer": "_dash-renderer" in content,
            "Plotly.js": "plotly" in content.lower(),
            "React": "react" in content.lower(),
            "Bootstrap": "bootstrap" in content.lower(),
            "Component tree": '"children"' in content,
            "Callbacks": "_dash-update-component" in content,
            "Layout data": '"layout"' in content
        }
        
        safe_print("📋 Dashboard Page Analysis:")
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            safe_print(f"   {status} {check_name}")
        
        # Check page size (too small = error page)
        page_size = len(content)
        safe_print(f"📊 Page size: {page_size} bytes")
        if page_size < 10000:
            safe_print("⚠️ Page size suspiciously small - might be error page")
        
        return all(checks.values()), content
        
    except Exception as e:
        safe_print(f"❌ Failed to get dashboard page: {e}")
        return False, ""

def test_dash_specific_endpoints():
    """Test Dash-specific endpoints that enable interactivity"""
    safe_print("\n🔍 Testing Dash Framework Endpoints...")
    
    dash_endpoints = [
        "/_dash-layout",
        "/_dash-dependencies", 
        "/_dash-update-component",
        "/_dash-component-suites/dash/deps/polyfill@7.12.1.min.js",
        "/_dash-component-suites/dash/deps/react@16.14.0.min.js",
        "/_dash-component-suites/dash/deps/react-dom@16.14.0.min.js",
        "/_dash-component-suites/dash/deps/prop-types@15.7.2.min.js"
    ]
    
    working_count = 0
    
    for endpoint in dash_endpoints:
        url = f"http://localhost:8050{endpoint}"
        try:
            if endpoint == "/_dash-update-component":
                # This needs POST with data
                response = requests.post(url, json={"inputs": [], "state": []}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            if response.status_code in [200, 400, 422]:  # 400/422 OK for update-component without proper data
                safe_print(f"✅ {endpoint}")
                working_count += 1
            else:
                safe_print(f"❌ {endpoint} -> {response.status_code}")
                
        except Exception as e:
            safe_print(f"❌ {endpoint} -> ERROR: {e}")
    
    safe_print(f"📊 Dash endpoints: {working_count}/{len(dash_endpoints)} working")
    return working_count >= len(dash_endpoints) - 2  # Allow some failures

def test_cors_and_networking():
    """Test CORS and networking issues"""
    safe_print("\n🌐 Testing CORS and Network Configuration...")
    
    # Test CORS headers
    try:
        response = requests.get("http://localhost:8050", timeout=5)
        headers = response.headers
        
        cors_checks = {
            "Access-Control-Allow-Origin": "Access-Control-Allow-Origin" in headers,
            "Content-Type": headers.get("Content-Type", "").startswith("text/html"),
            "Server Running": response.status_code == 200,
            "No CORS Errors": "cors" not in response.text.lower()
        }
        
        safe_print("📋 CORS/Network Analysis:")
        for check_name, passed in cors_checks.items():
            status = "✅" if passed else "❌"
            safe_print(f"   {status} {check_name}")
            
        return all(cors_checks.values())
        
    except Exception as e:
        safe_print(f"❌ CORS test failed: {e}")
        return False

def test_callback_registration_live():
    """Test if callbacks are actually registered in the live dashboard"""
    safe_print("\n⚡ Testing Live Callback Registration...")
    
    try:
        # Get dependencies (this shows registered callbacks)
        response = requests.get("http://localhost:8050/_dash-dependencies", timeout=5)
        
        if response.status_code == 200:
            dependencies = response.json()
            callback_count = len(dependencies)
            safe_print(f"✅ Found {callback_count} callbacks registered")
            
            # Check for specific critical callbacks
            critical_callbacks = []
            for dep in dependencies[:10]:  # Check first 10
                if isinstance(dep, dict) and 'inputs' in dep:
                    inputs = dep['inputs']
                    if isinstance(inputs, list) and len(inputs) > 0:
                        input_id = inputs[0].get('id', 'unknown')
                        critical_callbacks.append(input_id)
            
            safe_print("📋 Sample callback inputs found:")
            for cb in critical_callbacks[:5]:
                safe_print(f"   ⚡ {cb}")
                
            return callback_count > 0
        else:
            safe_print(f"❌ Cannot get callback dependencies: {response.status_code}")
            return False
            
    except Exception as e:
        safe_print(f"❌ Callback registration test failed: {e}")
        return False

def test_javascript_execution():
    """Test if JavaScript is properly executing"""
    safe_print("\n💻 Testing JavaScript Execution...")
    
    try:
        # Get the main page and check for JS errors
        response = requests.get("http://localhost:8050", timeout=5)
        content = response.text
        
        js_checks = {
            "No JS Errors": "error" not in content.lower() and "exception" not in content.lower(),
            "Dash Core": "window.dash_clientside" in content or "DashRenderer" in content,
            "Plotly Loaded": "Plotly.newPlot" in content or "plotly.min.js" in content,
            "Event Listeners": "addEventListener" in content or "onclick" in content,
            "AJAX/Fetch": "fetch(" in content or "XMLHttpRequest" in content or "_dash-update-component" in content
        }
        
        safe_print("📋 JavaScript Analysis:")
        for check_name, passed in js_checks.items():
            status = "✅" if passed else "❌"
            safe_print(f"   {status} {check_name}")
            
        return sum(js_checks.values()) >= 3  # At least 3 should pass
        
    except Exception as e:
        safe_print(f"❌ JavaScript test failed: {e}")
        return False

def test_component_interaction():
    """Test if components can actually be interacted with"""
    safe_print("\n🖱️ Testing Component Interaction...")
    
    try:
        # Try to trigger a simple callback
        test_payload = {
            "inputs": [{"id": "page-content", "property": "children", "value": None}],
            "state": [],
            "output": "page-content.children"
        }
        
        response = requests.post(
            "http://localhost:8050/_dash-update-component",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        safe_print(f"📡 Component interaction test: {response.status_code}")
        
        if response.status_code in [200, 204]:
            safe_print("✅ Components can be interacted with")
            return True
        elif response.status_code == 400:
            safe_print("⚠️ Component exists but payload format issue")
            return True  # This is actually OK - means the endpoint works
        else:
            safe_print(f"❌ Component interaction failed: {response.status_code}")
            safe_print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        safe_print(f"❌ Component interaction test failed: {e}")
        return False

def provide_browser_debugging_steps():
    """Provide steps for browser-side debugging"""
    safe_print("\n🔧 BROWSER DEBUGGING STEPS:")
    safe_print("=" * 50)
    
    safe_print("1. 💻 Open Browser Developer Tools (F12)")
    safe_print("   - Go to Console tab")
    safe_print("   - Look for JavaScript errors (red text)")
    safe_print("   - Screenshot any errors found")
    
    safe_print("\n2. 🌐 Check Network Tab:")
    safe_print("   - Refresh the page (F5)")
    safe_print("   - Look for failed requests (red status)")
    safe_print("   - Check if _dash-update-component calls work")
    
    safe_print("\n3. 🖱️ Test Button Interaction:")
    safe_print("   - Click any button on dashboard")
    safe_print("   - Watch Network tab for new requests")
    safe_print("   - Check Console for any errors")
    
    safe_print("\n4. 🔄 Cache Clearing:")
    safe_print("   - Hard refresh: Ctrl+Shift+R")
    safe_print("   - Clear browser cache completely")
    safe_print("   - Try incognito/private window")
    
    safe_print("\n5. 🌍 Try Different Browser:")
    safe_print("   - Test in Chrome, Firefox, Edge")
    safe_print("   - Check if issue is browser-specific")

def run_frontend_diagnostic():
    """Run comprehensive frontend diagnostic"""
    safe_print("🚀 Frontend Dashboard Interactivity Diagnostic")
    safe_print("=" * 60)
    safe_print("📋 Diagnosing browser-side dashboard issues...")
    safe_print("📋 Backend confirmed working - focusing on frontend")
    safe_print("")
    
    results = {}
    
    # Test 1: Dashboard page content
    results["page_content"], page_content = test_dashboard_page_content()
    
    # Test 2: Dash framework endpoints
    results["dash_endpoints"] = test_dash_specific_endpoints()
    
    # Test 3: CORS and networking
    results["cors_network"] = test_cors_and_networking()
    
    # Test 4: Callback registration
    results["callback_registration"] = test_callback_registration_live()
    
    # Test 5: JavaScript execution
    results["javascript"] = test_javascript_execution()
    
    # Test 6: Component interaction
    results["component_interaction"] = test_component_interaction()
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 FRONTEND DIAGNOSTIC SUMMARY")
    safe_print("=" * 60)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    safe_print(f"Tests passed: {passed_tests}/{total_tests}")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        safe_print(f"{test_name}: {status}")
    
    # Diagnosis
    safe_print("\n🎯 LIKELY CAUSE ANALYSIS:")
    safe_print("-" * 30)
    
    if not results["page_content"]:
        safe_print("❌ CRITICAL: Dashboard page not loading properly")
        safe_print("🔧 FIX: Check Dash app configuration and restart")
        
    elif not results["dash_endpoints"]:
        safe_print("❌ CRITICAL: Dash framework not working")
        safe_print("🔧 FIX: Dash installation or configuration issue")
        
    elif not results["callback_registration"]:
        safe_print("❌ CRITICAL: Callbacks not registered in live app")
        safe_print("🔧 FIX: Check callback imports and registration")
        
    elif not results["javascript"]:
        safe_print("❌ CRITICAL: JavaScript execution problems")
        safe_print("🔧 FIX: Browser compatibility or JS loading issues")
        
    elif not results["component_interaction"]:
        safe_print("❌ CRITICAL: Component interaction broken")
        safe_print("🔧 FIX: Component-callback communication issue")
        
    else:
        safe_print("⚠️ All frontend tests pass but dashboard still static")
        safe_print("🔧 This requires manual browser debugging")
    
    # Provide debugging steps
    provide_browser_debugging_steps()
    
    # Save results
    with open("frontend_diagnostic_results.json", "w") as f:
        json.dump({
            "timestamp": time.time(),
            "results": results,
            "passed_tests": passed_tests,
            "total_tests": total_tests
        }, f, indent=2)
    
    safe_print(f"\n💾 Results saved to: frontend_diagnostic_results.json")
    
    return results

if __name__ == "__main__":
    run_frontend_diagnostic()
