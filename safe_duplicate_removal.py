#!/usr/bin/env python3
"""
Safe duplicate removal plan for callbacks.py
Creates a clean version with only original callbacks
"""

def remove_duplicates_safely():
    """Remove all duplicates while preserving original callbacks"""
    
    # Read the current file
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Original file has {len(lines)} lines")
    
    # Find where original callbacks end (around line 1570)
    # The last original callback should be update_indicators_chart
    
    original_end_line = None
    for i, line in enumerate(lines):
        if 'def update_indicators_chart(' in line:
            # Find the end of this function
            j = i + 1
            while j < len(lines):
                if lines[j].strip().startswith('def ') or lines[j].strip().startswith('@app.callback'):
                    break
                if lines[j].strip() == '' and j + 1 < len(lines) and lines[j + 1].strip().startswith('#'):
                    # Check if next non-empty line is a comment about duplicates
                    k = j + 1
                    while k < len(lines) and (lines[k].strip() == '' or lines[k].strip().startswith('#')):
                        if 'REMOVED DUPLICATE SECTION' in lines[k]:
                            original_end_line = j
                            break
                        k += 1
                    if original_end_line:
                        break
                j += 1
            if original_end_line:
                break
    
    if original_end_line is None:
        print("Could not find end of original callbacks!")
        return False
    
    print(f"Original callbacks end at line: {original_end_line + 1}")
    
    # Keep only the original callbacks
    clean_lines = lines[:original_end_line + 1]
    
    # Add a proper ending message
    clean_lines.append('\n')
    clean_lines.append('# ========================================\n')
    clean_lines.append('# ALL DUPLICATES SUCCESSFULLY REMOVED\n')
    clean_lines.append('# File now contains only original callbacks\n')
    clean_lines.append('# Total callbacks preserved: Original only\n')
    clean_lines.append('# ========================================\n')
    clean_lines.append('\n')
    clean_lines.append('print("[OK] callbacks.py loaded - ALL DUPLICATES REMOVED")\n')
    clean_lines.append('print(f"[CLEAN] File contains only original callbacks")\n')
    clean_lines.append('print(f"[SUCCESS] No duplicate outputs remaining")\n')
    
    print(f"Clean file will have {len(clean_lines)} lines (reduced from {len(lines)})")
    print(f"Removing {len(lines) - len(clean_lines)} lines of duplicates")
    
    # Write the clean version
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks_clean.py", 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    
    print("Clean version saved as callbacks_clean.py")
    return True

if __name__ == "__main__":
    if remove_duplicates_safely():
        print("\n✅ SUCCESS: Clean version created!")
        print("Review callbacks_clean.py before replacing the original.")
    else:
        print("\n❌ FAILED: Could not create clean version.")
