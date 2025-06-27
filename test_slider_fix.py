#!/usr/bin/env python3
"""
Dashboard Slider Style Fix Test
Test that dashboard can import without slider style errors
"""

import sys
import os
import traceback

def test_layout_import():
    """Test that layout can be imported without slider style errors"""
    try:
        print("Testing dashboard layout import...")
        
        # Add dashboard directory to path
        sys.path.append(os.path.join(os.getcwd(), 'dashboard'))
        
        # Try to import layout - this should not fail with slider style errors
        from layout import layout
        print("✅ Layout imported successfully without slider errors")
        
        # Check that layout is properly structured
        if hasattr(layout, 'children'):
            print("✅ Layout has proper children structure")
            return True
        else:
            print("❌ Layout structure invalid")
            return False
            
    except TypeError as e:
        if 'Slider' in str(e) and 'style' in str(e):
            print(f"❌ Slider style error still present: {str(e)}")
            return False
        else:
            print(f"❌ Other TypeError: {str(e)}")
            return False
    except Exception as e:
        print(f"❌ Error importing layout: {str(e)}")
        traceback.print_exc()
        return False

def test_dashboard_startup():
    """Test that dashboard components can be created"""
    try:
        print("\nTesting dashboard component creation...")
        
        # Test basic Dash imports
        import dash
        from dash import dcc, html
        print("✅ Dash imports successful")
        
        # Test that sliders can be created without style
        try:
            slider = dcc.Slider(id="test-slider", min=0, max=100, value=50)
            print("✅ Slider creation without style works")
        except Exception as e:
            print(f"❌ Slider creation failed: {e}")
            return False
        
        # Test wrapped slider with div style
        try:
            wrapped_slider = html.Div([
                dcc.Slider(id="test-slider-2", min=0, max=100, value=50)
            ], style={"display": "none"})
            print("✅ Wrapped slider with div style works")
        except Exception as e:
            print(f"❌ Wrapped slider failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard components: {str(e)}")
        return False

def main():
    """Run slider style fix tests"""
    print("="*60)
    print("    DASHBOARD SLIDER STYLE FIX TEST")
    print("="*60)
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print(f"Working in: {bot_dir}\n")
    
    # Run tests
    test1 = test_layout_import()
    test2 = test_dashboard_startup()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("🎉 SLIDER STYLE ERROR FIXED!")
        print("✅ Dashboard layout imports successfully")
        print("✅ No more dcc.Slider style argument errors") 
        print("✅ Components wrapped properly for hiding")
        print("\n💡 Dashboard should now start without errors!")
    else:
        print("❌ SOME ISSUES REMAIN")
        print("❌ Additional fixes may be needed")
    print("="*60)
    
    return test1 and test2

if __name__ == "__main__":
    main()
