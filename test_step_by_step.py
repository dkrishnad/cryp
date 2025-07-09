#!/usr/bin/env python3
"""
Test callbacks one by one to find the problematic one
"""
import sys
import os
import traceback

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

def test_imports_only():
    """Test just the imports without callbacks"""
    try:
        safe_print("🔧 Testing dash_app import...")
        from dashboardtest.dash_app import app
        safe_print("✅ dash_app imported")
        
        safe_print("🔧 Testing layout import...")
        from dashboardtest.layout import layout
        safe_print("✅ layout imported")
        
        safe_print("🔧 Setting layout...")
        app.layout = layout
        safe_print("✅ layout set")
        
        safe_print("🔧 Testing app configuration...")
        safe_print(f"App instance: {type(app)}")
        safe_print(f"Layout type: {type(layout)}")
        safe_print(f"Callbacks count: {len(app.callback_map)}")
        
        safe_print("✅ All imports successful - NO CALLBACKS LOADED")
        return True
        
    except Exception as e:
        safe_print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_with_callbacks():
    """Test with callbacks - this is where it might hang"""
    try:
        safe_print("🔧 Importing callbacks (this may hang)...")
        
        # Set a timeout or test individually
        import dashboardtest.callbacks
        
        safe_print("✅ Callbacks imported successfully")
        return True
        
    except Exception as e:
        safe_print(f"❌ Callback import error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    safe_print("🔍 Testing Dashboard Components Step by Step...")
    safe_print("=" * 60)
    
    # Test 1: Imports only
    safe_print("\n🧪 Test 1: Imports without callbacks")
    if not test_imports_only():
        safe_print("❌ Basic imports failed")
        return
    
    # Test 2: With callbacks
    safe_print("\n🧪 Test 2: Import callbacks (potential hang point)")
    if not test_with_callbacks():
        safe_print("❌ Callbacks import failed")
        return
    
    safe_print("\n✅ All tests passed!")

if __name__ == "__main__":
    main()
