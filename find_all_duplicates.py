#!/usr/bin/env python3
"""
Comprehensive Duplicate ID Checker
Systematically finds all duplicate IDs across layout files
"""

import re
import os
from collections import defaultdict

def extract_all_ids_from_file(filepath):
    """Extract all component IDs from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all id= patterns, excluding commented lines
        lines = content.split('\n')
        ids = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip commented lines
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # Find id patterns
            id_matches = re.findall(r'id=["\']([^"\']+)["\']', line)
            for id_match in id_matches:
                ids.append({
                    'id': id_match,
                    'line': line_num,
                    'line_content': line.strip(),
                    'file': os.path.basename(filepath)
                })
        
        return ids
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def find_all_duplicates():
    """Find all duplicate IDs across all layout files"""
    
    layout_files = [
        'dashboardtest/layout.py',
        'dashboardtest/auto_trading_layout.py', 
        'dashboardtest/futures_trading_layout.py',
        'dashboardtest/binance_exact_layout.py',
        'dashboardtest/email_config_layout.py',
        'dashboardtest/hybrid_learning_layout.py'
    ]
    
    # Collect all IDs
    all_ids = defaultdict(list)
    
    for filepath in layout_files:
        if os.path.exists(filepath):
            file_ids = extract_all_ids_from_file(filepath)
            for id_info in file_ids:
                all_ids[id_info['id']].append(id_info)
    
    # Find duplicates
    duplicates = {}
    for id_name, occurrences in all_ids.items():
        if len(occurrences) > 1:
            duplicates[id_name] = occurrences
    
    return duplicates, all_ids

def main():
    print("🔍 COMPREHENSIVE DUPLICATE ID ANALYSIS")
    print("=" * 60)
    
    duplicates, all_ids = find_all_duplicates()
    
    print(f"📊 SUMMARY:")
    print(f"   Total unique IDs: {len(all_ids)}")
    print(f"   Duplicate IDs: {len(duplicates)}")
    print(f"   Files analyzed: 6")
    
    if duplicates:
        print(f"\n🚨 DUPLICATE IDs FOUND: {len(duplicates)}")
        print("=" * 60)
        
        # Sort duplicates by priority (layout.py duplicates first)
        layout_duplicates = []
        other_duplicates = []
        
        for id_name, occurrences in duplicates.items():
            has_layout_duplicate = any(occ['file'] == 'layout.py' for occ in occurrences)
            if has_layout_duplicate:
                layout_duplicates.append((id_name, occurrences))
            else:
                other_duplicates.append((id_name, occurrences))
        
        # Show layout.py duplicates first (highest priority)
        if layout_duplicates:
            print("🔴 HIGH PRIORITY - layout.py duplicates:")
            for id_name, occurrences in layout_duplicates[:10]:  # Show first 10
                print(f"\n   🆔 {id_name}")
                for occ in occurrences:
                    status = "🔴" if occ['file'] == 'layout.py' else "🟢"
                    print(f"      {status} {occ['file']}:{occ['line']} - {occ['line_content'][:80]}...")
        
        # Show other duplicates
        if other_duplicates:
            print(f"\n🟡 MEDIUM PRIORITY - Other duplicates: {len(other_duplicates)}")
            for id_name, occurrences in other_duplicates[:5]:  # Show first 5
                print(f"\n   🆔 {id_name}")
                for occ in occurrences:
                    print(f"      📁 {occ['file']}:{occ['line']}")
        
        print(f"\n🎯 FIXING STRATEGY:")
        print(f"   1. Comment out duplicates in layout.py (keep specialized files)")
        print(f"   2. Focus on HIGH PRIORITY duplicates first")
        print(f"   3. Test after each batch of fixes")
        
        # Generate fix commands
        print(f"\n🔧 RECOMMENDED FIXES:")
        fix_count = 0
        for id_name, occurrences in layout_duplicates:
            layout_occurrences = [occ for occ in occurrences if occ['file'] == 'layout.py']
            if layout_occurrences:
                for occ in layout_occurrences:
                    print(f"   Comment out line {occ['line']} in layout.py: {id_name}")
                    fix_count += 1
                    if fix_count >= 20:  # Limit output
                        print(f"   ... and {len(layout_duplicates) - fix_count} more")
                        break
                if fix_count >= 20:
                    break
        
    else:
        print("✅ NO DUPLICATES FOUND!")
        print("The DuplicateIdError should be resolved.")
    
    return duplicates

if __name__ == "__main__":
    duplicates = main()
    if duplicates:
        print(f"\n💡 Run this script regularly to track progress!")
    else:
        print(f"\n🚀 Ready to test dashboard!")
