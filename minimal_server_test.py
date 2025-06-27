import sys
import os

print("Starting minimal server test...")

# Add the backend directory to the path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)

print(f"Backend directory: {backend_dir}")

# Test uvicorn import
try:
    import uvicorn
    print("✓ uvicorn imported successfully")
except ImportError as e:
    print(f"✗ uvicorn import failed: {e}")
    sys.exit(1)

# Test fastapi import
try:
    from fastapi import FastAPI
    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")
    sys.exit(1)

# Create a minimal app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Minimal test server"}

@app.get("/health")
def health():
    return {"status": "healthy"}

print("Starting minimal server on port 8000...")
try:
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
except Exception as e:
    print(f"Server startup error: {e}")
    import traceback
    traceback.print_exc()
