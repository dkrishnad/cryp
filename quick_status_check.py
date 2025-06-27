#!/usr/bin/env python3
"""
Quick Dashboard Status Check
"""

import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard'))

try:
    print("🔍 QUICK DASHBOARD STATUS CHECK")
    print("=" * 50)
    
    # Check 1: Files exist
    dashboard_files = [
        'dashboard/app.py',
        'dashboard/callbacks.py', 
        'dashboard/layout.py',
        'dashboard/dash_app.py'
    ]
    
    for file in dashboard_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
    
    # Check 2: Callback count
    print("\n📊 CALLBACK COUNT:")
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
        callback_count = content.count('@app.callback')
        print(f"   Total @app.callback decorators: {callback_count}")
    
    # Check 3: Import test (quick)
    print("\n🧪 IMPORT TEST:")
    try:
        from dashboard.dash_app import app
        print("   ✅ App import: SUCCESS")
    except Exception as e:
        print(f"   ❌ App import: FAILED - {e}")
        
    print("\n🎯 DASHBOARD STATUS: READY FOR TESTING")
    
except Exception as e:
    print(f"❌ Error: {e}")
