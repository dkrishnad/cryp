#!/usr/bin/env python3
"""
COMPREHENSIVE PROBLEM DIAGNOSIS SCRIPT
=====================================
This script will identify ALL remaining issues in the crypto bot
"""

import os
import sys
import ast
import importlib
import traceback
import re
from collections import Counter

def check_syntax_all_files():
    """Check syntax of all Python files"""
    print("🔍 CHECKING SYNTAX OF ALL PYTHON FILES...")
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            print(f"✅ {file_path}")
        except SyntaxError as e:
            print(f"❌ {file_path} - SYNTAX ERROR: {e}")
            syntax_errors.append((file_path, str(e)))
        except Exception as e:
            print(f"⚠️  {file_path} - OTHER ERROR: {e}")
    
    return syntax_errors

def check_imports():
    """Check if all critical modules can be imported"""
    print("\n🔍 CHECKING CRITICAL IMPORTS...")
    
    critical_modules = [
        'dashboard.dash_app',
        'dashboard.app',
        'dashboard.callbacks',
        'dashboard.layout',
        'backend.main',
        'backend.db',
        'backend.data_collection',
        'backend.ws'
    ]
    
    import_errors = []
    for module in critical_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module} - ERROR: {e}")
            import_errors.append((module, str(e)))
    
    return import_errors

def check_callback_duplicates():
    """Check for duplicate callback outputs"""
    print("\n🔍 CHECKING CALLBACK DUPLICATES...")
    
    try:
        with open('dashboard/callbacks.py', 'r') as f:
            content = f.read()
        
        # Find all Output declarations
        output_pattern = r'Output\([\'\"](.*?)[\'\"]'
        outputs = re.findall(output_pattern, content)
        
        # Count occurrences
        output_counts = Counter(outputs)
        duplicates = {k: v for k, v in output_counts.items() if v > 1}
        
        print(f"Total outputs: {len(outputs)}")
        print(f"Unique outputs: {len(output_counts)}")
        
        if duplicates:
            print(f"❌ DUPLICATE OUTPUTS FOUND: {len(duplicates)}")
            for output_id, count in duplicates.items():
                print(f"  '{output_id}': {count} times")
            return duplicates
        else:
            print("✅ No duplicate outputs found")
            return {}
    except Exception as e:
        print(f"❌ Error checking duplicates: {e}")
        return {'error': str(e)}

def check_missing_components():
    """Check for callback outputs that don't exist in layout"""
    print("\n🔍 CHECKING MISSING COMPONENTS...")
    
    try:
        with open('dashboard/callbacks.py', 'r') as f:
            callbacks_content = f.read()
        
        with open('dashboard/layout.py', 'r') as f:
            layout_content = f.read()
        
        # Find all callback outputs
        output_pattern = r'Output\([\'\"](.*?)[\'\"]'
        callback_outputs = set(re.findall(output_pattern, callbacks_content))
        
        # Find all component IDs in layout
        id_pattern = r'id=[\'\"](.*?)[\'\"]'
        layout_ids = set(re.findall(id_pattern, layout_content))
        
        missing = callback_outputs - layout_ids
        
        if missing:
            print(f"❌ MISSING COMPONENTS: {len(missing)}")
            for component_id in missing:
                print(f"  '{component_id}' - referenced in callback but not in layout")
            return missing
        else:
            print("✅ All callback outputs have corresponding layout components")
            return set()
    except Exception as e:
        print(f"❌ Error checking components: {e}")
        return {'error': str(e)}

