#!/usr/bin/env python3
"""
Callback Error Analysis Script
This script analyzes callback execution errors in detail
"""

import sys
import os
import json
import requests
from datetime import datetime

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
            "📊": "[DASHBOARD]", "🎯": "[TARGET]", "🔍": "[TEST]", "⚡": "[CALLBACK]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def check_callback_errors():
    """Check for specific callback execution errors"""
    safe_print("🔍 Analyzing callback execution errors...")
    
    try:
        # Import app and setup
        from dash_app import app
        from layout import layout
        app.layout = layout
        import callbacks
        
        safe_print("✅ App setup complete")
        
        # Test a simple callback that should work
        safe_print("⚡ Testing account balance refresh callback...")
        
        # This is a common callback that should exist
        callback_data = {
            "inputs": [{"id": "account-refresh-interval", "property": "n_intervals", "value": 1}],
            "state": [],
            "output": "account-balance.children"
        }
        
        response = requests.post(
            "http://localhost:8050/_dash-update-component",
            json=callback_data,
            timeout=10
        )
        
        safe_print(f"📡 Callback response status: {response.status_code}")
        
        if response.status_code == 500:
            safe_print("❌ 500 Internal Server Error - analyzing...")
            safe_print(f"📄 Error response: {response.text}")
            
            # Try to get more details from the error
            if "Traceback" in response.text:
                safe_print("🐛 Found Python traceback in response")
            
            # Check if it's a specific error type
            if "ConnectionError" in response.text:
                safe_print("🔌 Likely backend connection issue")
            elif "KeyError" in response.text:
                safe_print("🔑 Likely missing key/component issue")
            elif "AttributeError" in response.text:
                safe_print("⚠️ Likely attribute/method issue")
            elif "ImportError" in response.text:
                safe_print("📦 Likely import issue")
                
        elif response.status_code == 200:
            safe_print("✅ Callback executed successfully!")
            safe_print(f"📤 Response: {response.text[:200]}...")
        else:
            safe_print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        safe_print(f"❌ Error during callback analysis: {e}")
        import traceback
        safe_print(f"Error details: {traceback.format_exc()}")

def test_backend_api_calls():
    """Test if backend API calls are working"""
    safe_print("🔍 Testing backend API calls...")
    
    backend_endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/account", "Account info"),
        ("GET", "/positions", "Positions"),
        ("GET", "/balance", "Balance")
    ]
    
    for method, endpoint, description in backend_endpoints:
        try:
            url = f"http://localhost:5000{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
                
            safe_print(f"✅ {description}: {response.status_code}")
            
            if response.status_code != 200:
                safe_print(f"   📄 Response: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            safe_print(f"❌ {description}: Backend not accessible")
        except Exception as e:
            safe_print(f"❌ {description}: {e}")

def analyze_common_callback_issues():
    """Analyze common issues that cause callback failures"""
    safe_print("🔍 Analyzing common callback issues...")
    
    try:
        # Import and check callback functions
        import callbacks
        
        # Check if there are any obvious import errors
        safe_print("✅ Callbacks module imported successfully")
        
        # Check if debug_logger is working
        try:
            from debug_logger import debugger
            safe_print("✅ Debug logger imported successfully")
        except Exception as e:
            safe_print(f"⚠️ Debug logger issue: {e}")
        
        # Check specific callback issues
        common_issues = [
            "Missing API endpoints",
            "Incorrect component IDs",
            "Backend connection failures",
            "Import errors in callback functions",
            "Circular import issues"
        ]
        
        safe_print("🎯 Common callback failure causes:")
        for issue in common_issues:
            safe_print(f"   - {issue}")
            
    except Exception as e:
        safe_print(f"❌ Error analyzing callback issues: {e}")

def run_callback_error_analysis():
    """Run comprehensive callback error analysis"""
    safe_print("🚀 Starting Callback Error Analysis...")
    safe_print("=" * 60)
    
    # Test 1: Check callback execution errors
    safe_print("\n📋 Test 1: Callback Execution Errors")
    check_callback_errors()
    
    # Test 2: Test backend API calls
    safe_print("\n📋 Test 2: Backend API Status")
    test_backend_api_calls()
    
    # Test 3: Common callback issues
    safe_print("\n📋 Test 3: Common Issues Analysis")
    analyze_common_callback_issues()
    
    safe_print("\n" + "=" * 60)
    safe_print("📊 ERROR ANALYSIS SUMMARY")
    safe_print("=" * 60)
    
    safe_print("🎯 KEY FINDINGS:")
    safe_print("1. Dashboard loads but callbacks fail with 500 errors")
    safe_print("2. This indicates callback functions are executing but failing internally")
    safe_print("3. Most likely causes: Backend API issues, import errors, or missing dependencies")
    
    safe_print("\n🔧 NEXT STEPS:")
    safe_print("1. Check backend API status and connectivity")
    safe_print("2. Review callback function implementations for errors")
    safe_print("3. Check for import or dependency issues in callback code")
    safe_print("4. Enable more detailed error logging")
    
    safe_print("\n🎉 Error analysis complete!")

if __name__ == "__main__":
    run_callback_error_analysis()
