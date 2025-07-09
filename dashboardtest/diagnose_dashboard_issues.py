#!/usr/bin/env python3
"""
Dashboard Callback Issues Detector
Identifies critical issues preventing callbacks from working
"""

import re
import os

def analyze_callbacks_file():
    """Analyze callbacks.py for critical issues"""
    issues = []
    
    try:
        with open("callbacks.py", "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [f"Could not read callbacks.py: {e}"]
    
    # Check for duplicate decorators
    duplicate_decorators = []
    for i, line in enumerate(lines, 1):
        if "@debug_callback" in line:
            if i < len(lines) and "@debug_callback" in lines[i]:
                duplicate_decorators.append(f"Line {i}: Duplicate @debug_callback decorator")
    
    if duplicate_decorators:
        issues.extend(duplicate_decorators)
    
    # Check for import issues
    import_issues = []
    for i, line in enumerate(lines, 1):
        if "from debug_logger import" in line or "import debug_logger" in line:
            # Check if debug_logger.py exists
            if not os.path.exists("debug_logger.py"):
                import_issues.append(f"Line {i}: debug_logger.py not found")
        if "from dash_app import app" in line:
            # Check if dash_app.py exists
            if not os.path.exists("dash_app.py"):
                import_issues.append(f"Line {i}: dash_app.py not found")
    
    if import_issues:
        issues.extend(import_issues)
    
    # Check for syntax issues
    syntax_issues = []
    try:
        compile(content, "callbacks.py", "exec")
    except SyntaxError as e:
        syntax_issues.append(f"Syntax Error at line {e.lineno}: {e.msg}")
    
    if syntax_issues:
        issues.extend(syntax_issues)
    
    # Check for callback registration issues
    callback_count = content.count("@app.callback")
    decorator_count = content.count("@debug_callback")
    
    if callback_count == 0:
        issues.append("No @app.callback decorators found")
    
    # Check for missing make_api_call function
    if "make_api_call" in content and "def make_api_call" not in content:
        # Check if it's imported
        if "from utils import make_api_call" not in content and "import utils" not in content:
            issues.append("make_api_call function used but not defined or imported")
    
    # Check for missing API_URL
    if "API_URL" in content and "API_URL =" not in content:
        issues.append("API_URL used but not defined")
    
    return issues

def analyze_app_startup():
    """Analyze app startup files for issues"""
    issues = []
    
    # Check app.py
    if os.path.exists("app.py"):
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                app_content = f.read()
            
            if "from callbacks import" not in app_content and "import callbacks" not in app_content:
                issues.append("app.py does not import callbacks")
            
            if "from layout import" not in app_content and "import layout" not in app_content:
                issues.append("app.py does not import layout")
                
        except Exception as e:
            issues.append(f"Could not read app.py: {e}")
    else:
        issues.append("app.py not found")
    
    # Check dash_app.py
    if os.path.exists("dash_app.py"):
        try:
            with open("dash_app.py", "r", encoding="utf-8") as f:
                dash_app_content = f.read()
            
            if "app = dash.Dash" not in dash_app_content:
                issues.append("dash_app.py does not create Dash app instance")
                
        except Exception as e:
            issues.append(f"Could not read dash_app.py: {e}")
    else:
        issues.append("dash_app.py not found")
    
    return issues

def main():
    print("Dashboard Issues Analysis")
    print("=" * 50)
    
    # Analyze callbacks
    print("\n1. Callbacks Analysis:")
    print("-" * 30)
    callback_issues = analyze_callbacks_file()
    if callback_issues:
        for issue in callback_issues:
            print(f"❌ {issue}")
    else:
        print("✅ No callback issues found")
    
    # Analyze app startup
    print("\n2. App Startup Analysis:")
    print("-" * 30)
    startup_issues = analyze_app_startup()
    if startup_issues:
        for issue in startup_issues:
            print(f"❌ {issue}")
    else:
        print("✅ No startup issues found")
    
    # Summary
    total_issues = len(callback_issues) + len(startup_issues)
    print(f"\n3. Summary:")
    print("-" * 30)
    print(f"Total Issues Found: {total_issues}")
    
    if total_issues > 0:
        print("\n🔧 Recommendations:")
        print("1. Fix duplicate decorators in callbacks.py")
        print("2. Ensure all import files exist")
        print("3. Check syntax errors")
        print("4. Verify API_URL and make_api_call function")
        print("5. Ensure proper app startup sequence")

if __name__ == "__main__":
    main()
