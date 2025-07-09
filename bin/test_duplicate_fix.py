#!/usr/bin/env python3
"""
Test script to verify the duplicate callback outputs fix
"""

import sys
import os
import traceback

def test_dashboard_imports():
    """Test that dashboard can be imported without callback conflicts"""
    try:
        print("Testing dashboard imports...")
        
        # Test basic imports
        import dash
        from dash import dcc, html, Input, Output, State, callback_context
        print("✅ Basic Dash imports successful")
        
        # Test email layout import
        sys.path.append(os.path.join(os.getcwd(), 'dashboard'))
        from email_config_layout import create_email_config_layout, register_email_config_callbacks
        print("✅ Email config layout imports successful")
        
        # Test callbacks import
        print("Testing callbacks.py import...")
        import dashboard.callbacks
        print("✅ Dashboard callbacks imported successfully")
        
        # Try to create a basic app and register callbacks
        print("Testing callback registration...")
        app = dash.Dash(__name__)
        
        # This should work without duplicate callback errors
        register_email_config_callbacks(app)
        print("✅ Email config callbacks registered successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during import test: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def test_email_layout():
    """Test that email layout can be created"""
    try:
        print("\nTesting email layout creation...")
        sys.path.append(os.path.join(os.getcwd(), 'dashboard'))
        from email_config_layout import create_email_config_layout
        
        layout = create_email_config_layout()
        print("✅ Email configuration layout created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating email layout: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("    DUPLICATE CALLBACK OUTPUTS FIX TEST")
    print("="*60)
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print(f"Working in: {bot_dir}\n")
    
    # Run tests
    test1 = test_dashboard_imports()
    test2 = test_email_layout()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Duplicate callback outputs error should be FIXED")
        print("✅ Dashboard should launch without callback conflicts")
    else:
        print("❌ SOME TESTS FAILED")
        print("❌ Additional fixes may be needed")
    print("="*60)
    
    return test1 and test2

if __name__ == "__main__":
    main()
