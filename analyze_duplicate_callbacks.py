#!/usr/bin/env python3
"""
Analyze duplicate callback outputs in dashboard/callbacks.py
"""
import re
from collections import defaultdict

def analyze_callbacks():
    """Analyze callbacks.py for duplicate outputs and other issues"""
    
    print("🔍 Analyzing dashboard/callbacks.py for duplicate outputs...")
    
    with open(r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @app.callback decorators and their outputs
    callback_pattern = r'@app\.callback\s*\(\s*(.*?)\s*\)\s*def\s+(\w+)'
    callbacks = re.findall(callback_pattern, content, re.DOTALL)
    
    # Track outputs
    output_tracker = defaultdict(list)
    callback_info = []
    
    for i, (callback_args, func_name) in enumerate(callbacks):
        # Extract Output statements
        output_pattern = r'Output\([\'"]([^\'\"]+)[\'"],\s*[\'"]([^\'\"]+)[\'"](?:,\s*allow_duplicate=([^)]+))?\)'
        outputs = re.findall(output_pattern, callback_args)
        
        callback_data = {
            'function': func_name,
            'callback_num': i + 1,
            'outputs': outputs,
            'has_allow_duplicate': any('allow_duplicate' in callback_args for _ in outputs)
        }
        callback_info.append(callback_data)
        
        # Track each output
        for output_id, output_prop, allow_dup in outputs:
            output_key = f"{output_id}.{output_prop}"
            output_tracker[output_key].append({
                'function': func_name,
                'callback_num': i + 1,
                'allow_duplicate': bool(allow_dup)
            })
    
    print(f"📊 Found {len(callbacks)} total callbacks")
    
    # Find duplicates
    duplicates = {k: v for k, v in output_tracker.items() if len(v) > 1}
    
    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicate outputs:")
        for output_key, callbacks_list in duplicates.items():
            print(f"\n🔴 DUPLICATE: {output_key}")
            for cb in callbacks_list:
                allow_dup_str = " (allow_duplicate=True)" if cb['allow_duplicate'] else ""
                print(f"   - Callback #{cb['callback_num']}: {cb['function']}{allow_dup_str}")
    else:
        print("✅ No duplicate outputs found!")
    
    # Check for common problematic patterns
    print("\n🔍 Checking for common issues...")
    
    # Check for commented duplicates
    if "# Duplicate callback removed" in content:
        commented_count = content.count("# Duplicate callback removed")
        print(f"ℹ️  Found {commented_count} comments about removed duplicates")
    
    # Check for problematic futures outputs
    futures_outputs = [k for k in output_tracker.keys() if 'futures-' in k]
    if futures_outputs:
        print(f"🎯 Found {len(futures_outputs)} futures-related outputs")
        
        # Check for specific problematic patterns
        problematic = []
        for output in futures_outputs:
            if len(output_tracker[output]) > 1:
                problematic.append(output)
        
        if problematic:
            print(f"   ❌ {len(problematic)} have duplicates: {', '.join(problematic)}")
    
    # Check for missing allow_duplicate flags
    needs_allow_duplicate = []
    for output_key, callbacks_list in duplicates.items():
        for cb in callbacks_list:
            if not cb['allow_duplicate']:
                needs_allow_duplicate.append((output_key, cb['function']))
    
    if needs_allow_duplicate:
        print(f"\n🔧 Callbacks that need allow_duplicate=True:")
        for output_key, func_name in needs_allow_duplicate:
            print(f"   - {func_name}: {output_key}")
    
    return duplicates, callback_info

if __name__ == "__main__":
    duplicates, callback_info = analyze_callbacks()
    
    print(f"\n📈 Analysis Summary:")
    print(f"   - Total callbacks: {len(callback_info)}")
    print(f"   - Duplicate outputs: {len(duplicates)}")
    
    if duplicates:
        print(f"\n🎯 Top priority fixes needed:")
        for i, (output_key, callbacks_list) in enumerate(list(duplicates.items())[:10]):
            print(f"   {i+1}. {output_key} ({len(callbacks_list)} duplicates)")
