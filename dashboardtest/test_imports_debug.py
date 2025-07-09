#!/usr/bin/env python3
"""
Import Test Script - Find the exact cause of the 500 error
"""
import sys
import traceback

def test_import(module_name, from_module=None):
    """Test importing a specific module and catch any errors"""
    try:
        if from_module:
            exec(f"from {from_module} import {module_name}")
            print(f"✅ Successfully imported {module_name} from {from_module}")
        else:
            exec(f"import {module_name}")
            print(f"✅ Successfully imported {module_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to import {module_name}: {e}")
        traceback.print_exc()
        return False

def main():
    print("Dashboard Import Analysis")
    print("=" * 50)
    
    # Test basic dependencies
    print("\n1. Testing basic dependencies:")
    test_import("dash")
    test_import("dash_bootstrap_components")
    test_import("plotly")
    test_import("pandas")
    test_import("requests")
    
    # Test dashboard files
    print("\n2. Testing dashboard files:")
    test_import("dash_app")
    test_import("debug_logger")
    
    # Test specific imports from callbacks
    print("\n3. Testing callback file imports:")
    try:
        # Test if we can import the callbacks file
        import callbacks
        print("✅ Successfully imported callbacks module")
    except Exception as e:
        print(f"❌ Failed to import callbacks: {e}")
        traceback.print_exc()
    
    # Test layout import
    print("\n4. Testing layout import:")
    try:
        from layout import layout
        print("✅ Successfully imported layout")
    except Exception as e:
        print(f"❌ Failed to import layout: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
