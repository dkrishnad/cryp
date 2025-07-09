#!/usr/bin/env python3
"""
Quick diagnostic script to check what's wrong
"""
import os
import sys
import subprocess
import requests

def check_python():
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print()

def check_directories():
    print("Checking directories...")
    backend_exists = os.path.exists("backend")
    dashboard_exists = os.path.exists("dashboard")
    print(f"Backend directory exists: {backend_exists}")
    print(f"Dashboard directory exists: {dashboard_exists}")
    
    if backend_exists:
        backend_files = os.listdir("backend")
        print(f"Backend files: {backend_files[:5]}...")  # Show first 5
    
    if dashboard_exists:
        dashboard_files = [f for f in os.listdir("dashboard") if f.endswith('.py')]
        print(f"Dashboard Python files: {dashboard_files[:5]}...")  # Show first 5
    print()

def check_dependencies():
    print("Checking key dependencies...")
    try:
        import uvicorn
        print("✓ uvicorn available")
    except ImportError:
        print("✗ uvicorn NOT available")
    
    try:
        import dash
        print("✓ dash available")
    except ImportError:
        print("✗ dash NOT available")
    
    try:
        import requests
        print("✓ requests available")
    except ImportError:
        print("✗ requests NOT available")
    print()

def test_backend_manually():
    print("Testing backend manually...")
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        print("Backend directory not found!")
        return
    
    try:
        # Try to import the backend main module
        sys.path.insert(0, backend_path)
        import main
        print("✓ Backend main.py can be imported")
        
        # Check if FastAPI app exists
        if hasattr(main, 'app'):
            print("✓ FastAPI app found in main.py")
        else:
            print("✗ No 'app' found in main.py")
            
    except Exception as e:
        print(f"✗ Error importing backend: {e}")
    finally:
        if backend_path in sys.path:
            sys.path.remove(backend_path)
    print()

def test_dashboard_manually():
    print("Testing dashboard manually...")
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        print("Dashboard directory not found!")
        return
    
    # Check which dashboard files exist
    dashboard_files = ['start_beautiful.py', 'start_safe.py', 'layout.py', 'callbacks.py']
    for file in dashboard_files:
        file_path = os.path.join(dashboard_path, file)
        exists = os.path.exists(file_path)
        print(f"{file}: {'✓' if exists else '✗'}")
    
    # Try to import layout
    try:
        sys.path.insert(0, dashboard_path)
        import layout
        print("✓ Dashboard layout.py can be imported")
    except Exception as e:
        print(f"✗ Error importing layout: {e}")
    finally:
        if dashboard_path in sys.path:
            sys.path.remove(dashboard_path)
    print()

def main():
    print("="*60)
    print("CRYPTO BOT DIAGNOSTIC")
    print("="*60)
    print()
    
    check_python()
    check_directories()
    check_dependencies()
    test_backend_manually()
    test_dashboard_manually()
    
    print("="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
