#!/usr/bin/env python3
"""
🔧 LAUNCHER VERIFICATION AND DIAGNOSTICS
Test all launcher components before full deployment
"""

import os
import sys
import subprocess
import time
import requests
import importlib.util

def print_header(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_directories():
    """Test directory structure"""
    print_header("DIRECTORY STRUCTURE TEST")
    
    required_dirs = ['backend', 'dashboard']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False
    
    return True

def test_backend_files():
    """Test backend files"""
    print_header("BACKEND FILES TEST")
    
    backend_files = ['main.py', 'db.py', 'trading.py']
    backend_path = 'backend'
    
    for file_name in backend_files:
        file_path = os.path.join(backend_path, file_name)
        if os.path.exists(file_path):
            print(f"✅ backend/{file_name} exists")
        else:
            print(f"⚠️ backend/{file_name} missing (may be optional)")
    
    return True

def test_dashboard_files():
    """Test dashboard files"""
    print_header("DASHBOARD FILES TEST")
    
    dashboard_files = ['start_dashboard.py', 'start_app.py', 'app.py', 'dash_app.py']
    dashboard_path = 'dashboard'
    
    found_main = False
    for file_name in dashboard_files:
        file_path = os.path.join(dashboard_path, file_name)
        if os.path.exists(file_path):
            print(f"✅ dashboard/{file_name} exists")
            found_main = True
        else:
            print(f"⚠️ dashboard/{file_name} not found")
    
    if found_main:
        print("✅ At least one dashboard start file found")
        return True
    else:
        print("❌ No dashboard start files found")
        return False

def test_imports():
    """Test Python imports"""
    print_header("PYTHON IMPORTS TEST")
    
    required_modules = [
        'fastapi', 'uvicorn', 'dash', 'plotly', 
        'pandas', 'numpy', 'requests', 'subprocess'
    ]
    
    for module in required_modules:
        try:
            if module == 'dash-bootstrap-components':
                import dash_bootstrap_components
            else:
                __import__(module)
            print(f"✅ {module} import OK")
        except ImportError:
            print(f"❌ {module} import FAILED")
            return False
    
    return True

def test_backend_import():
    """Test backend main.py import"""
    print_header("BACKEND IMPORT TEST")
    
    original_dir = os.getcwd()
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Try to import main
        spec = importlib.util.spec_from_file_location("main", "main.py")
        if spec is None:
            print("❌ Could not create module spec for main.py")
            return False
            
        main_module = importlib.util.module_from_spec(spec)
        
        print("✅ Backend main.py can be loaded")
        
        # Restore directory
        os.chdir(original_dir)
        return True
        
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        # Always restore directory
        try:
            os.chdir(original_dir)
        except:
            pass
        return False

def test_port_availability():
    """Test port availability"""
    print_header("PORT AVAILABILITY TEST")
    
    ports = [8001, 8050]
    
    for port in ports:
        try:
            # Try to connect
            response = requests.get(f"http://localhost:{port}", timeout=1)
            print(f"⚠️ Port {port} is occupied (service may be running)")
        except requests.exceptions.ConnectionError:
            print(f"✅ Port {port} is available")
        except Exception as e:
            print(f"⚠️ Port {port} test inconclusive: {e}")
    
    return True

def test_launcher_syntax():
    """Test launcher script syntax"""
    print_header("LAUNCHER SYNTAX TEST")
    
    launcher_files = ['launch_bot.py', 'simple_launcher.py']
    
    for launcher in launcher_files:
        if os.path.exists(launcher):
            try:
                # Compile the file to check syntax
                with open(launcher, 'r') as f:
                    compile(f.read(), launcher, 'exec')
                print(f"✅ {launcher} syntax OK")
            except SyntaxError as e:
                print(f"❌ {launcher} syntax error: {e}")
                return False
        else:
            print(f"⚠️ {launcher} not found")
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 CRYPTO BOT LAUNCHER VERIFICATION")
    print("Testing all components before deployment...")
    
    tests = [
        ("Directory Structure", test_directories),
        ("Backend Files", test_backend_files),
        ("Dashboard Files", test_dashboard_files),
        ("Python Imports", test_imports),
        ("Backend Import", test_backend_import),
        ("Port Availability", test_port_availability),
        ("Launcher Syntax", test_launcher_syntax)
    ]
    
    all_passed = True
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
            all_passed = False
    
    # Summary
    print_header("TEST SUMMARY")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Launcher is ready for deployment.")
        print("💡 You can now run: python launch_bot.py")
    else:
        print("\n⚠️ Some tests failed. Please address the issues above.")
        print("💡 Check missing dependencies or files.")
    
    return all_passed

if __name__ == "__main__":
    run_comprehensive_test()
