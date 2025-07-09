#!/usr/bin/env python3

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def test_component_integrity():
    """Test if all components referenced in callbacks exist in layout"""
    print("🔧 Testing Dashboard Component Integrity...")
    
    # Test imports
    try:
        print("📦 Testing imports...")
        from dash_app import app
        print("✅ dash_app imported successfully")
        
        import callbacks
        print("✅ callbacks imported successfully")
        
        from layout import layout
        print("✅ layout imported successfully")
        
        # Assign layout to app
        app.layout = layout
        print("✅ Layout assigned to app successfully")
        
        print("\n🎯 All core components are working correctly!")
        
        # Test that the app can be created without errors
        print("\n🧪 Testing app creation...")
        
        # This will validate that all components in callbacks have corresponding elements in layout
        app._validate_layout()
        print("✅ Layout validation passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False
    
    return True

def test_callback_components():
    """Test specific callback components"""
    print("\n🔍 Testing callback component registration...")
    
    try:
        from dash_app import app
        import callbacks
        from layout import layout
        
        app.layout = layout
        
        # Check if callbacks are properly registered
        callback_count = len(app.callback_map)
        print(f"📊 Total callbacks registered: {callback_count}")
        
        if callback_count > 0:
            print("✅ Callbacks are properly registered")
        else:
            print("⚠️ No callbacks registered - this might be an issue")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing callbacks: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_critical_components():
    """Check for critical components that must exist"""
    print("\n🔎 Checking critical components...")
    
    try:
        from layout import layout
        
        # Convert layout to string to search for component IDs
        layout_str = str(layout)
        
        critical_components = [
            'price-chart',
            'indicators-chart',
            'virtual-balance',
            'performance-monitor',
            'auto-trading-tab-content',
            'futures-trading-tab-content',
            'hybrid-learning-tab-content',
            'performance-interval',
            'balance-sync-interval'
        ]
        
        missing_components = []
        found_components = []
        
        for component in critical_components:
            if component in layout_str:
                found_components.append(component)
                print(f"✅ Found: {component}")
            else:
                missing_components.append(component)
                print(f"❌ Missing: {component}")
        
        print(f"\n📊 Summary:")
        print(f"✅ Found components: {len(found_components)}")
        print(f"❌ Missing components: {len(missing_components)}")
        
        if missing_components:
            print(f"⚠️ Missing critical components: {missing_components}")
            return False
        else:
            print("🎉 All critical components found!")
            return True
            
    except Exception as e:
        print(f"❌ Error checking components: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Dashboard Component Test...")
    
    success = True
    
    success &= test_component_integrity()
    success &= test_callback_components()
    success &= check_critical_components()
    
    if success:
        print("\n🎉 All tests passed! Dashboard should be working correctly.")
        print("💡 You can now start the dashboard with: python app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        
    print("\n" + "="*60)
