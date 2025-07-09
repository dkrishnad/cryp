#!/usr/bin/env python3
"""
COMPREHENSIVE DASHBOARD DIAGNOSIS
Step-by-step analysis to identify all issues preventing proper dashboard rendering
"""
import sys
import os
import importlib
import traceback

# Add paths
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

print("="*80)
print("COMPREHENSIVE DASHBOARD DIAGNOSIS")
print("="*80)

issues_found = []
fixes_needed = []

def report_issue(category, description, fix_suggestion):
    issues_found.append(f"❌ {category}: {description}")
    fixes_needed.append(f"🔧 FIX: {fix_suggestion}")

def report_success(category, description):
    print(f"✅ {category}: {description}")

# STEP 1: Test Core Imports
print("\n1. TESTING CORE IMPORTS")
print("-" * 40)

try:
    import dash
    from dash import dcc, html, dash_table
    import dash_bootstrap_components as dbc
    import plotly.graph_objs as go
    import plotly.express as px
    report_success("Core Libraries", "All core Dash libraries imported successfully")
except Exception as e:
    report_issue("Core Libraries", f"Failed to import core libraries: {e}", 
                "Install missing dependencies: pip install dash plotly dash-bootstrap-components")

# STEP 2: Test Dash App Import
print("\n2. TESTING DASH APP")
print("-" * 40)

try:
    from dash_app import app
    report_success("Dash App", "App instance imported successfully")
except Exception as e:
    report_issue("Dash App", f"Failed to import app: {e}", 
                "Check dash_app.py for syntax errors or missing dependencies")

# STEP 3: Test Tab Layout Imports
print("\n3. TESTING TAB LAYOUT IMPORTS")
print("-" * 40)

tab_layouts = [
    "auto_trading_layout",
    "futures_trading_layout", 
    "binance_exact_layout",
    "email_config_layout",
    "hybrid_learning_layout"
]

working_tabs = []
broken_tabs = []

for tab in tab_layouts:
    try:
        module = importlib.import_module(tab)
        create_func = getattr(module, f"create_{tab}")
        report_success("Tab Layout", f"{tab} imported and create function found")
        working_tabs.append(tab)
    except ImportError as e:
        report_issue("Tab Layout", f"{tab} import failed: {e}", 
                    f"Check {tab}.py file exists and has correct syntax")
        broken_tabs.append(tab)
    except AttributeError as e:
        report_issue("Tab Layout", f"{tab} missing create function: {e}",
                    f"Add create_{tab}() function to {tab}.py")
        broken_tabs.append(tab)
    except Exception as e:
        report_issue("Tab Layout", f"{tab} unexpected error: {e}",
                    f"Fix syntax/logic errors in {tab}.py")
        broken_tabs.append(tab)

# STEP 4: Test Main Layout Import
print("\n4. TESTING MAIN LAYOUT")
print("-" * 40)

try:
    from layout import layout
    report_success("Main Layout", "Layout imported successfully")
    
    # Check if layout is properly structured
    if hasattr(layout, 'children'):
        report_success("Layout Structure", "Layout has children property")
    else:
        report_issue("Layout Structure", "Layout missing children property",
                    "Ensure layout returns a Dash component with children")
        
except Exception as e:
    report_issue("Main Layout", f"Failed to import layout: {e}",
                "Check layout.py for syntax errors, missing imports, or circular imports")

# STEP 5: Test Callbacks Import
print("\n5. TESTING CALLBACKS")
print("-" * 40)

try:
    import callbacks
    report_success("Callbacks", "Callbacks module imported successfully")
except Exception as e:
    report_issue("Callbacks", f"Failed to import callbacks: {e}",
                "Check callbacks.py for syntax errors, missing imports, or invalid decorators")

# STEP 6: Check for Common Issues
print("\n6. CHECKING COMMON ISSUES")
print("-" * 40)

# Check if port is available
import socket
def check_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

if check_port(8050):
    report_issue("Port Availability", "Port 8050 is already in use",
                "Kill existing processes or use a different port")
else:
    report_success("Port Availability", "Port 8050 is available")

# STEP 7: Generate Report
print("\n" + "="*80)
print("DIAGNOSIS SUMMARY")
print("="*80)

if issues_found:
    print(f"\n❌ ISSUES FOUND ({len(issues_found)}):")
    for i, issue in enumerate(issues_found, 1):
        print(f"{i}. {issue}")
    
    print(f"\n🔧 FIXES NEEDED ({len(fixes_needed)}):")
    for i, fix in enumerate(fixes_needed, 1):
        print(f"{i}. {fix}")
else:
    print("\n✅ NO ISSUES FOUND - Dashboard should work properly")

print(f"\n📊 TAB STATUS:")
print(f"✅ Working tabs: {len(working_tabs)} - {working_tabs}")
print(f"❌ Broken tabs: {len(broken_tabs)} - {broken_tabs}")

print(f"\n🎯 NEXT STEPS:")
if issues_found:
    print("1. Fix the issues listed above")
    print("2. Test imports individually")
    print("3. Run this diagnosis again")
    print("4. Start dashboard with working components only")
else:
    print("1. Start the dashboard")
    print("2. Check browser console for JavaScript errors")
    print("3. Test individual features")

print("\n" + "="*80)
