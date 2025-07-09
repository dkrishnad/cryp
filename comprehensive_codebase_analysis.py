#!/usr/bin/env python3
"""
Comprehensive codebase analysis to find missing, wrongly named, or non-existent:
- Functions
- Modules  
- Files
- Classes
- Methods
- Imports
"""

import os
import sys
import ast
import importlib.util
import traceback
import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path

def find_python_files(directory):
    """Find all Python files in directory and subdirectories"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip bin folders, virtual environments, cache dirs, and other non-project directories
        dirs[:] = [d for d in dirs if d not in [
            'bin', '__pycache__', '.git', 'node_modules', '.venv', 'venv', 
            'site-packages', '.pytest_cache', '.mypy_cache', 'dist', 'build'
        ]]
        
        # Also skip any directory that starts with a dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports_and_calls(file_path):
    """Extract all imports and function calls from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        imports = []
        function_calls = []
        class_instantiations = []
        attribute_accesses = []
        
        class Visitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node):
                for alias in node.names:
                    imports.append({
                        'type': 'from_import',
                        'module': node.module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
                self.generic_visit(node)
            
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    function_calls.append({
                        'name': node.func.id,
                        'line': node.lineno,
                        'type': 'direct_call'
                    })
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        function_calls.append({
                            'name': f"{node.func.value.id}.{node.func.attr}",
                            'line': node.lineno,
                            'type': 'method_call',
                            'object': node.func.value.id,
                            'method': node.func.attr
                        })
                self.generic_visit(node)
            
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name):
                    attribute_accesses.append({
                        'object': node.value.id,
                        'attribute': node.attr,
                        'line': node.lineno
                    })
                self.generic_visit(node)
        
        visitor = Visitor()
        visitor.visit(tree)
        
        return {
            'imports': imports,
            'function_calls': function_calls,
            'class_instantiations': class_instantiations,
            'attribute_accesses': attribute_accesses
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'imports': [],
            'function_calls': [],
            'class_instantiations': [],
            'attribute_accesses': []
        }

def check_module_exists(module_name, base_paths):
    """Check if a module exists in the given base paths"""
    for base_path in base_paths:
        # Check for .py file
        module_file = os.path.join(base_path, f"{module_name}.py")
        if os.path.exists(module_file):
            return True, module_file
        
        # Check for package directory
        package_dir = os.path.join(base_path, module_name)
        if os.path.isdir(package_dir):
            init_file = os.path.join(package_dir, "__init__.py")
            if os.path.exists(init_file):
                return True, package_dir
    
    return False, None

def check_function_exists_in_module(module_path, function_name):
    """Check if a function exists in a module"""
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return True
            elif isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == function_name:
                        return True
        
        return False
    except Exception:
        return False

def analyze_codebase():
    """Analyze the entire codebase for issues"""
    
    base_dir = r"c:\Users\Hari\Desktop\Testin dub"
    backend_dir = os.path.join(base_dir, "backendtest")
    dashboard_dir = os.path.join(base_dir, "dashboardtest")
    
    # Find all Python files
    python_files = find_python_files(base_dir)
    
    print(f"Found {len(python_files)} Python files to analyze")
    print("=" * 60)
    
    all_issues = {
        'missing_modules': [],
        'missing_functions': [],
        'missing_files': [],
        'import_errors': [],
        'syntax_errors': [],
        'critical_issues': []
    }
    
    # Base paths for module resolution
    base_paths = [base_dir, backend_dir, dashboard_dir]
    
    for file_path in python_files:
        print(f"\nAnalyzing: {os.path.relpath(file_path, base_dir)}")
        
        # Check syntax first
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, file_path, 'exec')
        except SyntaxError as e:
            all_issues['syntax_errors'].append({
                'file': file_path,
                'error': str(e),
                'line': e.lineno
            })
            print(f"  ❌ SYNTAX ERROR: Line {e.lineno}: {e}")
            continue
        except Exception as e:
            all_issues['syntax_errors'].append({
                'file': file_path,
                'error': str(e),
                'line': None
            })
            print(f"  ❌ COMPILE ERROR: {e}")
            continue
        
        # Extract imports and calls
        analysis = extract_imports_and_calls(file_path)
        
        if 'error' in analysis:
            print(f"  ⚠️  Analysis error: {analysis['error']}")
            continue
        
        # Check imports
        for imp in analysis['imports']:
            if imp['type'] == 'import':
                module_name = imp['module']
                exists, path = check_module_exists(module_name, base_paths)
                if not exists:
                    # Try standard library
                    try:
                        spec = importlib.util.find_spec(module_name)
                        if spec is None:
                            all_issues['missing_modules'].append({
                                'file': file_path,
                                'module': module_name,
                                'line': imp['line'],
                                'type': 'import'
                            })
                            print(f"  ❌ Missing module: {module_name} (line {imp['line']})")
                    except (ImportError, ModuleNotFoundError):
                        all_issues['missing_modules'].append({
                            'file': file_path,
                            'module': module_name,
                            'line': imp['line'],
                            'type': 'import'
                        })
                        print(f"  ❌ Missing module: {module_name} (line {imp['line']})")
            
            elif imp['type'] == 'from_import':
                module_name = imp['module']
                if module_name:
                    exists, module_path = check_module_exists(module_name, base_paths)
                    if exists and module_path and module_path.endswith('.py'):
                        # Check if the imported name exists in the module
                        if not check_function_exists_in_module(module_path, imp['name']):
                            all_issues['missing_functions'].append({
                                'file': file_path,
                                'module': module_name,
                                'function': imp['name'],
                                'line': imp['line']
                            })
                            print(f"  ❌ Missing function: {imp['name']} in {module_name} (line {imp['line']})")
                    elif not exists:
                        # Try standard library
                        try:
                            spec = importlib.util.find_spec(module_name)
                            if spec is None:
                                all_issues['missing_modules'].append({
                                    'file': file_path,
                                    'module': module_name,
                                    'line': imp['line'],
                                    'type': 'from_import'
                                })
                                print(f"  ❌ Missing module: {module_name} (line {imp['line']})")
                        except (ImportError, ModuleNotFoundError):
                            all_issues['missing_modules'].append({
                                'file': file_path,
                                'module': module_name,
                                'line': imp['line'],
                                'type': 'from_import'
                            })
                            print(f"  ❌ Missing module: {module_name} (line {imp['line']})")
        
        print(f"  ✅ Checked {len(analysis['imports'])} imports, {len(analysis['function_calls'])} function calls")
    
    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    
    total_issues = sum(len(issues) for issues in all_issues.values())
    
    if total_issues == 0:
        print("🎉 NO ISSUES FOUND! Codebase is clean.")
    else:
        print(f"Found {total_issues} total issues:")
        for category, issues in all_issues.items():
            if issues:
                print(f"\n{category.upper().replace('_', ' ')}: {len(issues)}")
                for issue in issues[:5]:  # Show first 5 of each type
                    if category == 'syntax_errors':
                        file_rel = os.path.relpath(issue['file'], base_dir)
                        print(f"  - {file_rel}: {issue['error']}")
                    elif category == 'missing_modules':
                        file_rel = os.path.relpath(issue['file'], base_dir)
                        print(f"  - {file_rel}:{issue['line']} - Missing module: {issue['module']}")
                    elif category == 'missing_functions':
                        file_rel = os.path.relpath(issue['file'], base_dir)
                        print(f"  - {file_rel}:{issue['line']} - Missing function: {issue['function']} in {issue['module']}")
                
                if len(issues) > 5:
                    print(f"  ... and {len(issues) - 5} more")
    
    # Save detailed report
    report_file = os.path.join(base_dir, "codebase_analysis_report.json")
    with open(report_file, 'w') as f:
        json.dump(all_issues, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return all_issues

if __name__ == "__main__":
    print("COMPREHENSIVE CODEBASE ANALYSIS")
    print("=" * 60)
    analyze_codebase()