def check_indentation_issues():
    """Check for indentation issues"""
    print("\n🔍 CHECKING INDENTATION ISSUES...")
    
    problem_files = []
    for file_path in ['dashboard/callbacks.py', 'dashboard/app.py', 'dashboard/layout.py']:
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith('#'):
                    # Check for mixed spaces and tabs
                    if '\t' in line and '    ' in line:
                        print(f"❌ {file_path}:{i} - Mixed tabs and spaces")
                        problem_files.append((file_path, i, "Mixed tabs and spaces"))
                    
                    # Check for unusual indentation
                    leading_spaces = len(line) - len(line.lstrip(' \t'))
                    if leading_spaces > 0 and leading_spaces % 4 != 0 and '\t' not in line:
                        print(f"⚠️  {file_path}:{i} - Unusual indentation ({leading_spaces} spaces)")
            
            if file_path not in [p[0] for p in problem_files]:
                print(f"✅ {file_path}")
        except Exception as e:
            print(f"❌ {file_path} - ERROR: {e}")
            problem_files.append((file_path, 0, str(e)))
    
    return problem_files

def check_dashboard_startup():
    """Test dashboard startup components"""
    print("\n🔍 CHECKING DASHBOARD STARTUP...")
    
    startup_issues = []
    try:
        # Test dash app creation
        from dashboard.dash_app import app
        print("✅ Dash app creation OK")
        
        # Test layout import
        from dashboard.layout import layout
        print("✅ Layout import OK")
        
        # Test callbacks import
        import dashboard.callbacks
        print("✅ Callbacks import OK")
        
        # Test app layout assignment
        app.layout = layout
        print("✅ Layout assignment OK")
        
    except Exception as e:
        print(f"❌ Dashboard startup error: {e}")
        startup_issues.append(str(e))
        traceback.print_exc()
    
    return startup_issues

def check_backend_startup():
    """Test backend startup"""
    print("\n🔍 CHECKING BACKEND STARTUP...")
    
    backend_issues = []
    try:
        import backend.main
        print("✅ Backend main import OK")
        
        import backend.db
        print("✅ Backend database import OK")
        
        import backend.data_collection
        print("✅ Backend data collection import OK")
        
    except Exception as e:
        print(f"❌ Backend startup error: {e}")
        backend_issues.append(str(e))
        traceback.print_exc()
    
    return backend_issues

def main():
    print("=" * 60)
    print("🚨 COMPREHENSIVE PROBLEM DIAGNOSIS")
    print("=" * 60)
    
    all_issues = {}
    
    # Check syntax
    syntax_errors = check_syntax_all_files()
    if syntax_errors:
        all_issues['syntax_errors'] = syntax_errors
    
    # Check imports
    import_errors = check_imports()
    if import_errors:
        all_issues['import_errors'] = import_errors
    
    # Check callback duplicates
    duplicates = check_callback_duplicates()
    if duplicates:
        all_issues['callback_duplicates'] = duplicates
    
    # Check missing components
    missing_components = check_missing_components()
    if missing_components:
        all_issues['missing_components'] = missing_components
    
    # Check indentation
    indentation_issues = check_indentation_issues()
    if indentation_issues:
        all_issues['indentation_issues'] = indentation_issues
    
    # Check dashboard startup
    dashboard_issues = check_dashboard_startup()
    if dashboard_issues:
        all_issues['dashboard_startup'] = dashboard_issues
    
    # Check backend startup
    backend_issues = check_backend_startup()
    if backend_issues:
        all_issues['backend_startup'] = backend_issues
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if all_issues:
        print(f"❌ FOUND {len(all_issues)} TYPES OF ISSUES:")
        for issue_type, issues in all_issues.items():
            print(f"  - {issue_type}: {len(issues) if isinstance(issues, list) else 'Present'}")
        
        print(f"\n🔧 ISSUES TO FIX:")
        for issue_type, issues in all_issues.items():
            print(f"\n{issue_type.upper()}:")
            if isinstance(issues, list):
                for issue in issues:
                    print(f"  - {issue}")
            elif isinstance(issues, dict):
                for key, value in issues.items():
                    print(f"  - {key}: {value}")
            else:
                print(f"  - {issues}")
    else:
        print("🎉 NO ISSUES FOUND!")
        print("The crypto bot appears to be working correctly.")
    
    return all_issues

if __name__ == "__main__":
    main()
