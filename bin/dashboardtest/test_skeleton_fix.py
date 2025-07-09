#!/usr/bin/env python3
"""
Test backend connectivity and fix skeleton dashboard
"""
import requests
import time
import json

def test_backend_connection():
    """Test if backend is responding"""
    print("🔍 Testing Backend Connection...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy!")
            
            # Test a data endpoint
            response = requests.get("http://localhost:8000/features/indicators?symbol=btcusdt", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend data endpoints working!")
                print(f"   Sample data: RSI={data.get('rsi', 'N/A')}")
                return True
            else:
                print(f"⚠️ Data endpoint failed: {response.status_code}")
                return False
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running or not accessible on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_dashboard_startup():
    """Test dashboard startup without backend dependency"""
    print("\n🎨 Testing Dashboard Startup...")
    
    try:
        import sys
        import os
        
        # Add dashboard directory to path
        dashboard_dir = os.path.dirname(os.path.abspath(__file__))
        if dashboard_dir not in sys.path:
            sys.path.insert(0, dashboard_dir)
        
        from dash_app import app
        import callbacks
        from layout import layout
        
        app.layout = layout
        
        print("✅ Dashboard components loaded successfully")
        print(f"✅ {len(app.callback_map)} callbacks registered")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard startup error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_mock_backend():
    """Create a simple mock backend for testing"""
    print("\n🔧 Creating Mock Backend for Testing...")
    
    try:
        from flask import Flask, jsonify
        import threading
        import random
        
        mock_app = Flask(__name__)
        
        @mock_app.route('/health')
        def health():
            return jsonify({"status": "ok"})
        
        @mock_app.route('/price/<symbol>')
        def get_price(symbol):
            return jsonify({
                "symbol": symbol.upper(),
                "price": random.uniform(30000, 50000),
                "change_24h": random.uniform(-5, 5)
            })
        
        @mock_app.route('/features/indicators')
        def get_indicators():
            return jsonify({
                "rsi": random.uniform(30, 70),
                "macd": random.uniform(-100, 100),
                "sma_20": random.uniform(30000, 50000),
                "ema_12": random.uniform(30000, 50000)
            })
        
        def run_mock():
            mock_app.run(host='localhost', port=8001, debug=False)
        
        # Start mock backend in thread
        mock_thread = threading.Thread(target=run_mock, daemon=True)
        mock_thread.start()
        
        time.sleep(2)  # Give it time to start
        
        # Test mock backend
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Mock backend running on port 8001")
            return True
        else:
            print("❌ Mock backend failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Mock backend error: {e}")
        return False

def diagnose_skeleton_root_cause():
    """Diagnose the root cause of skeleton dashboard"""
    print("=" * 60)
    print("🩺 SKELETON DASHBOARD ROOT CAUSE ANALYSIS")
    print("=" * 60)
    
    # Test 1: Backend connectivity
    backend_ok = test_backend_connection()
    
    # Test 2: Dashboard startup
    dashboard_ok = test_dashboard_startup()
    
    print("\n" + "=" * 60)
    print("📋 DIAGNOSIS RESULTS")
    print("=" * 60)
    
    if not backend_ok and dashboard_ok:
        print("🎯 ROOT CAUSE IDENTIFIED:")
        print("   The dashboard is properly configured but the BACKEND IS NOT RUNNING")
        print("   or not accessible on http://localhost:8000")
        print()
        print("🔧 SOLUTION:")
        print("   1. Start the backend server first:")
        print("      cd backendtest && python main.py")
        print("   2. Then start the dashboard:")
        print("      cd dashboardtest && python app.py")
        print("   3. Or use the system launcher:")
        print("      python start_system.py")
        
        return "backend_not_running"
        
    elif not dashboard_ok:
        print("🎯 ROOT CAUSE IDENTIFIED:")
        print("   Dashboard has configuration or import issues")
        print()
        print("🔧 SOLUTION:")
        print("   Check dashboard imports and callback configurations")
        
        return "dashboard_config_error"
        
    elif backend_ok and dashboard_ok:
        print("✅ BOTH BACKEND AND DASHBOARD ARE WORKING")
        print("💡 The skeleton issue might be due to:")
        print("   - Browser caching (try Ctrl+F5)")
        print("   - Network connectivity between frontend and backend")
        print("   - CSS/JS assets not loading")
        
        return "other_issue"
        
    else:
        print("❌ BOTH BACKEND AND DASHBOARD HAVE ISSUES")
        print("🔧 Fix both backend and dashboard issues")
        
        return "both_broken"

if __name__ == "__main__":
    root_cause = diagnose_skeleton_root_cause()
    
    if root_cause == "backend_not_running":
        print("\n🚨 IMMEDIATE ACTION NEEDED:")
        print("   The dashboard skeleton issue is caused by the backend not running.")
        print("   Start the backend first to see real data in the dashboard!")
        
    print("\n" + "=" * 60)
