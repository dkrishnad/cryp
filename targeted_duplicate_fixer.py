#!/usr/bin/env python3
"""
Targeted Duplicate ID Fixer
Specifically targets the duplicate IDs causing DuplicateIdError
Uses a surgical approach to remove only redundant duplicates
"""

import re
import shutil
from datetime import datetime

def fix_specific_duplicates():
    """Fix the specific duplicate IDs that are causing the DuplicateIdError"""
    
    print("🎯 TARGETED DUPLICATE ID FIXER")
    print("=" * 50)
    print("Fixing only the specific duplicates causing DuplicateIdError")
    print("=" * 50)
    
    layout_file = 'dashboardtest/layout.py'
    
    # Read the layout file
    try:
        with open(layout_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {layout_file}: {e}")
        return False
    
    # Create backup
    backup_file = f'dashboardtest/layout_targeted_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    shutil.copy2(layout_file, backup_file)
    print(f"💾 Backup created: {backup_file}")
    
    # High-priority duplicates that are definitely causing issues
    critical_duplicates = [
        'auto-rollback-status',
        'auto-trading-tab-content',
        'futures-trading-tab-content', 
        'binance-exact-tab-content',
        'email-config-tab-content',
        'hybrid-learning-tab-content',
        'futures-available-balance',
        'auto-trading-toggle-output',
        'auto-symbol-dropdown'
    ]
    
    modified_content = content
    fixed_count = 0
    
    print(f"🔧 Targeting {len(critical_duplicates)} critical duplicate IDs...")
    
    for dup_id in critical_duplicates:
        print(f"   🎯 Fixing: {dup_id}")
        
        # Find all occurrences of this ID
        pattern = rf'(.*?id=["\']?{re.escape(dup_id)}["\']?.*?)(?=\n|$)'
        matches = list(re.finditer(pattern, modified_content, re.MULTILINE))
        
        if len(matches) > 1:
            print(f"      Found {len(matches)} occurrences")
            
            # Strategy: Keep the first occurrence, comment out others
            for i in range(len(matches) - 1, 0, -1):  # Work backwards to preserve positions
                match = matches[i]
                original_line = match.group(1)
                
                # Skip if already commented
                if original_line.strip().startswith('#'):
                    continue
                
                # Comment out this duplicate
                commented_line = f'# DUPLICATE_FIXED: {original_line.strip()}'
                
                # Replace in content
                start, end = match.span()
                modified_content = (modified_content[:start] + 
                                  commented_line + 
                                  modified_content[end:])
                fixed_count += 1
                print(f"      ✅ Commented out duplicate #{i}")
        else:
            print(f"      ⚠️  Only {len(matches)} occurrence(s) found")
    
    # Additional fix: Look for function definitions that might be duplicated
    function_duplicates = [
        'create_auto_trading_layout',
        'create_futures_trading_layout',
        'create_binance_exact_layout',
        'create_email_config_layout',
        'create_hybrid_learning_layout'
    ]
    
    print(f"\n🔧 Checking for duplicate function definitions...")
    
    for func_name in function_duplicates:
        pattern = rf'^def {re.escape(func_name)}\('
        matches = list(re.finditer(pattern, modified_content, re.MULTILINE))
        
        if len(matches) > 1:
            print(f"   🎯 Found {len(matches)} definitions of {func_name}")
            
            # Comment out all but the first definition
            for i in range(len(matches) - 1, 0, -1):
                match = matches[i]
                
                # Find the entire function (until next def or end of file)
                start_pos = match.start()
                lines = modified_content[start_pos:].split('\n')
                func_lines = []
                
                for j, line in enumerate(lines):
                    func_lines.append(line)
                    
                    # Stop at next function definition or end
                    if j > 0 and (line.startswith('def ') or line.startswith('class ') or 
                                 (line.strip() and not line.startswith(' ') and not line.startswith('\t'))):
                        break
                    
                    # Safety break
                    if j > 100:
                        break
                
                # Comment out the entire function
                commented_func = '\n'.join([f'# DUPLICATE_FUNC_REMOVED: {line}' for line in func_lines[:-1]])
                original_func = '\n'.join(func_lines[:-1])
                
                modified_content = modified_content.replace(original_func, commented_func)
                fixed_count += 1
                print(f"      ✅ Commented out duplicate function definition #{i}")
    
    # Write the fixed content
    try:
        with open(layout_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(f"\n✅ Targeted fix completed!")
        print(f"📊 Total fixes applied: {fixed_count}")
        print(f"💾 Backup saved: {backup_file}")
        print(f"🔄 To rollback: cp {backup_file} {layout_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing fixed file: {e}")
        # Restore backup
        shutil.copy2(backup_file, layout_file)
        print(f"🔄 Restored from backup")
        return False

if __name__ == "__main__":
    success = fix_specific_duplicates()
    if success:
        print("\n🚀 Try running the dashboard now!")
        print("   cd dashboardtest && python app.py")
    else:
        print("\n❌ Fix failed. Original file restored.")
