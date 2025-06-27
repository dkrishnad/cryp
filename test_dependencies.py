#!/usr/bin/env python3
"""
Simple test to identify import issues
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

print("Testing individual imports...")

try:
    print("Testing numpy...")
    import numpy as np
    print("✅ numpy OK")
    
    print("Testing pandas...")
    import pandas as pd
    print("✅ pandas OK")
    
    print("Testing sklearn...")
    from sklearn.linear_model import SGDClassifier
    print("✅ sklearn OK")
    
    print("Testing sqlite3...")
    import sqlite3
    print("✅ sqlite3 OK")
    
    print("Testing json...")
    import json
    print("✅ json OK")
    
    print("Testing datetime...")
    from datetime import datetime
    print("✅ datetime OK")
    
    print("Testing threading...")
    import threading
    print("✅ threading OK")
    
    print("Testing joblib...")
    import joblib
    print("✅ joblib OK")
    
    print("\nAll basic dependencies are OK!")
    
    print("\nTesting TA-Lib (optional)...")
    try:
        import talib
        print("✅ TA-Lib available")
    except ImportError:
        print("⚠ TA-Lib not available (will use fallback)")
    
    print("\nTesting schedule...")
    try:
        import schedule
        print("✅ schedule available")
    except ImportError:
        print("❌ schedule not available - need to install")
    
    print("\nTesting aiohttp...")
    try:
        import aiohttp
        print("✅ aiohttp available")
    except ImportError:
        print("❌ aiohttp not available - need to install")
        
    print("\n" + "="*50)
    print("Dependencies check complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
