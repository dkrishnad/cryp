#!/usr/bin/env python3
import sys
import os

# Add the backend directory to the path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Backend directory: {backend_dir}")
print(f"Python path: {sys.path[:3]}")

try:
    print("Testing import of main.py...")
    import main  # type: ignore
    print("main.py imported successfully!")
    
    print("Testing FastAPI app...")
    app = main.app
    print(f"FastAPI app: {app}")
    
    print("Testing uvicorn import...")
    import uvicorn
    print("uvicorn imported successfully!")
    
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
