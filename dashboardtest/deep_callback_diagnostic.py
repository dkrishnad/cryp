#!/usr/bin/env python3
"""
Callback Execution Deep Diagnostic
This script identifies why callbacks aren't executing
"""

import sys
import os
import requests
import json

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
            "⚡": "[CALLBACK]", "🔍": "[TEST]", "🎯": "[TARGET]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

def examine_callback_dependencies():
    """Examine the structure of callback dependencies"""
    safe_print("🔍 Examining callback dependencies structure...")
    
    try:
        # Get dependencies
        deps_response = requests.get("http://localhost:8050/_dash-dependencies", timeout=5)
        
        if deps_response.status_code != 200:
            safe_print(f"❌ Cannot get dependencies: {deps_response.status_code}")
            return False
        
        deps_data = deps_response.json()
        safe_print(f"✅ Found {len(deps_data)} dependencies")
        
        # Examine first few dependencies to understand structure
        for i, dep in enumerate(deps_data[:5]):
            safe_print(f"\n📋 Dependency {i+1}:")
            safe_print(f"   Type: {type(dep)}")
            
            if isinstance(dep, dict):
                safe_print(f"   Keys: {list(dep.keys())}")
                if 'output' in dep:
                    safe_print(f"   Output type: {type(dep['output'])}")
                    safe_print(f"   Output: {dep['output']}")
                if 'inputs' in dep:
                    safe_print(f"   Inputs type: {type(dep['inputs'])}")
                    safe_print(f"   Inputs: {dep['inputs'][:2] if len(dep['inputs']) > 2 else dep['inputs']}")
            elif isinstance(dep, str):
                safe_print(f"   Content (first 100 chars): {dep[:100]}...")
                safe_print("   ❌ ISSUE: Dependency is a string, should be dict!")
            else:
                safe_print(f"   Content: {dep}")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Dependencies examination failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def test_simple_callback_trigger():
    """Test triggering a simple callback"""
    safe_print("🔍 Testing simple callback trigger...")
    
    try:
        # Try to trigger a simple callback by simulating a button click
        # First, let's try the account refresh button
        callback_data = {
            "inputs": [
                {"id": "refresh-account-btn", "property": "n_clicks", "value": 1}
            ],
            "state": [],
            "output": "account-info.children"
        }
        
        safe_print("⚡ Attempting to trigger account refresh callback...")
        
        response = requests.post(
            "http://localhost:8050/_dash-update-component",
            json=callback_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        safe_print(f"📡 Response status: {response.status_code}")
        safe_print(f"📡 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            safe_print("✅ Callback triggered successfully!")
            try:
                result = response.json()
                safe_print(f"📊 Result type: {type(result)}")
                safe_print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            except:
                safe_print(f"📊 Response text (first 200 chars): {response.text[:200]}")
            return True
        else:
            safe_print(f"❌ Callback failed with status {response.status_code}")
            safe_print(f"📊 Response text: {response.text[:500]}")
            return False
            
    except Exception as e:
        safe_print(f"❌ Callback trigger test failed: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")
        return False

def check_dash_app_config():
    """Check if there are issues with Dash app configuration"""
    safe_print("🔍 Checking Dash app configuration...")
    
    try:
        # Get the main page and look for configuration issues
        response = requests.get("http://localhost:8050", timeout=10)
        content = response.text
        
        # Check for common issues
        issues = []
        
        # Check if suppress_callback_exceptions is causing issues
        if "suppress_callback_exceptions" in content:
            safe_print("✅ Found suppress_callback_exceptions reference")
        else:
            safe_print("⚠️ No suppress_callback_exceptions reference found")
            
        # Check for renderer script
        if "_dash-renderer" in content:
            safe_print("✅ Dash renderer script found")
        else:
            issues.append("Dash renderer script not found")
            
        # Check for callback context
        if "callback_context" in content:
            safe_print("✅ Callback context reference found")
        else:
            safe_print("⚠️ No callback context reference found")
            
        # Check for Plotly
        if "Plotly" in content or "plotly" in content:
            safe_print("✅ Plotly references found")
        else:
            issues.append("Plotly references not found")
            
        if issues:
            safe_print("❌ Configuration issues found:")
            for issue in issues:
                safe_print(f"   - {issue}")
            return False
        else:
            safe_print("✅ Dash app configuration looks good")
            return True
            
    except Exception as e:
        safe_print(f"❌ App configuration check failed: {e}")
        return False

def test_backend_connection():
    """Test if backend is responding"""
    safe_print("🔍 Testing backend connection...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            safe_print("✅ Backend is responding")
            return True
        else:
            safe_print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        safe_print("❌ Cannot connect to backend - is it running?")
        return False
    except Exception as e:
        safe_print(f"❌ Backend test failed: {e}")
        return False

def run_deep_diagnostic():
    """Run deep callback execution diagnostic"""
    safe_print("🚀 Starting Deep Callback Execution Diagnostic...")
    safe_print("=" * 60)
    
    tests = {}
    
    # Test 1: Examine callback dependencies structure
    safe_print("\n📋 Test 1: Callback Dependencies Structure")
    tests["dependencies_structure"] = examine_callback_dependencies()
    
    # Test 2: Test simple callback trigger
    safe_print("\n📋 Test 2: Simple Callback Trigger")
    tests["callback_trigger"] = test_simple_callback_trigger()
    
    # Test 3: Check Dash app configuration
    safe_print("\n📋 Test 3: Dash App Configuration")
    tests["app_config"] = check_dash_app_config()
    
    # Test 4: Test backend connection
    safe_print("\n📋 Test 4: Backend Connection")
    tests["backend_connection"] = test_backend_connection()
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 DEEP DIAGNOSTIC SUMMARY")
    safe_print("=" * 60)
    
    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        safe_print(f"{test_name}: {status}")
    
    # Analysis
    safe_print("\n🎯 ANALYSIS:")
    if not tests["dependencies_structure"]:
        safe_print("🔧 FIX: Dependencies structure is malformed")
    if not tests["callback_trigger"]:
        safe_print("🔧 FIX: Callback triggering mechanism is broken")
    if not tests["app_config"]:
        safe_print("🔧 FIX: Dash app configuration needs adjustment")
    if not tests["backend_connection"]:
        safe_print("🔧 FIX: Backend needs to be started")
        
    safe_print("\n🎉 Deep diagnostic complete!")

if __name__ == "__main__":
    run_deep_diagnostic()
