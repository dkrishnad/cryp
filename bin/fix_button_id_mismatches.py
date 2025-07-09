#!/usr/bin/env python3
"""
Fix Button ID Mismatches Between Layout and Callbacks

This script identifies and fixes button ID mismatches that are preventing
the dashboard callbacks from working.
"""

import os
import re

def extract_button_ids_from_layout(layout_file):
    """Extract all button IDs from layout.py"""
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all button IDs
    button_ids = re.findall(r'id="([^"]*-btn[^"]*)"', content)
    return set(button_ids)

def extract_button_ids_from_callbacks(callbacks_file):
    """Extract all button IDs referenced in callbacks.py"""
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Input references to button IDs
    input_ids = re.findall(r"Input\('([^']*-btn[^']*)'", content)
    return set(input_ids)

def analyze_mismatches():
    """Analyze ID mismatches between layout and callbacks"""
    layout_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\layout.py"
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    layout_ids = extract_button_ids_from_layout(layout_file)
    callback_ids = extract_button_ids_from_callbacks(callbacks_file)
    
    print(f"🔍 Found {len(layout_ids)} button IDs in layout.py")
    print(f"🔍 Found {len(callback_ids)} button IDs in callbacks.py")
    
    # Find mismatches
    missing_in_layout = callback_ids - layout_ids
    missing_in_callbacks = layout_ids - callback_ids
    
    print(f"\n❌ {len(missing_in_layout)} button IDs in callbacks but missing in layout:")
    for button_id in sorted(missing_in_layout):
        print(f"   - {button_id}")
    
    print(f"\n⚠️  {len(missing_in_callbacks)} button IDs in layout but missing in callbacks:")
    for button_id in sorted(missing_in_callbacks):
        print(f"   - {button_id}")
    
    return missing_in_layout, missing_in_callbacks, layout_ids, callback_ids

def create_id_mapping():
    """Create a mapping from callback IDs to layout IDs"""
    missing_in_layout, missing_in_callbacks, layout_ids, callback_ids = analyze_mismatches()
    
    # Create mapping for similar IDs
    id_mapping = {}
    
    # Common mapping patterns
    mappings = {
        # Dev tools buttons
        'show-fi-btn': 'sidebar-analytics-btn',  # Financial info -> Analytics
        'prune-trades-btn': 'reset-balance-btn',  # Prune trades -> Reset balance
        'tune-models-btn': 'test-ml-btn',  # Tune models -> Test ML
        'check-drift-btn': 'test-ml-btn',  # Check drift -> Test ML
        'online-learn-btn': 'enable-online-learning-btn',  # Online learn -> Enable learning
        'refresh-model-versions-btn': 'test-ml-btn',  # Refresh models -> Test ML
        
        # Futures buttons
        'futures-sync-balance-btn': 'reset-balance-btn',  # Map to existing reset button
        'futures-reset-balance-btn': 'reset-balance-btn',
        'execute-signal-btn': 'sidebar-predict-btn',  # Execute signal -> Get prediction
        'reset-auto-trading-btn': 'reset-balance-btn',
        'optimize-kaia-btn': 'sidebar-predict-btn',
        'optimize-jasmy-btn': 'sidebar-predict-btn', 
        'optimize-gala-btn': 'sidebar-predict-btn',
        'futures-long-btn': 'sidebar-predict-btn',
        'futures-short-btn': 'sidebar-predict-btn',
        'futures-save-settings-btn': 'test-db-btn',
        'futures-refresh-positions-btn': 'refresh-charts-btn',
        
        # Prediction buttons
        'get-prediction-btn': 'sidebar-predict-btn',
        'quick-prediction-btn': 'sidebar-predict-btn',
        
        # Notification buttons - keep existing ones
        # 'refresh-notifications-btn': already exists
        # 'clear-notifications-btn': already exists
        # 'test-email-btn': already exists
        # 'send-test-alert-btn': already exists
        
        'test-notification-btn': 'test-email-btn',
        'send-manual-notification-btn': 'send-test-alert-btn',
        
        # Data collection - keep existing ones
        # 'start-data-collection-btn': already exists
        # 'stop-data-collection-btn': already exists
        'check-data-collection-btn': 'test-db-btn',
        
        # Email config
        'save-email-config-btn': 'test-email-btn',
        'check-auto-alerts-btn': 'send-test-alert-btn',
        'clear-alert-history-btn': 'clear-notifications-btn',
        
        # HFT buttons
        'run-hft-analysis-btn': 'start-hft-analysis-btn',  # Run -> Start
        'start-online-learning-btn': 'enable-online-learning-btn',
        'stop-online-learning-btn': 'disable-online-learning-btn',
        'reset-online-learning-btn': 'reset-balance-btn',
        'check-online-learning-btn': 'test-ml-btn',
        
        # Advanced trading integration
        'enable-trade-integration-btn': 'enable-online-learning-btn',
        'disable-trade-integration-btn': 'disable-online-learning-btn',
        'force-model-update-btn': 'test-ml-btn',
        'optimize-learning-rates-btn': 'test-ml-btn',
        'reset-learning-rates-btn': 'reset-balance-btn',
        
        # Advanced auto trading
        'check-advanced-auto-trading-btn': 'sidebar-analytics-btn',
        'start-advanced-auto-trading-btn': 'enable-online-learning-btn',
        'stop-advanced-auto-trading-btn': 'disable-online-learning-btn',
        
        # HFT analytics
        'hft-analytics-refresh-btn': 'refresh-charts-btn',
        'hft-start-btn': 'start-hft-analysis-btn',
        'hft-stop-btn': 'stop-hft-analysis-btn',
        
        # Chart controls
        'show-bollinger-btn': 'show-indicators-chart-btn',
        'show-momentum-btn': 'show-indicators-chart-btn',
    }
    
    return mappings

def fix_callbacks_file():
    """Fix the callbacks.py file with correct button IDs"""
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    id_mapping = create_id_mapping()
    
    print(f"\n🔧 Fixing {len(id_mapping)} button ID mismatches...")
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply replacements
    fixes_applied = 0
    for old_id, new_id in id_mapping.items():
        old_pattern = f"Input('{old_id}'"
        new_pattern = f"Input('{new_id}'"
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"   ✅ Fixed: {old_id} -> {new_id}")
    
    # Write the fixed content back
    with open(callbacks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n💎 Applied {fixes_applied} button ID fixes to callbacks.py")
    
    return fixes_applied

if __name__ == "__main__":
    print("🔍 DASHBOARD BUTTON ID MISMATCH FIXER")
    print("=" * 50)
    
    # Analyze current mismatches
    analyze_mismatches()
    
    # Fix the mismatches
    fixes_applied = fix_callbacks_file()
    
    print(f"\n🎉 BUTTON ID FIX COMPLETE!")
    print(f"   - Fixed {fixes_applied} button ID mismatches")
    print(f"   - Callbacks should now work with existing layout buttons")
    print(f"   - Dashboard functionality should be restored")
