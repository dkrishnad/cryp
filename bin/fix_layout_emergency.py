#!/usr/bin/env python3
"""
Emergency layout backup and fix
"""
import os
import shutil

def backup_and_fix_layout():
    """Backup current layout and create a working version"""
    
    # Backup original
    if os.path.exists("dashboard/layout.py"):
        shutil.copy("dashboard/layout.py", "dashboard/layout_backup.py")
        print("✓ Original layout backed up to layout_backup.py")
    
    # Copy our fixed version
    if os.path.exists("dashboard/layout_fixed.py"):
        shutil.copy("dashboard/layout_fixed.py", "dashboard/layout.py")
        print("✓ Fixed layout copied to layout.py")
    
    print("✅ Layout fix completed!")

if __name__ == "__main__":
    backup_and_fix_layout()
