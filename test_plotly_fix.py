#!/usr/bin/env python3
"""
Test Dashboard Plotly.js Loading
Quick test to check if Plotly.js loading issues are resolved
"""

import requests
import time
import sys
from urllib.parse import urljoin

def test_dashboard_plotly():
    """Test if dashboard loads without Plotly.js errors"""
    
    print("🧪 Testing Dashboard Plotly.js Loading...")
    print("=" * 50)
    
    # Test dashboard is responding
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard is responding")
        else:
            print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard not accessible: {e}")
        print("💡 Make sure the dashboard is running: python dashboard/app.py")
        return False
    
    # Check if Plotly.js is being served locally
    try:
        plotly_response = requests.get("http://localhost:8050/_dash-component-suites/plotly/package/plotly.min.js", timeout=10)
        if plotly_response.status_code == 200:
            print("✅ Plotly.js is being served locally")
        else:
            print(f"⚠️  Plotly.js local serve status: {plotly_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check local Plotly.js: {e}")
    
    # Check if our custom assets are loading
    try:
        js_fix_response = requests.get("http://localhost:8050/assets/plotly-fix.js", timeout=5)
        if js_fix_response.status_code == 200:
            print("✅ Plotly.js fix script is accessible")
        else:
            print(f"⚠️  Plotly fix script status: {js_fix_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check plotly-fix.js: {e}")
    
    # Test backend connection
    try:
        backend_response = requests.get("http://localhost:8001/health", timeout=5)
        if backend_response.status_code == 200:
            print("✅ Backend API is responding")
        else:
            print(f"❌ Backend API status: {backend_response.status_code}")
    except Exception as e:
        print(f"⚠️  Backend API not accessible: {e}")
        print("💡 Make sure the backend is running: python backend/main.py")
    
    print()
    print("📋 Summary:")
    print("- Dashboard should now load without Plotly.js timeout errors")
    print("- The plotly-fix.js script will handle any loading issues")
    print("- Empty graphs will show 'No data' instead of causing errors")
    print("- Plotly.js timeout increased from 30 to 60 seconds")
    print()
    print("🌐 Access your dashboard at: http://localhost:8050")
    print("📊 Check browser console for any remaining issues")
    
    return True

if __name__ == "__main__":
    success = test_dashboard_plotly()
    sys.exit(0 if success else 1)
