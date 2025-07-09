#!/usr/bin/env python3
"""
🔧 LAUNCHER DIAGNOSTIC TOOL
Quick diagnosis of launcher issues
"""

import os
import sys
import subprocess
import traceback

def print_section(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_environment():
    """Check Python environment"""
    print_section("ENVIRONMENT CHECK")
    
    print(f"✅ Python Version: {sys.version}")
    print(f"✅ Python Executable: {sys.executable}")
    print(f"✅ Current Directory: {os.getcwd()}")
    print(f"✅ Script Location: {__file__}")

def check_files():
    """Check required files"""
    print_section("FILE CHECK")
    
    required_files = [
        'launch_bot.py',
        'launch_bot_v3.py', 
        'simple_launcher.py',
        'START_BOT.bat',
        'backend/main.py',
        'dashboard/start_dashboard.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - EXISTS")
        else:
            print(f"❌ {file_path} - MISSING")

def check_imports():
    """Check critical imports"""
    print_section("IMPORT CHECK")
    
    critical_modules = [
        'subprocess', 'requests', 'time', 'threading',
        'psutil', 'fastapi', 'uvicorn', 'dash'
    ]
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")

def test_launcher_import():
    """Test launcher import"""
    print_section("LAUNCHER IMPORT TEST")
    
    try:
        import launch_bot
        print("✅ launch_bot.py imports successfully")
        
        # Test key functions exist
        functions = ['main', 'launch_backend', 'launch_dashboard']
        for func in functions:
            if hasattr(launch_bot, func):
                print(f"✅ Function {func} exists")
            else:
                print(f"❌ Function {func} missing")
                
    except Exception as e:
        print(f"❌ launch_bot.py import failed: {e}")
        traceback.print_exc()

def test_simple_backend_start():
    """Test if we can start backend manually"""
    print_section("BACKEND START TEST")
    
    try:
        backend_path = os.path.join(os.getcwd(), "backend")
        if os.path.exists(backend_path):
            print(f"✅ Backend directory exists: {backend_path}")
            
            # Check if main.py exists
            main_file = os.path.join(backend_path, "main.py")
            if os.path.exists(main_file):
                print(f"✅ Backend main.py exists")
                
                # Try to import backend main (without running)
                sys.path.insert(0, backend_path)
                try:
                    import main as backend_main
                    print("✅ Backend main.py imports successfully")
                except Exception as e:
                    print(f"⚠️ Backend import issue: {e}")
                    
            else:
                print(f"❌ Backend main.py not found")
        else:
            print(f"❌ Backend directory not found")
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")

def provide_solutions():
    """Provide solutions"""
    print_section("SOLUTIONS")
    
    print("🔧 TO FIX THE START_BOT.bat ISSUE:")
    print("1. Use the fixed batch file: START_BOT_FIXED.bat")
    print("2. Or run directly: python launch_bot.py")
    print("3. Or run manually:")
    print("   - Open Command Prompt")
    print("   - cd \"c:\\Users\\Hari\\Desktop\\Crypto bot\"")
    print("   - python launch_bot.py")
    
    print("\n🚀 ALTERNATIVE QUICK START:")
    print("   python launch_bot.py")
    
    print("\n📋 MANUAL START (if launcher fails):")
    print("   Terminal 1: cd backend && python -m uvicorn main:app --port 8001")
    print("   Terminal 2: cd dashboard && python start_dashboard.py")

def main():
    """Run all diagnostics"""
    print("🚀 CRYPTO BOT LAUNCHER DIAGNOSTICS")
    print("This tool will help identify why START_BOT.bat isn't working")
    
    try:
        check_environment()
        check_files()
        check_imports()
        test_launcher_import()
        test_simple_backend_start()
        provide_solutions()
        
        print(f"\n{'='*50}")
        print("🎯 DIAGNOSIS COMPLETE")
        print("Check the results above to identify issues.")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
    
    # Keep window open
    input("\nPress Enter to exit...")
