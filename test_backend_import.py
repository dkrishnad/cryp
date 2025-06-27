#!/usr/bin/env python3
"""
Test script to check if backend.main imports correctly
"""
import sys
import os

try:
    print("Testing backend.main import...")
    from backend import main
    print("✅ Backend imports successfully!")
    print("✅ All import issues have been resolved!")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Other Error: {e}")
    sys.exit(1)
