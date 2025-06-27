#!/usr/bin/env python3
"""
Test if the dashboard can run without duplicate callback errors
"""
import sys
import os

# Change to dashboard directory  
os.chdir('dashboard')
sys.path.insert(0, '.')

try:
    print("Testing dashboard startup...")
    
    # Import the app
    from dash_app import app
    print("✅ Dashboard app imported successfully!")
    
    # Try to access the layout
    layout = app.layout
    print("✅ Dashboard layout accessible!")
    
    # Import callbacks
    import callbacks
    print("✅ Dashboard callbacks imported successfully!")
    
    print("\n🎉 SUCCESS: All dashboard components loaded without duplicate callback errors!")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    if "duplicate" in str(e).lower():
        print("🔍 This is a duplicate callback error")
    else:
        print(f"🔍 This is a different error: {type(e).__name__}")
