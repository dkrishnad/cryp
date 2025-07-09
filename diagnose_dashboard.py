#!/usr/bin/env python3
"""
Dashboard Diagnostic Script
This script will help identify the root cause of the dashboard errors
"""
import sys
import os
import traceback

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboardtest'))

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))

def test_imports():
    """Test all critical imports"""
    results = {}
    
    # Test dash_app import
    try:
        from dashboardtest.dash_app import app
        results['dash_app'] = "✅ OK"
        safe_print("✅ dash_app import successful")
    except Exception as e:
        results['dash_app'] = f"❌ ERROR: {str(e)}"
        safe_print(f"❌ dash_app import failed: {e}")
        traceback.print_exc()
    
    # Test layout import
    try:
        from dashboardtest.layout import layout
        results['layout'] = "✅ OK"
        safe_print("✅ layout import successful")
    except Exception as e:
        results['layout'] = f"❌ ERROR: {str(e)}"
        safe_print(f"❌ layout import failed: {e}")
        traceback.print_exc()
    
    # Test callbacks import
    try:
        import dashboardtest.callbacks
        results['callbacks'] = "✅ OK"
        safe_print("✅ callbacks import successful")
    except Exception as e:
        results['callbacks'] = f"❌ ERROR: {str(e)}"
        safe_print(f"❌ callbacks import failed: {e}")
        traceback.print_exc()
    
    # Test individual layout modules
    layout_modules = [
        'auto_trading_layout',
        'futures_trading_layout',
        'binance_exact_layout',
        'email_config_layout',
        'hybrid_learning_layout'
    ]
    
    for module in layout_modules:
        try:
            exec(f"from dashboardtest.{module} import create_{module.replace('_layout', '')}_layout")
            results[module] = "✅ OK"
            safe_print(f"✅ {module} import successful")
        except Exception as e:
            results[module] = f"❌ ERROR: {str(e)}"
            safe_print(f"❌ {module} import failed: {e}")
            traceback.print_exc()
    
    return results

def test_app_creation():
    """Test app creation and layout assignment"""
    try:
        from dashboardtest.dash_app import app
        from dashboardtest.layout import layout
        
        # Try to assign layout
        app.layout = layout
        safe_print("✅ App layout assignment successful")
        
        # Check if layout is callable
        if callable(layout):
            safe_print("✅ Layout is callable (dynamic)")
        else:
            safe_print("✅ Layout is static")
            
        return True
    except Exception as e:
        safe_print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return False

def test_backend_connection():
    """Test backend connection"""
    try:
        import requests
        response = requests.get('http://localhost:5000/api/status', timeout=5)
        if response.status_code == 200:
            safe_print("✅ Backend connection successful")
            return True
        else:
            safe_print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        safe_print(f"❌ Backend connection failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    safe_print("🔍 Starting Dashboard Diagnostic...")
    safe_print("=" * 50)
    
    # Test imports
    safe_print("🔧 Testing imports...")
    import_results = test_imports()
    
    # Test app creation
    safe_print("\n🔧 Testing app creation...")
    app_ok = test_app_creation()
    
    # Test backend connection
    safe_print("\n🔧 Testing backend connection...")
    backend_ok = test_backend_connection()
    
    # Summary
    safe_print("\n📊 DIAGNOSTIC SUMMARY")
    safe_print("=" * 50)
    
    for component, status in import_results.items():
        safe_print(f"{component}: {status}")
    
    safe_print(f"App creation: {'✅ OK' if app_ok else '❌ FAILED'}")
    safe_print(f"Backend connection: {'✅ OK' if backend_ok else '❌ FAILED'}")
    
    if all("✅" in str(v) for v in import_results.values()) and app_ok:
        safe_print("\n🎉 All components appear to be working!")
        safe_print("The issue might be in the callback functions or component IDs.")
        return True
    else:
        safe_print("\n❌ Found issues that need to be fixed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
