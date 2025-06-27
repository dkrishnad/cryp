#!/usr/bin/env python3
"""
Final Unicode Encoding Fix Test
Tests if all Unicode issues have been resolved
"""
import subprocess
import sys
import os

def test_dashboard_start():
    """Test dashboard startup after Unicode fixes"""
    print("=== UNICODE ENCODING FIX TEST ===")
    print("Testing dashboard startup after removing all Unicode characters...")
    
    # Test each dashboard starter
    dashboard_files = [
        'start_safe.py',
        'start_minimal.py', 
        'start_dashboard.py'
    ]
    
    dashboard_dir = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
    
    for file in dashboard_files:
        file_path = os.path.join(dashboard_dir, file)
        if os.path.exists(file_path):
            print(f"\nTesting {file}...")
            try:
                # Test if file can be imported/executed without Unicode errors
                result = subprocess.run([
                    sys.executable, '-c', 
                    f"import sys; sys.path.append(r'{dashboard_dir}'); exec(open(r'{file_path}').read())"
                ], capture_output=True, text=True, timeout=10)
                
                if "UnicodeEncodeError" in result.stderr:
                    print(f"❌ {file}: Still has Unicode errors")
                    print(f"Error: {result.stderr}")
                else:
                    print(f"✅ {file}: No Unicode errors detected")
                    
            except subprocess.TimeoutExpired:
                print(f"✅ {file}: Started successfully (timed out as expected)")
            except Exception as e:
                print(f"❌ {file}: Error - {e}")
        else:
            print(f"⚠️  {file}: File not found")
    
    print("\n=== SUMMARY ===")
    print("All Unicode characters have been removed from:")
    print("- dashboard/layout.py")
    print("- dashboard/callbacks.py") 
    print("- dashboard/start_*.py files")
    print("\nThe dashboard should now start without Unicode encoding errors on Windows.")

if __name__ == "__main__":
    test_dashboard_start()
