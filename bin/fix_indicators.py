#!/usr/bin/env python3
"""
Fix the last endpoint mismatch
"""

import re

def fix_features_indicators():
    """Fix /features/indicators?symbol= calls"""
    frontend_file = "dashboardtest/callbacks.py"
    
    with open(frontend_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the query string format with params format
    old_pattern = r'f"{API_URL}/features/indicators\?symbol=\{([^}]+)\}"'
    new_pattern = r'f"{API_URL}/features/indicators", params={"symbol": \1}'
    
    content = re.sub(old_pattern, new_pattern, content)
    
    # Also fix the case with timeout
    old_pattern2 = r'f"{API_URL}/features/indicators\?symbol=\{([^}]+)\}", timeout=(\d+)'
    new_pattern2 = r'f"{API_URL}/features/indicators", params={"symbol": \1}, timeout=\2'
    
    content = re.sub(old_pattern2, new_pattern2, content)
    
    with open(frontend_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed /features/indicators endpoint calls")
    print("   Changed query string format to params format")

if __name__ == "__main__":
    fix_features_indicators()
