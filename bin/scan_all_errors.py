#!/usr/bin/env python3
"""
Comprehensive Error Scanner - Find ALL remaining issues
"""

import os
import subprocess
import sys

def scan_all_python_files():
    """Scan all Python files for errors"""
    print("🔍 Scanning ALL Python files for errors...")
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip common non-essential directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.vscode', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    errors = []
    
    for file_path in python_files:
        try:
            # Check syntax
            result = subprocess.run([sys.executable, '-m', 'py_compile', file_path], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                errors.append({
                    'file': file_path,
                    'type': 'SYNTAX_ERROR',
                    'error': result.stderr.strip()
                })
                print(f"❌ SYNTAX: {file_path}")
                print(f"   {result.stderr.strip()}")
            else:
                print(f"✅ {file_path}")
        except Exception as e:
            errors.append({
                'file': file_path,
                'type': 'SCAN_ERROR', 
                'error': str(e)
            })
            print(f"⚠️  SCAN: {file_path} - {e}")
    
    return errors, python_files

def write_error_report(errors, total_files):
    """Write detailed error report"""
    with open('error_report.txt', 'w') as f:
        f.write("COMPREHENSIVE ERROR SCAN REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Python files scanned: {total_files}\n")
        f.write(f"Files with errors: {len(errors)}\n\n")
        
        if errors:
            f.write("DETAILED ERRORS:\n")
            f.write("-" * 30 + "\n")
            for i, error in enumerate(errors, 1):
                f.write(f"\n{i}. {error['file']}\n")
                f.write(f"   Type: {error['type']}\n")
                f.write(f"   Error: {error['error']}\n")
        else:
            f.write("🎉 NO ERRORS FOUND!\n")
    
    print(f"\nDetailed report written to: error_report.txt")

def main():
    print("=" * 60)
    print("🔍 COMPREHENSIVE ERROR SCANNER")
    print("=" * 60)
    
    errors, python_files = scan_all_python_files()
    
    print("\n" + "=" * 60)
    print("📊 SCAN RESULTS")
    print("=" * 60)
    print(f"Total files scanned: {len(python_files)}")
    print(f"Files with errors: {len(errors)}")
    
    if errors:
        print(f"\n❌ FOUND {len(errors)} FILES WITH ERRORS")
        error_types = {}
        for error in errors:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in error_types.items():
            print(f"   {error_type}: {count}")
    else:
        print("\n🎉 NO ERRORS FOUND!")
    
    write_error_report(errors, len(python_files))
    
    return len(errors)

if __name__ == "__main__":
    error_count = main()
    print(f"\nFinal error count: {error_count}")
