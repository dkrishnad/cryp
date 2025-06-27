#!/usr/bin/env python3
"""
Test script to verify dashboard layout loads without errors.
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
sys.path.insert(0, dashboard_dir)

def test_layout_import():
    """Test if layout can be imported without errors"""
    try:
        print("Testing layout import...")
        from layout import layout, sidebar, tabs, notification_toast
        print("✓ Layout components imported successfully")
        
        # Check if main components exist
        if layout:
            print("✓ Main layout exists")
        else:
            print("✗ Main layout is None or empty")
            
        if sidebar:
            print("✓ Sidebar exists")
        else:
            print("✗ Sidebar is None or empty")
            
        if tabs:
            print("✓ Tabs exist")
        else:
            print("✗ Tabs are None or empty")
            
        if notification_toast:
            print("✓ Notification toast exists")
        else:
            print("✗ Notification toast is None or empty")
            
        print("\n✅ Layout test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_dash_app():
    """Test if dash app can be created"""
    try:
        print("\nTesting dash app creation...")
        from dash_app import app
        print("✓ Dash app created successfully")
        
        # Test layout assignment
        from layout import layout
        app.layout = layout
        print("✓ Layout assigned to app successfully")
        
        return True
    except Exception as e:
        print(f"✗ Dash app error: {e}")
        return False

def main():
    """Run layout tests"""
    print("=== Dashboard Layout Test ===\n")
    
    layout_ok = test_layout_import()
    app_ok = test_dash_app()
    
    if layout_ok and app_ok:
        print("\n🎉 All tests passed! Dashboard layout is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
