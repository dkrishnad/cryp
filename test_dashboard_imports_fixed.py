#!/usr/bin/env python3
"""
Fixed Dashboard Import Test - No Path Issues
"""

import sys
import os
import subprocess

def test_dashboard_imports_safe():
    """Test dashboard imports safely using subprocess"""
    print("🔍 Testing dashboard imports (safe method)...")
    
    # Save current directory
    original_dir = os.getcwd()
    
    try:
        # Test by changing to dashboard directory and running subprocess
        os.chdir('dashboard')
        
        tests = [
            ('dash_app', 'from dash_app import app; print("dash_app OK")'),
            ('layout', 'from layout import layout; print("layout OK")'),
            ('callbacks', 'import callbacks; print("callbacks OK")')
        ]
        
        results = {}
        for name, cmd in tests:
            try:
                result = subprocess.run([sys.executable, '-c', cmd], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ {name}")
                    results[name] = True
                else:
                    print(f"❌ {name}: {result.stderr.strip()}")
                    results[name] = False
            except Exception as e:
                print(f"❌ {name}: {e}")
                results[name] = False
        
        return all(results.values())
        
    finally:
        os.chdir(original_dir)

def main():
    print("=" * 50)
    print("🧪 DASHBOARD IMPORT TEST (Fixed)")
    print("=" * 50)
    
    success = test_dashboard_imports_safe()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    
    if success:
        print("🎉 ALL IMPORTS SUCCESSFUL!")
        print("\n✅ Dashboard imports are working correctly!")
    else:
        print("❌ IMPORT ISSUES DETECTED!")
        print("Some dashboard modules failed to import.")

if __name__ == "__main__":
    main()
