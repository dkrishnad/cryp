#!/usr/bin/env python3
"""
COMPREHENSIVE REDUNDANT FILES ANALYSIS & CLEANUP
Identifies the most advanced files and moves redundant ones to bin
"""

import os
import shutil
from datetime import datetime

def analyze_and_move_redundant_files():
    """Analyze files and move redundant ones to bin while keeping the most advanced versions"""
    
    print("🔍 COMPREHENSIVE REDUNDANT FILES ANALYSIS")
    print("=" * 60)
    
    moved_files = []
    kept_files = []
    
    # =========================================================================
    # CALLBACK FILES ANALYSIS
    # =========================================================================
    print("\n📋 CALLBACK FILES ANALYSIS:")
    print("-" * 40)
    
    # Most advanced callback file: callbacks.py (225,909 bytes - largest and most comprehensive)
    # Keep: callbacks.py, futures_callbacks.py, binance_exact_callbacks.py (specialized)
    # Move: All others are backups/refactored versions
    
    callback_files_to_move = [
        "dashboardtest/callbacks_backup_before_duplicate_fix.py",  # 105,795 bytes - backup
        "dashboardtest/refactoredcallback.py",                    # 68,754 bytes - refactored version
        "dashboardtest/refactored_callbacks_step1.py",            # 37,940 bytes - partial refactor
        "dashboardtest/refactored_callbacks_full.py",             # 0 bytes - empty
        "dashboardtest/final_fix_callbacks.py"                    # 0 bytes - empty
    ]
    
    callback_files_to_keep = [
        "dashboardtest/callbacks.py",                # 225,909 bytes - MOST ADVANCED
        "dashboardtest/futures_callbacks.py",        # 13,164 bytes - specialized futures
        "dashboardtest/binance_exact_callbacks.py"   # 18,240 bytes - specialized binance
    ]
    
    print("✅ KEEPING (Most Advanced):")
    for file in callback_files_to_keep:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   📁 {file} ({size:,} bytes)")
            kept_files.append(file)
    
    print("\n📦 MOVING TO BIN (Redundant):")
    for file in callback_files_to_move:
        if os.path.exists(file):
            size = os.path.getsize(file)
            target = f"bin/dashboard_redundant/{os.path.basename(file)}"
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            try:
                shutil.move(file, target)
                print(f"   ✅ {file} → {target} ({size:,} bytes)")
                moved_files.append(file)
            except Exception as e:
                print(f"   ❌ Failed to move {file}: {e}")
    
    # =========================================================================
    # APP FILES ANALYSIS  
    # =========================================================================
    print("\n📱 APP FILES ANALYSIS:")
    print("-" * 40)
    
    # Most advanced: app.py (main entry point), dash_app.py (configuration)
    # Move: fixed_app.py (alternative version)
    
    app_files_to_move = [
        "dashboardtest/fixed_app.py"  # 2,071 bytes - alternative version
    ]
    
    app_files_to_keep = [
        "dashboardtest/app.py",      # 3,003 bytes - MAIN ENTRY POINT
        "dashboardtest/dash_app.py"  # 853 bytes - essential config
    ]
    
    print("✅ KEEPING (Essential):")
    for file in app_files_to_keep:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   📁 {file} ({size:,} bytes)")
            kept_files.append(file)
    
    print("\n📦 MOVING TO BIN (Alternative):")
    for file in app_files_to_move:
        if os.path.exists(file):
            size = os.path.getsize(file)
            target = f"bin/dashboard_redundant/{os.path.basename(file)}"
            
            try:
                shutil.move(file, target)
                print(f"   ✅ {file} → {target} ({size:,} bytes)")
                moved_files.append(file)
            except Exception as e:
                print(f"   ❌ Failed to move {file}: {e}")
    
    # =========================================================================
    # LAYOUT FILES ANALYSIS
    # =========================================================================
    print("\n🎨 LAYOUT FILES ANALYSIS:")
    print("-" * 40)
    
    # All layout files are essential - no redundant ones found
    layout_files_to_keep = [
        "dashboardtest/layout.py",                    # 79,858 bytes - MAIN LAYOUT
        "dashboardtest/futures_trading_layout.py",   # 30,197 bytes - futures specific
        "dashboardtest/auto_trading_layout.py",      # 24,767 bytes - auto trading specific
        "dashboardtest/hybrid_learning_layout.py",   # 21,841 bytes - ML specific
        "dashboardtest/binance_exact_layout.py",     # 19,431 bytes - binance specific
        "dashboardtest/email_config_layout.py"       # 12,242 bytes - email specific
    ]
    
    print("✅ KEEPING (All Essential - No Redundancy Found):")
    for file in layout_files_to_keep:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   📁 {file} ({size:,} bytes)")
            kept_files.append(file)
    
    # =========================================================================
    # CHECK FOR OTHER REDUNDANT FILES
    # =========================================================================
    print("\n🔍 CHECKING FOR OTHER REDUNDANT FILES:")
    print("-" * 40)
    
    # Check for any other backup/redundant files in dashboardtest
    redundant_patterns = [
        "_backup", "_old", "_copy", "_test", "_debug", "_fixed", "_clean", 
        "_minimal", "_simple", "_working", "_temp", "_original"
    ]
    
    other_redundant = []
    for root, dirs, files in os.walk("dashboardtest"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                filename = os.path.basename(file)
                
                # Skip files we already processed
                if filepath.replace("\\", "/") in [f.replace("\\", "/") for f in kept_files + moved_files]:
                    continue
                
                # Check if it matches redundant patterns
                for pattern in redundant_patterns:
                    if pattern in filename.lower():
                        other_redundant.append(filepath)
                        break
    
    if other_redundant:
        print("📦 MOVING OTHER REDUNDANT FILES:")
        for file in other_redundant:
            if os.path.exists(file):
                size = os.path.getsize(file)
                target = f"bin/dashboard_redundant/{os.path.basename(file)}"
                
                try:
                    shutil.move(file, target)
                    print(f"   ✅ {file} → {target} ({size:,} bytes)")
                    moved_files.append(file)
                except Exception as e:
                    print(f"   ❌ Failed to move {file}: {e}")
    else:
        print("✅ No other redundant files found in dashboardtest")
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n📊 CLEANUP SUMMARY:")
    print("=" * 60)
    print(f"✅ Files Kept (Most Advanced): {len(kept_files)}")
    print(f"📦 Files Moved to Bin: {len(moved_files)}")
    
    # Create archive info
    archive_info = f"""# DASHBOARD REDUNDANT FILES ARCHIVE
## Created: {datetime.now().isoformat()}

This folder contains redundant dashboard files that were moved to avoid confusion:

### Callback Files (Redundant/Backup Versions):
- callbacks_backup_before_duplicate_fix.py (105,795 bytes) - Backup before fixes
- refactoredcallback.py (68,754 bytes) - Refactored version (superseded)
- refactored_callbacks_step1.py (37,940 bytes) - Partial refactor (incomplete)
- refactored_callbacks_full.py (0 bytes) - Empty file
- final_fix_callbacks.py (0 bytes) - Empty file

### App Files (Alternative Versions):
- fixed_app.py (2,071 bytes) - Alternative app version (superseded)

### Other Redundant Files:
{chr(10).join(f"- {os.path.basename(f)}" for f in other_redundant)}

## ACTIVE/ADVANCED FILES KEPT:
### Callbacks (Most Advanced):
- callbacks.py (225,909 bytes) - Main comprehensive callbacks
- futures_callbacks.py (13,164 bytes) - Specialized futures callbacks  
- binance_exact_callbacks.py (18,240 bytes) - Specialized Binance callbacks

### Apps (Essential):
- app.py (3,003 bytes) - Main entry point
- dash_app.py (853 bytes) - Essential Dash configuration

### Layouts (All Essential):
- layout.py (79,858 bytes) - Main comprehensive layout
- futures_trading_layout.py (30,197 bytes) - Futures-specific layout
- auto_trading_layout.py (24,767 bytes) - Auto trading layout
- hybrid_learning_layout.py (21,841 bytes) - ML/AI layout
- binance_exact_layout.py (19,431 bytes) - Binance-specific layout
- email_config_layout.py (12,242 bytes) - Email configuration layout

## REASON FOR ARCHIVING:
These files were moved to prevent confusion and maintain a clean development environment.
The active files contain the most advanced and comprehensive implementations.
"""
    
    with open("bin/dashboard_redundant/_ARCHIVE_INFO.md", "w") as f:
        f.write(archive_info)
    
    print(f"\n📄 Archive documentation created: bin/dashboard_redundant/_ARCHIVE_INFO.md")
    print("\n🎉 Dashboard file cleanup completed successfully!")
    
    return {
        "kept_files": kept_files,
        "moved_files": moved_files,
        "status": "success"
    }

if __name__ == "__main__":
    result = analyze_and_move_redundant_files()
    print(f"\n✅ Operation completed: {result['status']}")
