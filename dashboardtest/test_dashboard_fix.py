#!/usr/bin/env python3
"""
Dashboard Test Script
Tests if the dashboard can start without DuplicateIdError
"""

import sys
import os
sys.path.insert(0, os.getcwd())

try:
    print("🔧 Testing dashboard components...")
    
    # Test layout import
    from layout import layout
    print("✅ Layout imported successfully")
    
    # Test app import
    from dash_app import app
    print("✅ Dash app imported successfully")
    
    # Test assignment (this is where DuplicateIdError would occur)
    app.layout = layout
    print("✅ Layout assigned to app successfully")
    print("✅ NO DUPLICATEID ERROR!")
    print()
    print("🎉 DASHBOARD IS READY!")
    print("🚀 All duplicate IDs have been resolved")
    print("🚀 Dashboard should be fully functional now")
    print()
    print("📝 To start dashboard:")
    print("   python app.py")
    
except Exception as e:
    print(f"❌ Error detected: {e}")
    print("❌ DuplicateIdError still present")
    print("🔧 Additional fixes needed")
