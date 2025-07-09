#!/usr/bin/env python3
"""
Find Duplicate Component IDs in Dashboard Layout Files
"""

import re
import os

def find_duplicate_ids():
    """Find all duplicate component IDs"""
    total_ids = {}
    duplicates = []
    
    # Check layout files
    layout_files = [
        'layout.py',
        'auto_trading_layout.py', 
        'futures_trading_layout.py',
        'binance_exact_layout.py',
        'email_config_layout.py',
        'hybrid_learning_layout.py'
    ]
    
    for file in layout_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find all id= patterns
                    ids = re.findall(r'id=["\']([^"\']+)["\']', content)
                    for id_name in ids:
                        if id_name in total_ids:
                            duplicates.append({
                                'id': id_name,
                                'file1': total_ids[id_name],
                                'file2': file
                            })
                            print(f"🚨 DUPLICATE ID: '{id_name}'")
                            print(f"   File 1: {total_ids[id_name]}")
                            print(f"   File 2: {file}")
                            print()
                        else:
                            total_ids[id_name] = file
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    print(f"📊 Total unique IDs: {len(total_ids)}")
    print(f"🚨 Duplicate IDs: {len(duplicates)}")
    
    return duplicates

if __name__ == "__main__":
    print("🔍 Checking for Duplicate Component IDs...")
    print("=" * 50)
    duplicates = find_duplicate_ids()
    
    if duplicates:
        print("\n❌ CRITICAL: Duplicate IDs found!")
        print("These must be fixed to resolve the DuplicateIdError")
    else:
        print("\n✅ No duplicate IDs found!")
