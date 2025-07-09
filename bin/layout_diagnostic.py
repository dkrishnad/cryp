#!/usr/bin/env python3
"""
Simple layout diagnostic script.
"""

try:
    print("1. Testing basic imports...")
    import dash
    from dash import dcc, html
    import dash_bootstrap_components as dbc
    print("✓ Basic imports successful")
    
    print("2. Testing dashboard directory...")
    import os
    dashboard_dir = os.path.join(os.getcwd(), "dashboard")
    print(f"Dashboard directory: {dashboard_dir}")
    print(f"Directory exists: {os.path.exists(dashboard_dir)}")
    
    if os.path.exists(dashboard_dir):
        files = os.listdir(dashboard_dir)
        print(f"Files in dashboard: {files}")
    
    print("3. Testing layout.py syntax...")
    with open("dashboard/layout.py", "r") as f:
        content = f.read()
        
    # Count brackets
    open_brackets = content.count('[')
    close_brackets = content.count(']')
    open_parens = content.count('(')
    close_parens = content.count(')')
    
    print(f"Open brackets: {open_brackets}, Close brackets: {close_brackets}")
    print(f"Open parentheses: {open_parens}, Close parentheses: {close_parens}")
    
    if open_brackets != close_brackets:
        print("⚠️ Bracket mismatch detected!")
    else:
        print("✓ Brackets balanced")
        
    if open_parens != close_parens:
        print("⚠️ Parentheses mismatch detected!")
    else:
        print("✓ Parentheses balanced")
    
    print("4. Checking for syntax errors...")
    compile(content, "dashboard/layout.py", "exec")
    print("✓ No syntax errors found")
    
except SyntaxError as e:
    print(f"✗ Syntax error in layout.py: {e}")
    print(f"Line {e.lineno}: {e.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nDiagnostic complete!")
