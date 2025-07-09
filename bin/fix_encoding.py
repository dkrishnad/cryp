#!/usr/bin/env python3
"""
Fix encoding issues in dashboard files for Windows compatibility
"""
import os
import sys

def fix_encoding_for_windows():
    """Apply encoding fixes for Windows"""
    
    # Set environment variables for UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = '1'
    
    # Try to set console to UTF-8 mode
    if os.name == 'nt':
        try:
            # Windows 10 version 1903+ supports UTF-8 mode
            import subprocess
            subprocess.run('chcp 65001', shell=True, capture_output=True)
        except:
            pass
    
    print("Encoding fixes applied for Windows compatibility")

def test_dashboard_startup():
    """Test if dashboard can start without encoding errors"""
    
    print("Testing dashboard startup...")
    
    # Apply encoding fixes
    fix_encoding_for_windows()
    
    try:
        # Test basic imports
        import dash
        import dash_bootstrap_components as dbc
        print("✓ Basic imports successful")
        
        # Test layout import
        sys.path.insert(0, 'dashboard')
        from layout import layout
        print("✓ Layout import successful")
        
        # Test app creation
        app = dash.Dash(__name__, suppress_callback_exceptions=True)
        app.layout = layout
        print("✓ App creation successful")
        
        print("✓ Dashboard startup test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Dashboard startup test failed: {e}")
        return False

if __name__ == "__main__":
    if test_dashboard_startup():
        print("Dashboard is ready to start!")
    else:
        print("Dashboard needs fixes before starting")
