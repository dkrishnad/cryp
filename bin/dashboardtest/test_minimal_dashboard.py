#!/usr/bin/env python3
"""
Minimal test script to isolate dashboard issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Step 1: Testing dash_app import...")
    from dash_app import app
    print("✅ dash_app imported successfully")
    
    print("\nStep 2: Testing layout imports...")
    from auto_trading_layout import create_auto_trading_layout
    print("✅ auto_trading_layout imported")
    
    from futures_trading_layout import create_futures_trading_layout
    print("✅ futures_trading_layout imported")
    
    from binance_exact_layout import create_binance_exact_layout
    print("✅ binance_exact_layout imported")
    
    from email_config_layout import create_email_config_layout
    print("✅ email_config_layout imported")
    
    from hybrid_learning_layout import create_hybrid_learning_layout
    print("✅ hybrid_learning_layout imported")
    
    print("\nStep 3: Testing layout.py import...")
    from layout import layout
    print("✅ layout imported successfully")
    
    print("\nStep 4: Testing callbacks import...")
    import callbacks
    print("✅ callbacks imported successfully")
    
    print("\nStep 5: Setting app layout...")
    app.layout = layout
    print("✅ app layout set successfully")
    
    print("\n🎉 All imports successful! Dashboard should work.")
    
except Exception as e:
    print(f"❌ Error at step: {e}")
    import traceback
    traceback.print_exc()
