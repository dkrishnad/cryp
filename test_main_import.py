#!/usr/bin/env python3
"""
MINIMAL BACKEND TEST - Test if main.py can import
"""
import sys
import os

def test_main_import():
    """Test if main.py can be imported"""
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        os.chdir(backend_dir)
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Add to path
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        print("🔧 Testing main.py import...")
        
        # Test step by step
        print("1. Importing sys, os, json...")
        import sys, os, json
        print("✅ Basic imports OK")
        
        print("2. Importing FastAPI...")
        from fastapi import FastAPI
        print("✅ FastAPI import OK")
        
        print("3. Attempting main.py import...")
        import main
        print("✅ main.py imported successfully!")
        
        print("4. Testing app creation...")
        app = main.app
        print(f"✅ App created: {app.title if hasattr(app, 'title') else 'FastAPI app'}")
        
        print("5. Testing uvicorn startup...")
        import uvicorn
        print("✅ uvicorn available")
        
        print("🎉 ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_main_import()
    if success:
        print("\n🚀 main.py is ready to run!")
    else:
        print("\n⚠️  main.py has import issues")
