#!/usr/bin/env python3
"""
Test script to debug dashboard layout issues
"""
import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard')
sys.path.insert(0, dashboard_dir)

print(f"Dashboard dir: {dashboard_dir}")
print(f"Checking if dashboard files exist...")

# Check if key files exist
key_files = [
    'dash_app.py',
    'layout.py', 
    'callbacks.py',
    'auto_trading_layout.py',
    'futures_trading_layout.py',
    'binance_exact_layout.py',
    'email_config_layout.py',
    'hybrid_learning_layout.py'
]

for file in key_files:
    file_path = os.path.join(dashboard_dir, file)
    exists = os.path.exists(file_path)
    print(f"  {file}: {'✓' if exists else '✗'}")

print("\nTesting imports...")

try:
    print("Testing dash_app import...")
    from dash_app import app
    print("✓ dash_app imported successfully")
except Exception as e:
    print(f"✗ dash_app import error: {e}")

try:
    print("Testing layout module imports...")
    from auto_trading_layout import create_auto_trading_layout
    print("✓ auto_trading_layout imported")
    from futures_trading_layout import create_futures_trading_layout
    print("✓ futures_trading_layout imported")
    from binance_exact_layout import create_binance_exact_layout
    print("✓ binance_exact_layout imported")
    from email_config_layout import create_email_config_layout
    print("✓ email_config_layout imported")
    from hybrid_learning_layout import create_hybrid_learning_layout
    print("✓ hybrid_learning_layout imported")
except Exception as e:
    print(f"✗ Layout module import error: {e}")

try:
    print("Testing main layout import...")
    from layout import layout
    print("✓ Layout imported successfully")
    print(f"Layout type: {type(layout)}")
    print(f"Layout has children: {hasattr(layout, 'children')}")
except Exception as e:
    print(f"✗ Layout import error: {e}")

try:
    print("Testing callbacks import...")
    import callbacks
    print("✓ Callbacks imported successfully")
except Exception as e:
    print(f"✗ Callbacks import error: {e}")

print("\nLayout test complete!")
