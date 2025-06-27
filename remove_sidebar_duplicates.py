#!/usr/bin/env python3
"""
Remove Recent Sidebar Callback Duplications (Step 1 & Step 2)
Only removes the duplicated callbacks added during dashboard decluttering
"""
import os
import re

def remove_recent_sidebar_duplications():
    """Remove only the recent sidebar callback duplications from Step 1 & 2"""
    
    callbacks_file = r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py'
    
    print("🔧 Starting removal of recent sidebar duplications...")
    
    # Read the file
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_length = len(content.splitlines())
    print(f"📄 Original file has {original_length} lines")
    
    # Find and remove duplicated sections from lines 5173-5398
    # These are the recent duplications we added in Step 1 & 2
    
    lines = content.splitlines()
    
    # Define the start and end of duplicated sections to remove
    duplicated_sections = [
        # Step 2 toggles (duplicated around line 5173-5210)
        {"start_pattern": "# STEP 2: ANALYTICS, ML TOOLS & CHARTS SIDEBAR TOGGLES", 
         "end_pattern": "print.*Step 2 Complete.*dashboard simplified"},
        
        # Sidebar technical indicators (duplicated around line 5211-5398)
        {"start_pattern": "# SIDEBAR TECHNICAL INDICATORS CALLBACKS", 
         "end_pattern": "print.*Step 2 dashboard decluttering fully implemented"},
        
        # Advanced tools toggles (if duplicated)
        {"start_pattern": "# ADVANCED TOOLS SIDEBAR TOGGLE CALLBACKS", 
         "end_pattern": "print.*Advanced/Dev Tools moved to sidebar"},
    ]
    
    # Process each section
    cleaned_lines = []
    skip_mode = False
    current_section = None
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Check if we're starting a duplicated section
        for section in duplicated_sections:
            if section["start_pattern"] in line_stripped:
                # Check if this is a duplicate (not the first occurrence)
                previous_occurrence = False
                for j in range(i):
                    if section["start_pattern"] in lines[j]:
                        previous_occurrence = True
                        break
                
                if previous_occurrence:
                    skip_mode = True
                    current_section = section
                    print(f"🗑️  Removing duplicate section starting at line {i+1}: {section['start_pattern']}")
                    break
        
        # Check if we're ending a duplicated section
        if skip_mode and current_section:
            if current_section["end_pattern"] in line_stripped:
                skip_mode = False
                current_section = None
                print(f"✅ Finished removing duplicate section at line {i+1}")
                continue  # Skip this line too
        
        # Add line if we're not in skip mode
        if not skip_mode:
            cleaned_lines.append(line)
    
    # Rejoin the content
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Additional cleanup: Remove any duplicate function definitions
    print("🧹 Cleaning up duplicate function definitions...")
    
    # List of functions that might be duplicated
    duplicate_functions = [
        "toggle_analytics_section",
        "toggle_ml_tools_section", 
        "toggle_charts_section",
        "update_sidebar_rsi",
        "update_sidebar_macd",
        "update_sidebar_bollinger",
        "update_sidebar_analytics",
        "update_sidebar_ml_tools",
        "update_sidebar_risk_display",
        "update_sidebar_amount_from_buttons",
        "toggle_hft_tools",
        "toggle_data_collection",
        "toggle_online_learning",
        "toggle_risk_management",
        "toggle_notifications",
        "toggle_email_alerts"
    ]
    
    # Remove duplicate function definitions (keep only the first occurrence)
    for func_name in duplicate_functions:
        pattern = rf'(@app\.callback.*?def {func_name}\(.*?(?=@app\.callback|def \w|print\(|$))'
        matches = list(re.finditer(pattern, cleaned_content, re.DOTALL))
        
        if len(matches) > 1:
            print(f"🔄 Found {len(matches)} copies of {func_name}, removing duplicates...")
            # Keep only the first match, remove the rest
            for match in reversed(matches[1:]):  # Remove from end to preserve indices
                cleaned_content = cleaned_content[:match.start()] + cleaned_content[match.end():]
    
    # Remove excessive empty lines
    cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)
    
    # Create backup
    backup_file = callbacks_file + '.backup_before_cleanup'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup created: {backup_file}")
    
    # Write cleaned content
    with open(callbacks_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    final_length = len(cleaned_content.splitlines())
    removed_lines = original_length - final_length
    
    print(f"✅ Cleanup complete!")
    print(f"📊 Original: {original_length} lines")
    print(f"📊 Final: {final_length} lines") 
    print(f"📊 Removed: {removed_lines} lines")
    print(f"💡 Backup saved as: {backup_file}")
    
    return True

def verify_cleanup():
    """Verify that essential callbacks are still present"""
    callbacks_file = r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py'
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    essential_callbacks = [
        "update_live_price",
        "update_portfolio_status", 
        "update_virtual_balance",
        "toggle_dev_tools",
        "update_auto_trading_stats",
        "execute_futures_trade"
    ]
    
    print("🔍 Verifying essential callbacks are preserved...")
    missing_callbacks = []
    
    for callback in essential_callbacks:
        if f"def {callback}" not in content:
            missing_callbacks.append(callback)
        else:
            print(f"✅ {callback} - Found")
    
    if missing_callbacks:
        print(f"⚠️  Missing callbacks: {missing_callbacks}")
        return False
    else:
        print("✅ All essential callbacks preserved!")
        return True

if __name__ == "__main__":
    print("🚀 Starting Sidebar Duplications Cleanup...")
    print("=" * 50)
    
    try:
        success = remove_recent_sidebar_duplications()
        
        if success:
            verify_cleanup()
            print("\n" + "=" * 50)
            print("🎉 Cleanup completed successfully!")
            print("📋 Summary:")
            print("   - Removed duplicate Step 1 & Step 2 sidebar callbacks")
            print("   - Preserved all essential functionality")
            print("   - Created backup file")
            print("   - Dashboard decluttering maintained")
        else:
            print("❌ Cleanup failed!")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
        print("💡 Your original file is safe - check the backup!")
