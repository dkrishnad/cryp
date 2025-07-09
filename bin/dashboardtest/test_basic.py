#!/usr/bin/env python3
print("=== BASIC TEST ===")
print("Python is working")

try:
    import dash
    print("✅ Dash imported successfully")
except ImportError as e:
    print(f"❌ Dash import failed: {e}")

try:
    import dash_bootstrap_components
    print("✅ DBC imported successfully")
except ImportError as e:
    print(f"❌ DBC import failed: {e}")

try:
    import plotly
    print("✅ Plotly imported successfully")
except ImportError as e:
    print(f"❌ Plotly import failed: {e}")

print("=== TEST COMPLETE ===")
