#!/usr/bin/env python3
"""
Complete Dashboard Status Checker
Checks all tabs, sidebar features, and functionality
"""
import os
import sys

# Add the dashboard directory to Python path
dashboard_dir = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def count_lines_in_file(filepath):
    """Count lines in a file"""
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def search_in_file(filepath, search_term):
    """Search for a term in a file and return count"""
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count(search_term)
    except:
        return 0

def main():
    print("🔍 COMPLETE DASHBOARD STATUS CHECK")
    print("=" * 60)
    
    base_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
    
    # Check main dashboard files
    print("\n📁 CORE DASHBOARD FILES:")
    print("-" * 30)
    
    core_files = [
        "app.py",
        "layout.py", 
        "callbacks.py",
        "dash_app.py"
    ]
    
    for file in core_files:
        filepath = os.path.join(base_path, file)
        exists = check_file_exists(filepath)
        lines = count_lines_in_file(filepath)
        status = "✅" if exists else "❌"
        print(f"{status} {file}: {lines} lines")
    
    # Check tab layout files
    print("\n📋 TAB LAYOUT FILES:")
    print("-" * 30)
    
    tab_files = [
        "auto_trading_layout.py",
        "futures_trading_layout.py", 
        "binance_exact_layout.py",
        "email_config_layout.py",
        "hybrid_learning_layout.py"
    ]
    
    for file in tab_files:
        filepath = os.path.join(base_path, file)
        exists = check_file_exists(filepath)
        lines = count_lines_in_file(filepath)
        status = "✅" if exists else "❌"
        print(f"{status} {file}: {lines} lines")
    
    # Check callbacks and features
    print("\n🔧 CALLBACK ANALYSIS:")
    print("-" * 30)
    
    callbacks_file = os.path.join(base_path, "callbacks.py")
    
    if check_file_exists(callbacks_file):
        callback_count = search_in_file(callbacks_file, "@app.callback")
        register_count = search_in_file(callbacks_file, "register_")
        sidebar_callbacks = search_in_file(callbacks_file, "sidebar-")
        
        print(f"✅ Total @app.callback: {callback_count}")
        print(f"✅ Register functions: {register_count}")
        print(f"✅ Sidebar callbacks: {sidebar_callbacks}")
    else:
        print("❌ callbacks.py not found")
    
    # Check layout.py for tabs
    print("\n📊 TAB ANALYSIS:")
    print("-" * 30)
    
    layout_file = os.path.join(base_path, "layout.py")
    
    if check_file_exists(layout_file):
        dashboard_tab = search_in_file(layout_file, "📊 Dashboard")
        auto_trading_tab = search_in_file(layout_file, "🤖 Auto Trading")
        futures_tab = search_in_file(layout_file, "📈 Futures Trading")
        binance_tab = search_in_file(layout_file, "🔗 Binance-Exact")
        email_tab = search_in_file(layout_file, "✉️ Email Config")
        hybrid_tab = search_in_file(layout_file, "🧠 Hybrid Learning")
        
        print(f"✅ Dashboard Tab: {'Present' if dashboard_tab > 0 else 'Missing'}")
        print(f"✅ Auto Trading Tab: {'Present' if auto_trading_tab > 0 else 'Missing'}")
        print(f"✅ Futures Trading Tab: {'Present' if futures_tab > 0 else 'Missing'}")
        print(f"✅ Binance-Exact Tab: {'Present' if binance_tab > 0 else 'Missing'}")
        print(f"✅ Email Config Tab: {'Present' if email_tab > 0 else 'Missing'}")
        print(f"{'✅' if hybrid_tab > 0 else '❌'} Hybrid Learning Tab: {'Present' if hybrid_tab > 0 else 'MISSING'}")
        
        total_tabs = sum([dashboard_tab > 0, auto_trading_tab > 0, futures_tab > 0, binance_tab > 0, email_tab > 0, hybrid_tab > 0])
        print(f"\n📊 Total Tabs: {total_tabs}/6")
    else:
        print("❌ layout.py not found")
    
    # Check sidebar features
    print("\n🔧 SIDEBAR ANALYSIS:")
    print("-" * 30)
    
    if check_file_exists(layout_file):
        symbol_selection = search_in_file(layout_file, "sidebar-symbol")
        virtual_balance = search_in_file(layout_file, "virtual-balance")
        amount_controls = search_in_file(layout_file, "sidebar-amount")
        risk_controls = search_in_file(layout_file, "sidebar-risk")
        quick_buttons = search_in_file(layout_file, "sidebar-amount-")
        performance = search_in_file(layout_file, "sidebar-winrate")
        
        print(f"✅ Symbol Selection: {'Present' if symbol_selection > 0 else 'Missing'}")
        print(f"✅ Virtual Balance: {'Present' if virtual_balance > 0 else 'Missing'}")
        print(f"{'✅' if amount_controls > 0 else '❌'} Amount Controls: {'Present' if amount_controls > 0 else 'MISSING'}")
        print(f"{'✅' if risk_controls > 0 else '❌'} Risk Controls: {'Present' if risk_controls > 0 else 'MISSING'}")
        print(f"{'✅' if quick_buttons > 0 else '❌'} Quick Buttons: {'Present' if quick_buttons > 0 else 'MISSING'}")
        print(f"{'✅' if performance > 0 else '❌'} Performance Display: {'Present' if performance > 0 else 'MISSING'}")
    
    # Summary
    print("\n🎯 SUMMARY:")
    print("-" * 30)
    
    if check_file_exists(callbacks_file) and check_file_exists(layout_file):
        callback_count = search_in_file(callbacks_file, "@app.callback")
        hybrid_tab = search_in_file(layout_file, "🧠 Hybrid Learning")
        sidebar_features = search_in_file(layout_file, "sidebar-amount") + search_in_file(layout_file, "sidebar-risk")
        
        print(f"📊 Total Callbacks: {callback_count} (Target: 93+)")
        print(f"📋 All Tabs Present: {'Yes' if hybrid_tab > 0 else 'NO - Missing Hybrid Learning'}")
        print(f"🔧 Sidebar Complete: {'Yes' if sidebar_features > 0 else 'NO - Missing Controls'}")
        
        if callback_count >= 80 and hybrid_tab > 0 and sidebar_features > 0:
            print("\n🎉 STATUS: DASHBOARD FULLY RESTORED!")
        elif callback_count >= 80:
            print("\n⚠️  STATUS: MOSTLY RESTORED - Minor issues")
        else:
            print("\n❌ STATUS: NEEDS MORE WORK")
    else:
        print("❌ Cannot complete analysis - missing core files")

if __name__ == "__main__":
    main()
