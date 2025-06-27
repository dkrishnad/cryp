#!/usr/bin/env python3
"""
Test script to verify main.py imports successfully from project root
"""

print("Testing backend/main.py import from project root...")

try:
    from backend.main import app
    print("✅ SUCCESS: backend/main.py imports successfully from project root!")
    print(f"✅ FastAPI app created: {type(app)}")
    
    # Test basic functionality
    print("✅ App routes available:", len(app.routes))
    print("✅ Main import issue FIXED!")
    
except ImportError as e:
    print(f"❌ FAILED: Import error - {e}")
except Exception as e:
    print(f"❌ FAILED: Other error - {e}")

print("\nTesting dashboard import...")
try:
    from dashboard.dash_app import app as dash_app
    print("✅ SUCCESS: dashboard/dash_app.py imports successfully!")
    print(f"✅ Dash app created: {type(dash_app)}")
except ImportError as e:
    print(f"❌ FAILED: Dashboard import error - {e}")
except Exception as e:
    print(f"❌ FAILED: Dashboard error - {e}")

print("\n🎉 ALL IMPORT TESTS COMPLETE!")
