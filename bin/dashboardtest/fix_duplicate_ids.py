#!/usr/bin/env python3
"""
Fix duplicate callback output IDs by removing conflicting hidden divs
"""
import re

def fix_duplicate_ids():
    """Remove duplicate hidden divs from layout.py that conflict with tab layouts"""
    
    # IDs that should be removed from hidden divs because they exist in tab layouts
    duplicate_ids = [
        'futures-total-balance',
        'futures-virtual-balance', 
        'futures-trading-controls',
        'futures-positions-table',
        'futures-history-table',
        'futures-settings-result',
        'futures-trade-result',
        'email-config-status',
        'online-learning-status',
        'data-collection-status'
    ]
    
    print("🔧 Fixing duplicate callback output IDs...")
    
    # Read the layout file
    with open('layout.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    removed_count = 0
    
    # Remove each duplicate hidden div
    for div_id in duplicate_ids:
        pattern = f'\\s*html\\.Div\\(id="{div_id}", style={{\"display\": \"none\"}}\\),\\s*\n'
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            print(f"✅ Removed hidden div: {div_id}")
            removed_count += 1
        else:
            print(f"⚠️ Hidden div not found: {div_id}")
    
    # Write the fixed content back
    with open('layout.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📊 SUMMARY:")
    print(f"Removed {removed_count} duplicate hidden divs")
    print(f"This should fix the 'Duplicate callback outputs' errors")

if __name__ == "__main__":
    print("=== FIXING DUPLICATE CALLBACK OUTPUTS ===")
    fix_duplicate_ids()
    print("\n✅ DUPLICATE ID FIX COMPLETE!")
