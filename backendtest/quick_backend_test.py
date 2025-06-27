#!/usr/bin/env python3
"""
Quick test to verify backend can start without errors
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_backend_startup():
    """Test if the backend can start successfully"""
    try:
        print("🔧 Testing backend startup...")
        
        # Import the main module to test for import errors
        import main
        print("✅ main.py imports successfully")
        
        # Check if the FastAPI app is created
        if hasattr(main, 'app'):
            print("✅ FastAPI app is created")
        else:
            print("❌ FastAPI app not found")
            return False
            
        # Check if database is initialized
        if hasattr(main, 'initialize_database'):
            print("✅ Database functions available")
        else:
            print("❌ Database functions not available")
            
        print("✅ Backend startup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Backend startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backend_startup()
    sys.exit(0 if success else 1)
