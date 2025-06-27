#!/usr/bin/env python3
"""
Simple callback counter and component checker
"""
import os
import re

def count_callbacks():
    """Count callbacks in all dashboard files"""
    
    files_to_check = {
        'dashboard/callbacks.py': 0,
        'dashboard/hybrid_learning_layout.py': 0,
        'dashboard/email_config_layout.py': 0,
        'dashboard/binance_exact_callbacks.py': 0,
        'dashboard/auto_trading_layout.py': 0,
        'dashboard/futures_trading_layout.py': 0,
        'dashboard/binance_exact_layout.py': 0
    }
    
    total = 0
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    count = len(re.findall(r'@app\.callback', content))
                    files_to_check[file_path] = count
                    total += count
                    print(f"{file_path}: {count} callbacks")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f"{file_path}: FILE NOT FOUND")
    
    return total, files_to_check

def check_sidebar_elements():
    """Check sidebar elements in layout"""
    if os.path.exists('dashboard/layout.py'):
        try:
            with open('dashboard/layout.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            sidebar_elements = [
                'sidebar-symbol',
                'virtual-balance', 
                'reset-balance-btn',
                'reset-balance-btn-output'
            ]
            
            print("\nSIDEBAR ELEMENTS:")
            for element in sidebar_elements:
                if element in content:
                    print(f"✅ {element}")
                else:
                    print(f"❌ {element}")
        except Exception as e:
            print(f"Error checking sidebar: {e}")

def check_main_tabs():
    """Check main tabs"""
    if os.path.exists('dashboard/layout.py'):
        try:
            with open('dashboard/layout.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            tabs = [
                'Dashboard',
                'Auto Trading',
                'Futures Trading', 
                'Binance-Exact',
                'Email Config'
            ]
            
            print("\nMAIN TABS:")
            for tab in tabs:
                if tab in content:
                    print(f"✅ {tab}")
                else:
                    print(f"❌ {tab}")
        except Exception as e:
            print(f"Error checking tabs: {e}")

if __name__ == "__main__":
    print("📊 CALLBACK COUNT:")
    total, breakdown = count_callbacks()
    print(f"\nTOTAL: {total}/93 callbacks ({(total/93)*100:.1f}%)")
    
    check_sidebar_elements()
    check_main_tabs()
    
    print(f"\n🏆 FINAL STATUS:")
    if total >= 90:
        print("✅ Dashboard is near complete!")
    else:
        print(f"⚠️  Missing {93-total} callbacks")
