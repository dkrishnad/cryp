#!/usr/bin/env python3
"""
Quick Backend Connectivity Test
"""
import requests

def test_backend_connection():
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        print(f"✅ Backend is running! Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start with: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    test_backend_connection()
