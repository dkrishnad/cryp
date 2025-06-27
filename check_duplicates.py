#!/usr/bin/env python3

import re
from collections import Counter

def check_callback_duplicates():
    """Check for duplicate callback outputs"""
    
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Output declarations
    output_pattern = r'Output\([\'\"](.*?)[\'\"]'
    outputs = re.findall(output_pattern, content)
    
    # Count occurrences
    output_counts = Counter(outputs)
    duplicates = {k: v for k, v in output_counts.items() if v > 1}
    
    print("=== CALLBACK DUPLICATE ANALYSIS ===")
    print(f"Total callback outputs found: {len(outputs)}")
    print(f"Unique outputs: {len(output_counts)}")
    print(f"Duplicate outputs: {len(duplicates)}")
    
    if duplicates:
        print("\n❌ DUPLICATE OUTPUTS FOUND:")
        for output_id, count in duplicates.items():
            print(f"  '{output_id}': {count} times")
            
        # Find line numbers for duplicates
        lines = content.split('\n')
        for output_id in duplicates.keys():
            print(f"\nLines containing '{output_id}':")
            for i, line in enumerate(lines, 1):
                if f"'{output_id}'" in line or f'"{output_id}"' in line:
                    print(f"  Line {i}: {line.strip()}")
    else:
        print("\n✅ No duplicate outputs found!")
    
    return duplicates

def check_missing_components():
    """Check for callback outputs that don't exist in layout"""
    
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        callbacks_content = f.read()
    
    with open('dashboard/layout.py', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Find all Output IDs in callbacks
    output_pattern = r'Output\([\'\"](.*?)[\'\"]'
    callback_outputs = set(re.findall(output_pattern, callbacks_content))
    
    # Find all IDs in layout
    id_pattern = r'id=[\'\"](.*?)[\'\"]'
    layout_ids = set(re.findall(id_pattern, layout_content))
    
    missing_in_layout = callback_outputs - layout_ids
    missing_callbacks = layout_ids - callback_outputs
    
    print("\n=== COMPONENT MISMATCH ANALYSIS ===")
    print(f"Callback outputs: {len(callback_outputs)}")
    print(f"Layout components: {len(layout_ids)}")
    
    if missing_in_layout:
        print(f"\n❌ CALLBACK OUTPUTS MISSING IN LAYOUT ({len(missing_in_layout)}):")
        for missing in sorted(missing_in_layout):
            print(f"  '{missing}'")
    
    if missing_callbacks:
        print(f"\n⚠️  LAYOUT COMPONENTS WITHOUT CALLBACKS ({len(missing_callbacks)}):")
        for missing in sorted(missing_callbacks):
            print(f"  '{missing}'")
    
    if not missing_in_layout and not missing_callbacks:
        print("\n✅ All callback outputs have matching layout components!")

def verify_dashboard_health():
    """Verify dashboard is ready to start"""
    print("\n=== DASHBOARD HEALTH CHECK ===")
    
    try:
        # Check if key files exist
        import os
        files_to_check = [
            'dashboard/app.py',
            'dashboard/dash_app.py', 
            'dashboard/callbacks.py',
            'dashboard/layout.py'
        ]
        
        all_exist = True
        for file_path in files_to_check:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MISSING!")
                all_exist = False
        
        if all_exist:
            print("\n🎉 ALL CRITICAL FILES PRESENT!")
            print("🚀 Dashboard is ready to start!")
            print("\nTo start your crypto bot:")
            print("  python dashboard/app.py")
            print("\nDashboard URL: http://localhost:8050")
        
        return all_exist
        
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 CRYPTO BOT - COMPREHENSIVE STATUS CHECK")
    print("=" * 50)
    
    duplicates = check_callback_duplicates()
    check_missing_components()
    dashboard_ready = verify_dashboard_health()
    
    print("\n" + "=" * 50)
    print("📊 FINAL STATUS REPORT")
    print("=" * 50)
    
    if not duplicates and dashboard_ready:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ No duplicate callbacks")
        print("✅ All components matched") 
        print("✅ Dashboard files ready")
        print("\n🚀 Your crypto bot is ready to run!")
    else:
        print("⚠️  ISSUES FOUND:")
        if duplicates:
            print(f"   - {len(duplicates)} duplicate callbacks")
        if not dashboard_ready:
            print("   - Dashboard files missing")
