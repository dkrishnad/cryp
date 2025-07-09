#!/usr/bin/env python3
"""
Check for indentation and syntax issues in callbacks.py
"""

import ast
import sys

def check_syntax(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        print(f"✅ {filename} has valid Python syntax")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error in {filename}:")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error checking {filename}: {e}")
        return False

def check_indentation_issues(filename):
    """Check for common indentation problems"""
    issues = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Check for mixed tabs and spaces
            if '\t' in line and '    ' in line:
                issues.append(f"Line {i}: Mixed tabs and spaces")
            
            # Check for inconsistent indentation patterns
            if line.strip() and len(line) - len(line.lstrip()) % 4 != 0:
                # Allow some flexibility for continuation lines
                if not line.lstrip().startswith((')', ']', '}', 'except', 'elif', 'else', 'finally')):
                    stripped = line.lstrip()
                    if not (stripped.startswith('#') or '"""' in stripped or "'''" in stripped):
                        issues.append(f"Line {i}: Inconsistent indentation (not multiple of 4)")
        
        if issues:
            print(f"⚠️  Indentation issues in {filename}:")
            for issue in issues[:10]:  # Show first 10 issues
                print(f"   {issue}")
        else:
            print(f"✅ {filename} has consistent indentation")
            
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Error checking indentation in {filename}: {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        'dashboard/callbacks.py',
        'dashboard/app.py',
        'backend/main.py'
    ]
    
    all_good = True
    
    for filename in files_to_check:
        print(f"\nChecking {filename}...")
        syntax_ok = check_syntax(filename)
        indent_ok = check_indentation_issues(filename)
        
        if not syntax_ok or not indent_ok:
            all_good = False
    
    if all_good:
        print(f"\n🎉 All files are syntactically correct!")
    else:
        print(f"\n⚠️  Some files have issues that need fixing")
        
    sys.exit(0 if all_good else 1)
