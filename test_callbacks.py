#!/usr/bin/env python3
"""
Test script to check for duplicate callback errors by importing callbacks
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

try:
    print("Testing dashboard import...")
    from dashboard import callbacks
    print("✅ SUCCESS: Dashboard callbacks imported without errors!")
    
except Exception as e:
    print(f"❌ ERROR: Failed to import dashboard callbacks")
    print(f"Error details: {str(e)}")
    
    # Check if it's a duplicate callback error
    if "duplicate" in str(e).lower() or "output" in str(e).lower():
        print("\n🔍 This appears to be a duplicate callback issue")
        print("Details:", str(e))
    else:
        print(f"\n🔍 This is a different error: {type(e).__name__}")
