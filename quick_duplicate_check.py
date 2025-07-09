#!/usr/bin/env python3
"""
Quick Duplicate Checker - Find remaining active duplicates
"""

import re

def check_remaining_duplicates():
    layout_file = 'dashboardtest/layout.py'
    
    try:
        with open(layout_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print("Could not read layout.py")
        return
    
    # Find all non-commented id= lines
    lines = content.split('\n')
    active_ids = []
    
    for line_num, line in enumerate(lines, 1):
        # Skip commented lines
        if line.strip().startswith('#'):
            continue
        
        # Find id= patterns
        id_matches = re.findall(r'id=["\']([^"\']+)["\']', line)
        for id_match in id_matches:
            active_ids.append((id_match, line_num, line.strip()))
    
    # Count occurrences
    id_counts = {}
    for id_name, line_num, line_content in active_ids:
        if id_name not in id_counts:
            id_counts[id_name] = []
        id_counts[id_name].append((line_num, line_content))
    
    # Find duplicates
    duplicates = {id_name: occurrences for id_name, occurrences in id_counts.items() if len(occurrences) > 1}
    
    print("🔍 ACTIVE DUPLICATE CHECK")
    print("=" * 40)
    
    if duplicates:
        print(f"🚨 Found {len(duplicates)} active duplicates:")
        for id_name, occurrences in duplicates.items():
            print(f"\n   🆔 {id_name} ({len(occurrences)} times):")
            for line_num, line_content in occurrences:
                print(f"      Line {line_num}: {line_content[:60]}...")
    else:
        print("✅ No active duplicates found!")
    
    return len(duplicates)

if __name__ == "__main__":
    check_remaining_duplicates()
