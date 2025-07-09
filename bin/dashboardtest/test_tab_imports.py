#!/usr/bin/env python3
"""
Test tab imports to find skeleton issue
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== TAB IMPORT TEST ===")

tab_modules = [
    'auto_trading_layout',
    'futures_trading_layout', 
    'binance_exact_layout',
    'email_config_layout',
    'hybrid_learning_layout'
]

working_tabs = []
failing_tabs = []

for tab in tab_modules:
    print(f"Testing {tab}...")
    try:
        module = __import__(tab)
        print(f"✅ {tab} imported successfully")
        
        # Test if create function exists
        create_func_name = f"create_{tab.replace('_layout', '')}_layout"
        if hasattr(module, create_func_name):
            print(f"✅ {create_func_name} function found")
            
            # Try to call the function
            try:
                layout_func = getattr(module, create_func_name)
                result = layout_func()
                print(f"✅ {create_func_name} executes successfully")
                working_tabs.append(tab)
            except Exception as e:
                print(f"❌ {create_func_name} execution failed: {e}")
                failing_tabs.append((tab, str(e)))
        else:
            print(f"❌ {create_func_name} function not found")
            failing_tabs.append((tab, "function not found"))
            
    except Exception as e:
        print(f"❌ {tab} import failed: {e}")
        failing_tabs.append((tab, str(e)))
    
    print()

print("=== TAB IMPORT SUMMARY ===")
print(f"Working tabs: {len(working_tabs)}")
for tab in working_tabs:
    print(f"  ✅ {tab}")

print(f"\nFailing tabs: {len(failing_tabs)}")
for tab, error in failing_tabs:
    print(f"  ❌ {tab}: {error}")

if len(failing_tabs) > 0:
    print("\n🔍 SKELETON CAUSE IDENTIFIED:")
    print("Tab layout import failures are causing the skeleton dashboard!")
    print("The main layout cannot build properly when tab imports fail.")
else:
    print("\n✅ All tab imports work - issue is elsewhere")
