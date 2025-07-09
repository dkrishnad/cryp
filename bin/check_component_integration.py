#!/usr/bin/env python3
"""
Check which callback component IDs are missing from dashboard layouts
"""
import re
import os

def extract_output_ids_from_callbacks(callbacks_file):
    """Extract all Output component IDs from callbacks.py"""
    output_ids = set()
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Output() patterns
    output_pattern = r"Output\s*\(\s*['\"]([^'\"]+)['\"]"
    matches = re.findall(output_pattern, content)
    output_ids.update(matches)
    
    # Also check for dcc.Store and other store IDs
    store_pattern = r"dcc\.Store\s*\(\s*id\s*=\s*['\"]([^'\"]+)['\"]"
    store_matches = re.findall(store_pattern, content)
    output_ids.update(store_matches)
    
    return output_ids

def extract_component_ids_from_layout(layout_file):
    """Extract all component IDs from a layout file"""
    component_ids = set()
    
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all id= patterns
    id_pattern = r'id\s*=\s*[\'"]([^\'"]+)[\'"]'
    matches = re.findall(id_pattern, content)
    component_ids.update(matches)
    
    # Also check for function calls like safe_graph("id", ...)
    function_id_pattern = r'safe_graph\s*\(\s*[\'"]([^\'"]+)[\'"]'
    function_matches = re.findall(function_id_pattern, content)
    component_ids.update(function_matches)
    
    return component_ids

def main():
    print("🔍 Checking Dashboard Component Integration")
    print("=" * 60)
    
    # Paths
    dashboard_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
    callbacks_file = os.path.join(dashboard_path, "callbacks.py")
    
    # Layout files to check
    layout_files = [
        "layout.py",
        "hybrid_learning_layout.py", 
        "auto_trading_layout.py",
        "futures_trading_layout.py",
        "binance_exact_layout.py",
        "email_config_layout.py"
    ]
    
    # Extract all Output IDs from callbacks
    try:
        callback_output_ids = extract_output_ids_from_callbacks(callbacks_file)
        print(f"📋 Found {len(callback_output_ids)} Output component IDs in callbacks.py")
        print()
    except Exception as e:
        print(f"❌ Error reading callbacks.py: {e}")
        return
    
    # Extract all component IDs from layout files
    all_layout_ids = set()
    layout_ids_by_file = {}
    
    for layout_file in layout_files:
        layout_path = os.path.join(dashboard_path, layout_file)
        if os.path.exists(layout_path):
            try:
                ids = extract_component_ids_from_layout(layout_path)
                layout_ids_by_file[layout_file] = ids
                all_layout_ids.update(ids)
                print(f"📄 {layout_file}: {len(ids)} component IDs")
            except Exception as e:
                print(f"❌ Error reading {layout_file}: {e}")
        else:
            print(f"⚠️  {layout_file}: File not found")
    
    print()
    print(f"📊 Total component IDs in all layouts: {len(all_layout_ids)}")
    print()
    
    # Find missing component IDs
    missing_ids = callback_output_ids - all_layout_ids
    
    if missing_ids:
        print("🚨 MISSING COMPONENT IDs in Layouts:")
        print("=" * 50)
        for missing_id in sorted(missing_ids):
            print(f"❌ {missing_id}")
        
        print()
        print("🔧 These components need to be added to the appropriate layout files!")
        
        # Group missing IDs by likely layout file
        print("\n📂 Suggested Layout File Additions:")
        print("-" * 40)
        
        # ML/AI related components
        ml_keywords = ['model', 'drift', 'learn', 'retrain', 'feature', 'analytics', 'prediction', 'ai', 'ml']
        auto_trading_keywords = ['auto', 'trading', 'futures', 'position']
        hybrid_keywords = ['hybrid', 'online', 'transfer', 'backtest']
        
        ml_missing = []
        auto_missing = []
        hybrid_missing = []
        other_missing = []
        
        for missing_id in sorted(missing_ids):
            lower_id = missing_id.lower()
            if any(keyword in lower_id for keyword in ml_keywords):
                ml_missing.append(missing_id)
            elif any(keyword in lower_id for keyword in auto_trading_keywords):
                auto_missing.append(missing_id)
            elif any(keyword in lower_id for keyword in hybrid_keywords):
                hybrid_missing.append(missing_id)
            else:
                other_missing.append(missing_id)
        
        if hybrid_missing:
            print(f"\n🧠 hybrid_learning_layout.py should add:")
            for comp_id in hybrid_missing:
                print(f"   • {comp_id}")
        
        if auto_missing:
            print(f"\n🤖 auto_trading_layout.py should add:")
            for comp_id in auto_missing:
                print(f"   • {comp_id}")
        
        if ml_missing:
            print(f"\n📊 layout.py (ML section) should add:")
            for comp_id in ml_missing:
                print(f"   • {comp_id}")
        
        if other_missing:
            print(f"\n🔧 Other/General layout.py should add:")
            for comp_id in other_missing:
                print(f"   • {comp_id}")
        
    else:
        print("✅ ALL COMPONENT IDs FOUND!")
        print("🎉 All callback outputs have corresponding UI components in the layouts.")
    
    print()
    print("📋 Component Analysis Summary:")
    print(f"  • Callback outputs: {len(callback_output_ids)}")
    print(f"  • Layout components: {len(all_layout_ids)}")
    print(f"  • Missing: {len(missing_ids)}")
    print(f"  • Integration: {((len(callback_output_ids) - len(missing_ids)) / len(callback_output_ids) * 100):.1f}%")

if __name__ == "__main__":
    main()
