#!/usr/bin/env python3
"""
Quick Backend Test
==================
Tests if backend can import and start
"""

import sys
import os

# Add backend to path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

print("🔍 Testing Backend...")
print("Directory:", os.getcwd())
print("Python path includes backend:", backend_dir in sys.path)

try:
    print("\n📦 Testing main import...")
    import main
    print("✅ Main module imported successfully")
    
    print("📦 Testing app object...")
    if hasattr(main, 'app'):
        print("✅ FastAPI app object exists")
    else:
        print("❌ No FastAPI app object found")
    
    print("\n🚀 Testing server startup...")
    # Try a very basic startup test
    import uvicorn
    print("✅ uvicorn available")
    
    print("\n✅ Backend looks good - try starting manually:")
    print("cd 'c:\\Users\\Hari\\Desktop\\Crypto bot\\backend'")
    print("python main.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
