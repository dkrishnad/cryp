#!/usr/bin/env python3
"""
Test Backend - Minimal version to test if FastAPI works
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test Crypto Bot Backend")

@app.get("/")
async def root():
    return {"message": "Test backend is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("🔧 Starting test backend...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
