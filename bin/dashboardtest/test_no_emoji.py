#!/usr/bin/env python3
print("=== BASIC TEST ===")
print("Python is working")

try:
    import dash
    print("[OK] Dash imported successfully")
except ImportError as e:
    print(f"[ERROR] Dash import failed: {e}")

try:
    import dash_bootstrap_components
    print("[OK] DBC imported successfully")
except ImportError as e:
    print(f"[ERROR] DBC import failed: {e}")

try:
    import plotly
    print("[OK] Plotly imported successfully")
except ImportError as e:
    print(f"[ERROR] Plotly import failed: {e}")

print("=== TESTING LAYOUT IMPORT ===")
try:
    from layout import layout
    print("[OK] Layout imported successfully")
except Exception as e:
    print(f"[ERROR] Layout import failed: {e}")
    import traceback
    traceback.print_exc()

print("=== TESTING DASH APP ===")
try:
    from dash_app import app
    print("[OK] Dash app imported successfully")
except Exception as e:
    print(f"[ERROR] Dash app import failed: {e}")
    import traceback
    traceback.print_exc()

print("=== TEST COMPLETE ===")
