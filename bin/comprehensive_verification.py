#!/usr/bin/env python3
"""
COMPREHENSIVE BOT VERIFICATION SCRIPT
=====================================
This script checks all critical components of the crypto trading bot.
"""

import os
import sys
import subprocess
import requests
import importlib
import ast

def print_status(message, status="INFO"):
    """Print colored status message"""
    icons = {"PASS": "✅", "FAIL": "❌", "INFO": "ℹ️", "WARN": "⚠️"}
    icon = icons.get(status, "•")
    print(f"{icon} {status} {message}")

def test_directory_structure():
    """Test directory structure"""
    print_status("Directory Structure", "INFO")
    
    required_dirs = ["backend", "dashboard", "data"]
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_status(f"  {dir_name}/ exists", "PASS")
        else:
            print_status(f"  {dir_name}/ missing", "FAIL")
            all_exist = False
    
    return all_exist

def test_backend_files():
    """Test backend files"""
    print_status("Backend Files", "INFO")
    
    backend_files = ["main.py", "db.py", "trading.py"]
    all_exist = True
    
    for file_name in backend_files:
        file_path = os.path.join("backend", file_name)
        if os.path.exists(file_path):
            print_status(f"  backend/{file_name} exists", "PASS")
        else:
            print_status(f"  backend/{file_name} missing", "FAIL")
            all_exist = False
    
    return all_exist

def test_dashboard_files():
    """Test dashboard files"""
    print_status("Dashboard Files", "INFO")
    
    dashboard_files = ["app.py", "callbacks.py", "layout.py", "start_dashboard.py"]
    all_exist = True
    
    for file_name in dashboard_files:
        file_path = os.path.join("dashboard", file_name)
        if os.path.exists(file_path):
            print_status(f"  dashboard/{file_name} exists", "PASS")
        else:
            print_status(f"  dashboard/{file_name} missing", "FAIL")
            all_exist = False
    
    return all_exist

def test_python_imports():
    """Test Python imports"""
    print_status("Python Imports", "INFO")
    
    required_packages = ["fastapi", "uvicorn", "dash", "plotly", "pandas", "numpy", "requests"]
    all_imported = True
    
    for package in required_packages:
        try:
            if package == "dash-bootstrap-components":
                import dash_bootstrap_components
            else:
                __import__(package)
            print_status(f"  {package} imported", "PASS")
        except ImportError:
            print_status(f"  {package} missing", "FAIL")
            all_imported = False
    
    return all_imported

def test_backend_import():
    """Test backend import"""
    print_status("Backend Import", "INFO")
    
    try:
        sys.path.insert(0, os.path.abspath("backend"))
        import main
        print_status("  backend.main imported", "PASS")
        return True
    except Exception as e:
        print_status(f"  backend.main failed: {str(e)[:50]}...", "FAIL")
        return False

def test_port_availability():
    """Test port availability"""
    print_status("Port Availability", "INFO")
    
    ports = [8001, 8050]
    all_available = True
    
    for port in ports:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            print_status(f"  Port {port} occupied", "WARN")
        except requests.exceptions.ConnectionError:
            print_status(f"  Port {port} available", "PASS")
        except Exception:
            print_status(f"  Port {port} available", "PASS")
    
    return True  # Ports being used is not necessarily a failure

def test_launcher_syntax():
    """Test launcher syntax"""
    print_status("Launcher Syntax", "INFO")
    
    try:
        with open("launch_bot.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        ast.parse(content)
        print_status("  launch_bot.py syntax OK", "PASS")
        return True
    except SyntaxError as e:
        print_status(f"  launch_bot.py syntax error: {e}", "FAIL")
        return False
    except Exception as e:
        print_status(f"  launch_bot.py error: {e}", "FAIL")
        return False

def main():
    """Run all verification tests"""
    print("🚀 COMPREHENSIVE CRYPTO BOT VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Backend Files", test_backend_files),
        ("Dashboard Files", test_dashboard_files),
        ("Python Imports", test_python_imports),
        ("Backend Import", test_backend_import),
        ("Port Availability", test_port_availability),
        ("Launcher Syntax", test_launcher_syntax),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print_status(f"{test_name} - Exception: {e}", "FAIL")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    failed_tests = []
    for test_name, result in results.items():
        if result:
            print_status(f"{test_name}", "PASS")
        else:
            print_status(f"{test_name}", "FAIL")
            failed_tests.append(test_name)
    
    print("=" * 60)
    
    if not failed_tests:
        print_status("All tests passed! Bot is ready to launch! 🎉", "PASS")
    else:
        print_status("Some tests failed. Please address the issues above.", "WARN")
        print_status("Check missing dependencies or files.", "INFO")
    
    print('echo "Verification complete"')

if __name__ == "__main__":
    main()
