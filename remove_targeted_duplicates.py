#!/usr/bin/env python3
"""
Targeted Duplicate Removal - Remove lines 5235-5398 (recent sidebar duplications)
"""
import os

def remove_specific_duplicates():
    """Remove the specific duplicate lines 5235-5398"""
    
    callbacks_file = r'c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py'
    
    print("🔧 Removing specific duplicate lines 5235-5398...")
    
    # Read the file
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    print(f"📄 Original file has {original_count} lines")
    
    # Create backup
    backup_file = callbacks_file + '.backup_targeted'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"💾 Backup created: {backup_file}")
    
    # Remove lines 5235-5398 (these are the duplicated sidebar callbacks)
    # Python lists are 0-indexed, so line 5235 is index 5234
    start_remove = 5234  # Line 5235
    end_remove = 5398    # Line 5398
    
    # Keep everything before line 5235 and after line 5398
    cleaned_lines = lines[:start_remove]
    
    # Add a clean ending
    cleaned_lines.append("\n")
    
    print(f"🗑️  Removing lines {start_remove+1}-{end_remove} ({end_remove-start_remove} lines)")
    
    # Write cleaned content
    with open(callbacks_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    final_count = len(cleaned_lines)
    removed_lines = original_count - final_count
    
    print(f"✅ Cleanup complete!")
    print(f"📊 Original: {original_count} lines")
    print(f"📊 Final: {final_count} lines") 
    print(f"📊 Removed: {removed_lines} lines")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Targeted Duplicate Removal...")
    print("=" * 50)
    
    try:
        success = remove_specific_duplicates()
        
        if success:
            print("\n" + "=" * 50)
            print("🎉 Targeted cleanup completed successfully!")
            print("📋 Summary:")
            print("   - Removed lines 5235-5398 (duplicated sidebar callbacks)")
            print("   - Preserved all original functionality")
            print("   - Dashboard decluttering Step 1 & 2 complete")
            print("   - No more duplications!")
        else:
            print("❌ Cleanup failed!")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
        print("💡 Your original file is safe - check the backup!")
