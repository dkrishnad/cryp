#!/usr/bin/env python3
"""
Minimal FastAPI test to verify server can start
"""
from fastapi import FastAPI
import uvicorn

# Create minimal app
app = FastAPI(title="Crypto Bot API Test")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Minimal server is running"}

@app.get("/test")
def test_endpoint():
    return {"status": "success", "message": "Test endpoint working"}

if __name__ == "__main__":
    print("🚀 Starting minimal FastAPI server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📍 Health check: http://localhost:8000/health")
    print("📍 Test endpoint: http://localhost:8000/test")
    print("📍 API docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
