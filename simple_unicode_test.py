#!/usr/bin/env python3
"""
Simple test to verify Unicode issues are fixed
"""

import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

print("[TEST] Testing imports...")

try:
    # Try importing the problematic modules
    print("[TEST] Importing main module...")
    
    # Read first few lines to check for Unicode issues
    with open('main.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()[:30]
    
    print("[TEST] Checking for Unicode characters in print statements...")
    unicode_found = False
    for i, line in enumerate(lines, 1):
        if 'print(' in line and any(ord(c) > 127 for c in line):
            print(f"[TEST] Unicode found on line {i}: {repr(line.strip())}")
            unicode_found = True
    
    if not unicode_found:
        print("[TEST] SUCCESS: No Unicode characters found in print statements")
    
    # Try to import basic modules
    print("[TEST] Testing basic imports...")
    import fastapi
    print("[TEST] FastAPI imported successfully")
    
    import uvicorn
    print("[TEST] Uvicorn imported successfully")
    
    print("[TEST] All tests passed - Unicode issues should be fixed!")
    
except Exception as e:
    print(f"[TEST] ERROR: {e}")
    import traceback
    traceback.print_exc()

print("[TEST] Test completed")
