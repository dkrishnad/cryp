#!/usr/bin/env python3
"""
Test script to verify Dash component suite fix
"""

import requests
import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def test_component_suites():
    """Test if Dash component suites are working"""
    print("🔧 Testing Dash Component Suite Fix...")
    
    base_url = "http://localhost:8050"
    
    # Test critical Dash endpoints
    test_endpoints = [
        "/_dash-layout",
        "/_dash-dependencies", 
        "/_dash-component-suites/dash/dash-renderer/build/dash_renderer.min.js"
    ]
    
    working = 0
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                working += 1
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    print(f"\n📊 Component suites working: {working}/{len(test_endpoints)}")
    
    if working == len(test_endpoints):
        print("🎉 DASH COMPONENT SUITES FIXED!")
        return True
    else:
        print("🔧 Still need more fixes")
        return False

if __name__ == "__main__":
    test_component_suites()
