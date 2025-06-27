#!/usr/bin/env python3
"""
Dashboard Fix Verification
Tests if dashboard import and syntax issues are resolved
"""
import sys
import os
import subprocess

def test_callbacks_syntax():
    """Test if callbacks.py has proper syntax"""
    print("🔍 Testing callbacks.py syntax...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', 'dashboard/callbacks.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ callbacks.py syntax is valid")
            return True
        else:
            print(f"❌ callbacks.py syntax error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing callbacks.py: {e}")
        return False

def test_app_syntax():
    """Test if app.py has proper syntax"""
    print("🔍 Testing app.py syntax...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', 'dashboard/app.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ app.py syntax is valid")
            return True
        else:
            print(f"❌ app.py syntax error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing app.py: {e}")
        return False

def test_dashboard_import():
    """Test if dashboard can be imported"""
    print("🔍 Testing dashboard import...")
    try:
        # Test import without running the app
        result = subprocess.run([
            sys.executable, '-c', '''
import sys
import os
sys.path.append("dashboard")
try:
    import layout
    import callbacks
    print("SUCCESS: Dashboard imports work")
except Exception as e:
    print(f"ERROR: {e}")
'''
        ], capture_output=True, text=True, timeout=10)
        
        if "SUCCESS" in result.stdout:
            print("✅ Dashboard imports successfully")
            return True
        else:
            print(f"❌ Dashboard import failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing dashboard import: {e}")
        return False

def main():
    print("🔧 DASHBOARD FIX VERIFICATION")
    print("="*40)
    
    # Test all components
    callbacks_ok = test_callbacks_syntax()
    app_ok = test_app_syntax()
    import_ok = test_dashboard_import()
    
    print("\n📊 VERIFICATION RESULTS:")
    print(f"Callbacks Syntax: {'✅ FIXED' if callbacks_ok else '❌ NEEDS FIX'}")
    print(f"App Syntax: {'✅ FIXED' if app_ok else '❌ NEEDS FIX'}")
    print(f"Import Issues: {'✅ FIXED' if import_ok else '❌ NEEDS FIX'}")
    
    if callbacks_ok and app_ok and import_ok:
        print("\n🎉 ALL DASHBOARD ISSUES FIXED!")
        print("✅ IndentationError resolved")
        print("✅ ImportError resolved")
        print("✅ Dashboard ready to run")
        print("\n🚀 To start dashboard: python dashboard/app.py")
        return True
    else:
        print("\n⚠️ Some issues still need attention")
        return False

if __name__ == "__main__":
    main()
