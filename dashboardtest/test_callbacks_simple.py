#!/usr/bin/env python3
"""Simple test to verify callbacks work"""

try:
    from callbacks import app
    print("✅ Callbacks loaded successfully")
    
    # Check if we can access the app
    print(f"✅ App object: {type(app)}")
    
    # Try importing layout
    from layout import layout
    print("✅ Layout loaded successfully")
    
    print("\n=== TESTING BUTTON FUNCTIONALITY ===")
    
    # Test if the backend is running
    import requests
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and responding")
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
    except:
        print("❌ Backend is not running")
    
    print("\n=== NEXT STEPS ===")
    print("1. Start the backend if not running")
    print("2. Start the dashboard: python app.py")
    print("3. Test buttons in the browser")
    
except Exception as e:
    print(f"❌ Error loading callbacks: {e}")
    import traceback
    traceback.print_exc()
