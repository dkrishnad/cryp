#!/usr/bin/env python3
"""
Complete Duplicate ID Resolver
Systematically fixes ALL duplicate IDs to prevent DuplicateIdError
"""

import re
import shutil
from datetime import datetime

def find_all_duplicate_ids():
    """Find ALL duplicate IDs across layout files"""
    
    files_to_check = [
        'dashboardtest/layout.py',
        'dashboardtest/auto_trading_layout.py', 
        'dashboardtest/futures_trading_layout.py',
        'dashboardtest/binance_exact_layout.py',
        'dashboardtest/email_config_layout.py',
        'dashboardtest/hybrid_learning_layout.py'
    ]
    
    all_ids = {}  # id -> [list of files containing it]
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all id= patterns
            id_matches = re.findall(r'id=["\']([^"\']+)["\']', content)
            
            for id_name in id_matches:
                if id_name not in all_ids:
                    all_ids[id_name] = []
                all_ids[id_name].append(file_path)
        
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    # Find duplicates
    duplicates = {}
    for id_name, files in all_ids.items():
        if len(files) > 1:
            duplicates[id_name] = files
    
    return duplicates

def fix_duplicate_in_layout(duplicate_id):
    """Remove a specific duplicate ID from layout.py"""
    
    layout_file = 'dashboardtest/layout.py'
    
    try:
        with open(layout_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading layout.py: {e}")
        return False
    
    # Find lines containing this ID
    lines = content.split('\n')
    modified_lines = []
    removed_count = 0
    
    for i, line in enumerate(lines):
        if f'id="{duplicate_id}"' in line or f"id='{duplicate_id}'" in line:
            # Comment out this line
            modified_lines.append(f'        # DUPLICATE_REMOVED: {line.strip()}')
            removed_count += 1
            print(f"   ✅ Removed: {line.strip()}")
        else:
            modified_lines.append(line)
    
    if removed_count > 0:
        # Write back the modified content
        try:
            with open(layout_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(modified_lines))
            return True
        except Exception as e:
            print(f"Error writing layout.py: {e}")
            return False
    
    return False

def resolve_all_duplicates():
    """Systematically resolve ALL duplicate IDs"""
    
    print("🔧 COMPLETE DUPLICATE ID RESOLVER")
    print("=" * 60)
    print("Step-by-step resolution of ALL DuplicateIdError issues")
    print("=" * 60)
    
    # Create backup first
    layout_file = 'dashboardtest/layout.py'
    backup_file = f'dashboardtest/layout_complete_fix_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    shutil.copy2(layout_file, backup_file)
    print(f"💾 Backup created: {backup_file}")
    
    # Find all duplicates
    print("🔍 Step 1: Finding ALL duplicate IDs...")
    duplicates = find_all_duplicate_ids()
    
    if not duplicates:
        print("✅ No duplicates found!")
        return True
    
    print(f"🚨 Found {len(duplicates)} duplicate IDs:")
    for id_name, files in duplicates.items():
        print(f"   - {id_name}: {len(files)} files")
    
    # Strategy: Remove duplicates from layout.py, keep in specialized files
    print(f"\n🎯 Step 2: Removing duplicates from layout.py...")
    
    # Focus on layout.py duplicates first
    layout_duplicates = [id_name for id_name, files in duplicates.items() 
                        if 'dashboardtest/layout.py' in files and len(files) > 1]
    
    print(f"🔧 Found {len(layout_duplicates)} IDs to remove from layout.py:")
    
    fixed_count = 0
    for duplicate_id in layout_duplicates:
        print(f"   🎯 Fixing: {duplicate_id}")
        if fix_duplicate_in_layout(duplicate_id):
            fixed_count += 1
        else:
            print(f"   ⚠️  Could not fix: {duplicate_id}")
    
    print(f"\n✅ Step 3: Complete!")
    print(f"📊 Fixed {fixed_count}/{len(layout_duplicates)} duplicates")
    print(f"💾 Backup: {backup_file}")
    
    # Verify fix
    print(f"\n🔍 Step 4: Verification...")
    remaining_duplicates = find_all_duplicate_ids()
    layout_remaining = [id_name for id_name, files in remaining_duplicates.items() 
                       if 'dashboardtest/layout.py' in files and len(files) > 1]
    
    if len(layout_remaining) == 0:
        print("🎉 SUCCESS: All layout.py duplicates resolved!")
        return True
    else:
        print(f"⚠️  Still {len(layout_remaining)} duplicates remaining:")
        for dup in layout_remaining[:5]:  # Show first 5
            print(f"   - {dup}")
        return False

def main():
    """Main execution"""
    success = resolve_all_duplicates()
    
    if success:
        print("\n🚀 DASHBOARD SHOULD NOW WORK!")
        print("Run: cd dashboardtest && python app.py")
    else:
        print("\n⚠️  Some duplicates remain. Manual intervention may be needed.")
    
    return success

if __name__ == "__main__":
    main()
