#!/usr/bin/env python3
"""
Test script to check dashboard imports
"""
import sys
import traceback

def test_imports():
    """Test importing dashboard components"""
    try:
        print("Testing dash_app import...")
        from dash_app import app
        print("✅ dash_app imported successfully")
        
        print("Testing layout import...")
        from layout import layout
        print("✅ layout imported successfully")
        
        print("Testing callbacks import...")
        import callbacks
        print("✅ callbacks imported successfully")
        
        print("Testing app layout assignment...")
        app.layout = layout
        print("✅ app layout assigned successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
