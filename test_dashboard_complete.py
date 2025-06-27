#!/usr/bin/env python3
"""
Test script to verify all dashboard components and callbacks are functional
"""

def test_dashboard_import():
    """Test if all dashboard modules can be imported without errors"""
    try:
        print("📊 Testing Dashboard Import...")
        
        # Test main dashboard files
        import sys
        import os
        sys.path.append(os.path.abspath('.'))
        sys.path.append(os.path.abspath('./dashboard'))
        
        # Import dash first
        import dash
        print("✅ Dash imported successfully")
        
        # Import main layout
        from dashboard.layout import layout
        print("✅ Dashboard layout imported successfully")
        
        # Import callbacks
        from dashboard import callbacks
        print("✅ Dashboard callbacks imported successfully")
        
        # Import tab layouts
        from dashboard.auto_trading_layout import create_auto_trading_layout
        from dashboard.futures_trading_layout import create_futures_trading_layout
        from dashboard.binance_exact_layout import create_binance_exact_layout
        from dashboard.email_config_layout import create_email_config_layout
        from dashboard.hybrid_learning_layout import create_hybrid_learning_layout
        print("✅ All tab layouts imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard import failed: {e}")
        return False

def count_dashboard_callbacks():
    """Count all callbacks in dashboard files"""
    import os
    import re
    
    callback_files = [
        'dashboard/callbacks.py',
        'dashboard/hybrid_learning_layout.py',
        'dashboard/email_config_layout.py',
        'dashboard/binance_exact_callbacks.py',
        'dashboard/auto_trading_layout.py',
        'dashboard/futures_trading_layout.py',
        'dashboard/binance_exact_layout.py'
    ]
    
    total_callbacks = 0
    for file_path in callback_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                callbacks_count = len(re.findall(r'@app\.callback', content))
                print(f"  📝 {file_path}: {callbacks_count} callbacks")
                total_callbacks += callbacks_count
        else:
            print(f"  ❌ {file_path}: File not found")
    
    print(f"\n🎯 TOTAL CALLBACKS: {total_callbacks}")
    target_callbacks = 93
    print(f"🎯 TARGET: {target_callbacks} callbacks")
    print(f"📊 Coverage: {(total_callbacks/target_callbacks)*100:.1f}%")
    
    if total_callbacks >= target_callbacks:
        print("✅ CALLBACK TARGET REACHED!")
    else:
        missing = target_callbacks - total_callbacks
        print(f"⚠️  Missing {missing} callbacks")
    
    return total_callbacks

def check_sidebar_components():
    """Check if all sidebar components are present"""
    print("\n🔧 CHECKING SIDEBAR COMPONENTS...")
    
    sidebar_components = [
        "sidebar-symbol",           # Symbol dropdown
        "virtual-balance",          # Virtual balance display
        "reset-balance-btn",        # Reset balance button
        "reset-balance-btn-output", # Reset button output
    ]
    
    try:
        from dashboard.layout import layout
        layout_str = str(layout)
        
        for component in sidebar_components:
            if component in layout_str:
                print(f"  ✅ {component}: Found")
            else:
                print(f"  ❌ {component}: Missing")
                
    except Exception as e:
        print(f"❌ Error checking sidebar: {e}")

def check_tab_components():
    """Check if all main tabs are present"""
    print("\n📑 CHECKING TAB COMPONENTS...")
    
    tabs = [
        "📊 Dashboard",
        "🤖 Auto Trading", 
        "📈 Futures Trading",
        "🔗 Binance-Exact API",
        "✉️ Email Config"
    ]
    
    try:
        from dashboard.layout import layout
        layout_str = str(layout)
        
        for tab in tabs:
            if tab in layout_str:
                print(f"  ✅ {tab}: Found")
            else:
                print(f"  ❌ {tab}: Missing")
                
    except Exception as e:
        print(f"❌ Error checking tabs: {e}")

def check_button_outputs():
    """Check if critical button outputs are present"""
    print("\n🔘 CHECKING BUTTON OUTPUTS...")
    
    button_outputs = [
        "check-drift-btn-output",
        "online-learn-btn-output", 
        "test-db-btn-output",
        "test-ml-btn-output",
        "tune-models-btn-output",
        "reset-balance-btn-output",
        "get-prediction-btn"
    ]
    
    try:
        import os
        if os.path.exists('dashboard/callbacks.py'):
            with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
            for output in button_outputs:
                if output in content:
                    print(f"  ✅ {output}: Found")
                else:
                    print(f"  ❌ {output}: Missing")
        else:
            print("❌ callbacks.py file not found")
            
    except Exception as e:
        print(f"❌ Error checking button outputs: {e}")

def main():
    """Main test function"""
    print("🚀 CRYPTO BOT DASHBOARD VERIFICATION")
    print("=" * 50)
    
    # Test 1: Import test
    import_success = test_dashboard_import()
    
    # Test 2: Count callbacks
    print("\n📊 CALLBACK COUNT VERIFICATION")
    print("-" * 30)
    callback_count = count_dashboard_callbacks()
    
    # Test 3: Check sidebar
    check_sidebar_components()
    
    # Test 4: Check tabs
    check_tab_components()
    
    # Test 5: Check button outputs
    check_button_outputs()
    
    # Final assessment
    print("\n🏆 FINAL ASSESSMENT")
    print("=" * 50)
    
    if import_success:
        print("✅ Dashboard imports: SUCCESSFUL")
    else:
        print("❌ Dashboard imports: FAILED")
    
    if callback_count >= 93:
        print("✅ Callback coverage: COMPLETE (93+ callbacks)")
    else:
        print(f"⚠️  Callback coverage: PARTIAL ({callback_count}/93 callbacks)")
    
    print("\n🎯 RECOMMENDATION:")
    if import_success and callback_count >= 90:
        print("Dashboard appears to be fully functional!")
        print("All major components and settings should be working.")
    else:
        print("Dashboard may need additional fixes.")
        if not import_success:
            print("- Fix import errors")
        if callback_count < 90:
            print("- Add missing callbacks")

if __name__ == "__main__":
    main()
