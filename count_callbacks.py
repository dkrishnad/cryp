#!/usr/bin/env python3
"""
Count actual functional callbacks in the dashboard
"""
import os

def count_callbacks_in_file(filepath):
    """Count @app.callback occurrences in a file"""
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count('@app.callback')
    except:
        return 0

def main():
    print("📊 FUNCTIONAL CALLBACK COUNT ANALYSIS")
    print("=" * 50)
    
    base_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
    
    # Count callbacks in functional files only
    functional_files = {
        "callbacks.py": "Main callbacks",
        "hybrid_learning_layout.py": "Hybrid Learning",
        "email_config_layout.py": "Email Config", 
        "binance_exact_callbacks.py": "Binance Exact",
        "futures_callbacks.py": "Futures",
        "auto_trading_layout.py": "Auto Trading",
        "futures_trading_layout.py": "Futures Trading"
    }
    
    total_callbacks = 0
    
    for file, description in functional_files.items():
        filepath = os.path.join(base_path, file)
        count = count_callbacks_in_file(filepath)
        total_callbacks += count
        status = "✅" if count > 0 else "❌"
        print(f"{status} {description:20} ({file:25}): {count:2d} callbacks")
    
    print("-" * 50)
    print(f"📊 TOTAL FUNCTIONAL CALLBACKS: {total_callbacks}")
    print(f"🎯 TARGET: 93+ callbacks")
    
    if total_callbacks >= 93:
        print("🎉 STATUS: TARGET REACHED!")
    elif total_callbacks >= 80:
        print("⚠️  STATUS: CLOSE TO TARGET")
    else:
        print("❌ STATUS: NEEDS MORE CALLBACKS")
    
    # Check if we need to add more callbacks from additional files
    additional_files = ["binance_exact_callbacks.py", "futures_callbacks.py"]
    
    print(f"\n🔍 CHECKING ADDITIONAL CALLBACK FILES:")
    for file in additional_files:
        filepath = os.path.join(base_path, file)
        if os.path.exists(filepath):
            count = count_callbacks_in_file(filepath)
            print(f"✅ {file}: {count} callbacks available")
        else:
            print(f"❌ {file}: Not found")

if __name__ == "__main__":
    main()
