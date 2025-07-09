#!/usr/bin/env python3
"""
Fixed Comprehensive Codebase Analysis Tool
Performs accurate deep dive analysis of the entire crypto trading bot application
"""

import os
import sys
import ast
import re
import json
import sqlite3
import traceback
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
import importlib.util

class FixedComprehensiveAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'root_path': str(self.root_path),
            'files_analyzed': [],
            'missing_files': [],
            'existing_files': [],
            'import_errors': [],
            'syntax_errors': [],
            'buttons_and_callbacks': {},
            'api_endpoints': {},
            'database_analysis': {},
            'functionality_map': {},
            'dependencies': {},
            'security_issues': [],
            'performance_issues': [],
            'code_quality': {}
        }
        
    def run_complete_analysis(self):
        """Run comprehensive analysis with improved file detection"""
        print(f"🔍 Starting APPLICATION-FOCUSED analysis from: {self.root_path}")
        
        # 1. Verify root path exists
        if not self.root_path.exists():
            print(f"❌ Root path does not exist: {self.root_path}")
            return self.analysis_results
            
        print(f"✅ Root path verified: {self.root_path}")
        
        # 2. Check for critical files first
        self.check_critical_files()
        
        # 3. Analyze APPLICATION file structure only
        self.analyze_file_structure_fixed()
        
        # 4. Trace actual application usage
        self.trace_application_usage()
        
        # 5. Analyze Python files with better error handling (only used files)
        self.analyze_python_files_fixed()
        
        # 6. Check imports and dependencies
        self.check_imports_and_dependencies()
        
        # 7. Analyze dashboard components
        self.analyze_dashboard_components_fixed()
        
        # 8. Analyze backend API endpoints
        self.analyze_backend_endpoints_fixed()
        
        # 9. Check database files
        self.analyze_database_files()
        
        # 10. Generate comprehensive report
        self.generate_fixed_report()
        
        return self.analysis_results
    
    def check_critical_files(self):
        """Check for existence of critical application files"""
        print("🔍 Checking critical files...")
        
        critical_files = [
            "main.py",
            "dashboardtest/app.py",
            "dashboardtest/layout.py", 
            "dashboardtest/callbacks.py",
            "backendtest/main.py",
            "backendtest/app.py",
            "backendtest/data_collection.py",
            "backendtest/ml.py",
            "backendtest/futures_trading.py",
            "backendtest/online_learning.py",
            "backendtest/advanced_auto_trading.py"
        ]
        
        for file_path in critical_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                self.analysis_results['existing_files'].append({
                    'path': file_path,
                    'full_path': str(full_path),
                    'size': full_path.stat().st_size,
                    'modified': datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
                })
                print(f"  ✅ {file_path}")
            else:
                self.analysis_results['missing_files'].append(file_path)
                print(f"  ❌ {file_path}")
    
    def analyze_file_structure_fixed(self):
        """Analyze ONLY files used by the active application"""
        print("📁 Analyzing APPLICATION files only (excluding .venv, bin, etc.)...")
        
        try:
            # Define application directories only
            app_directories = [
                "dashboardtest",
                "backendtest"
            ]
            
            # Include root level application files
            root_app_files = [
                "main.py"
            ]
            
            python_files = []
            
            # Get files from application directories
            for app_dir in app_directories:
                app_path = self.root_path / app_dir
                if app_path.exists():
                    py_files_in_dir = list(app_path.rglob("*.py"))
                    python_files.extend(py_files_in_dir)
            
            # Add root level application files
            for root_file in root_app_files:
                root_path = self.root_path / root_file
                if root_path.exists():
                    python_files.append(root_path)
            
            # Get database files (application level only)
            db_files = [
                self.root_path / "trades.db",
                self.root_path / "data.db"
            ]
            db_files = [f for f in db_files if f.exists()]
            
            # Get configuration files
            config_files = [
                self.root_path / "requirements.txt",
                self.root_path / "config.json"
            ]
            config_files = [f for f in config_files if f.exists()]
            
            print(f"📊 Found APPLICATION files:")
            print(f"  🐍 Python files: {len(python_files)}")
            print(f"  🗄️  Database files: {len(db_files)}")
            print(f"  ⚙️  Config files: {len(config_files)}")
            
            # Analyze each APPLICATION Python file
            for py_file in python_files:
                try:
                    relative_path = py_file.relative_to(self.root_path)
                    stat = py_file.stat()
                    
                    self.analysis_results['files_analyzed'].append({
                        'path': str(relative_path),
                        'full_path': str(py_file),
                        'type': '.py',
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'category': 'application'
                    })
                except Exception as e:
                    print(f"⚠️  Error analyzing {py_file}: {e}")
            
            # Add database files to analysis
            for db_file in db_files:
                try:
                    relative_path = db_file.relative_to(self.root_path)
                    stat = db_file.stat()
                    
                    self.analysis_results['files_analyzed'].append({
                        'path': str(relative_path),
                        'full_path': str(db_file),
                        'type': '.db',
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'category': 'database'
                    })
                except Exception as e:
                    print(f"⚠️  Error analyzing {db_file}: {e}")
                    
        except Exception as e:
            print(f"❌ Error in file structure analysis: {e}")
    
    def analyze_python_files_fixed(self):
        """Analyze Python files with improved error handling"""
        print("🐍 Analyzing Python files (improved)...")
        
        python_files = [f for f in self.analysis_results['files_analyzed'] if f['type'] == '.py']
        
        for file_info in python_files:
            file_path = Path(file_info['full_path'])
            self.analyze_single_python_file_fixed(file_path)
    
    def analyze_single_python_file_fixed(self, file_path: Path):
        """Analyze a single Python file with better error handling"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            relative_path = file_path.relative_to(self.root_path)
            file_key = str(relative_path)
            
            # Initialize analysis for this file
            if file_key not in self.analysis_results['functionality_map']:
                self.analysis_results['functionality_map'][file_key] = {
                    'functions': [],
                    'classes': [],
                    'imports': [],
                    'api_endpoints': [],
                    'callbacks': [],
                    'syntax_valid': True,
                    'import_errors': []
                }
            
            # Check syntax
            try:
                ast.parse(content)
                self.analysis_results['functionality_map'][file_key]['syntax_valid'] = True
            except SyntaxError as e:
                self.analysis_results['syntax_errors'].append({
                    'file': file_key,
                    'error': str(e),
                    'line': e.lineno
                })
                self.analysis_results['functionality_map'][file_key]['syntax_valid'] = False
                print(f"❌ Syntax error in {file_key}: {e}")
                return
            
            # Analyze imports
            self.analyze_imports_in_file(content, file_key)
            
            # Analyze functions and classes
            self.analyze_functions_and_classes_in_file(content, file_key)
            
            # Check for API endpoints
            self.check_api_endpoints_in_file(content, file_key)
            
            # Check for callbacks
            self.check_callbacks_in_file(content, file_key)
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            self.analysis_results['import_errors'].append({
                'file': str(file_path.relative_to(self.root_path)),
                'error': str(e)
            })
    
    def analyze_imports_in_file(self, content: str, file_key: str):
        """Analyze imports in a file"""
        import_patterns = [
            r'import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import',
        ]
        
        imports = set()
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            imports.update(matches)
        
        self.analysis_results['functionality_map'][file_key]['imports'] = list(imports)
    
    def analyze_functions_and_classes_in_file(self, content: str, file_key: str):
        """Analyze functions and classes in a file"""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'decorators': []
                    }
                    
                    # Check decorators safely
                    for decorator in node.decorator_list:
                        try:
                            decorator_name = ast.unparse(decorator) if hasattr(ast, 'unparse') else str(type(decorator).__name__)
                            func_info['decorators'].append(decorator_name)
                        except Exception:
                            # Skip decorators we can't parse safely
                            func_info['decorators'].append("<unparseable>")
                    
                    self.analysis_results['functionality_map'][file_key]['functions'].append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'methods': []
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append({
                                'name': item.name,
                                'line': item.lineno
                            })
                    
                    self.analysis_results['functionality_map'][file_key]['classes'].append(class_info)
                    
        except Exception as e:
            print(f"⚠️  Error parsing AST for {file_key}: {e}")
    
    def check_api_endpoints_in_file(self, content: str, file_key: str):
        """Check for API endpoints in a file"""
        endpoint_patterns = [
            r'@app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'\"]+)[\'"]',
            r'@router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'\"]+)[\'"]',
            r'@bp\.(route)\s*\(\s*[\'"]([^\'\"]+)[\'"]'
        ]
        
        endpoints = []
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match) >= 2:
                    endpoints.append({
                        'method': match[0].upper(),
                        'path': match[1]
                    })
        
        if endpoints:
            self.analysis_results['api_endpoints'][file_key] = endpoints
            self.analysis_results['functionality_map'][file_key]['api_endpoints'] = endpoints
    
    def check_callbacks_in_file(self, content: str, file_key: str):
        """Check for Dash callbacks in a file"""
        callback_patterns = [
            r'@app\.callback\s*\(\s*([^)]+)\s*\)',
            r'def\s+(\w*callback\w*)\s*\(',
            r'Output\s*\(\s*[\'"]([^\'\"]+)[\'"]',
            r'Input\s*\(\s*[\'"]([^\'\"]+)[\'"]'
        ]
        
        callbacks = []
        for pattern in callback_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            callbacks.extend(matches)
        
        if callbacks:
            self.analysis_results['buttons_and_callbacks'][file_key] = callbacks
            self.analysis_results['functionality_map'][file_key]['callbacks'] = callbacks
    
    def check_imports_and_dependencies(self):
        """Check if imports can be resolved"""
        print("📦 Checking imports and dependencies...")
        
        for file_key, file_info in self.analysis_results['functionality_map'].items():
            imports = file_info.get('imports', [])
            
            for import_name in imports:
                try:
                    # Try to find the module
                    if import_name.startswith('.'):
                        # Relative import - skip for now
                        continue
                    
                    # Check if it's a local module
                    local_module_path = self.root_path / f"{import_name.replace('.', '/')}.py"
                    if local_module_path.exists():
                        continue
                    
                    # Check if it's a standard library or installed package
                    try:
                        spec = importlib.util.find_spec(import_name)
                        if spec is None:
                            file_info['import_errors'].append(f"Cannot find module: {import_name}")
                    except (ImportError, ModuleNotFoundError, ValueError):
                        file_info['import_errors'].append(f"Import error: {import_name}")
                        
                except Exception as e:
                    file_info['import_errors'].append(f"Error checking {import_name}: {str(e)}")
    
    def analyze_dashboard_components_fixed(self):
        """Analyze dashboard components with improved detection"""
        print("🎛️  Analyzing dashboard components...")
        
        dashboard_files = [
            'dashboardtest/layout.py',
            'dashboardtest/callbacks.py',
            'dashboardtest/app.py'
        ]
        
        for file_path in dashboard_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                self.analyze_dashboard_file(full_path)
    
    def analyze_dashboard_file(self, file_path: Path):
        """Analyze a dashboard file for components"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_key = str(file_path.relative_to(self.root_path))
            
            # Find buttons
            button_patterns = [
                r'dbc\.Button\s*\([^)]*id\s*=\s*[\'"]([^\'\"]+)[\'"]',
                r'html\.Button\s*\([^)]*id\s*=\s*[\'"]([^\'\"]+)[\'"]',
                r'id\s*=\s*[\'"]([^\'\"]*button[^\'\"]*)[\'"]',
                r'id\s*=\s*[\'"]([^\'\"]*-btn[^\'\"]*)[\'"]'
            ]
            
            buttons = set()
            for pattern in button_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                buttons.update(matches)
            
            # Find callback components
            callback_patterns = [
                r'Output\s*\(\s*[\'"]([^\'\"]+)[\'"]',
                r'Input\s*\(\s*[\'"]([^\'\"]+)[\'"]',
                r'State\s*\(\s*[\'"]([^\'\"]+)[\'"]'
            ]
            
            callback_components = set()
            for pattern in callback_patterns:
                matches = re.findall(pattern, content)
                callback_components.update(matches)
            
            if file_key not in self.analysis_results['buttons_and_callbacks']:
                self.analysis_results['buttons_and_callbacks'][file_key] = {}
            
            self.analysis_results['buttons_and_callbacks'][file_key].update({
                'buttons': list(buttons),
                'callback_components': list(callback_components)
            })
            
        except Exception as e:
            print(f"❌ Error analyzing dashboard file {file_path}: {e}")
    
    def analyze_backend_endpoints_fixed(self):
        """Analyze backend API endpoints with improved detection"""
        print("🌐 Analyzing backend endpoints...")
        
        backend_files = [
            'backendtest/main.py',
            'backendtest/app.py'
        ]
        
        for file_path in backend_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                self.analyze_backend_file(full_path)
    
    def analyze_backend_file(self, file_path: Path):
        """Analyze a backend file for API endpoints"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_key = str(file_path.relative_to(self.root_path))
            
            # Find API endpoints
            endpoint_patterns = [
                r'@app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'\"]+)[\'"]',
                r'@router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'\"]+)[\'"]'
            ]
            
            endpoints = []
            for pattern in endpoint_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                for method, path in matches:
                    endpoints.append({
                        'method': method.upper(),
                        'path': path
                    })
            
            if endpoints:
                self.analysis_results['api_endpoints'][file_key] = endpoints
                print(f"  📡 {file_key}: {len(endpoints)} endpoints")
                
        except Exception as e:
            print(f"❌ Error analyzing backend file {file_path}: {e}")
    
    def analyze_database_files(self):
        """Analyze database files"""
        print("🗄️  Analyzing database files...")
        
        db_files = list(self.root_path.rglob("*.db"))
        
        for db_file in db_files:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                db_info = {
                    'file': str(db_file.relative_to(self.root_path)),
                    'size': db_file.stat().st_size,
                    'tables': {}
                }
                
                for table in tables:
                    table_name = table[0]
                    
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    row_count = cursor.fetchone()[0]
                    
                    db_info['tables'][table_name] = {
                        'columns': len(columns),
                        'row_count': row_count
                    }
                
                conn.close()
                self.analysis_results['database_analysis'][str(db_file)] = db_info
                print(f"  📊 {db_file.name}: {len(tables)} tables")
                
            except Exception as e:
                print(f"❌ Error analyzing database {str(db_file)}: {e}")
    
    def generate_fixed_report(self):
        """Generate comprehensive fixed report"""
        print("📊 Generating comprehensive report...")
        
        report_path = self.root_path / 'FIXED_COMPREHENSIVE_ANALYSIS_REPORT.md'
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# 🔧 FIXED COMPREHENSIVE CODEBASE ANALYSIS REPORT\n\n")
                f.write(f"**Generated:** {self.analysis_results['timestamp']}\n")
                f.write(f"**Root Path:** {self.analysis_results['root_path']}\n\n")
                
                # Executive Summary
                f.write("## 📋 EXECUTIVE SUMMARY\n\n")
                f.write(f"- **Total Files Analyzed:** {len(self.analysis_results['files_analyzed'])}\n")
                f.write(f"- **Existing Critical Files:** {len(self.analysis_results['existing_files'])}\n")
                f.write(f"- **Missing Critical Files:** {len(self.analysis_results['missing_files'])}\n")
                f.write(f"- **Syntax Errors:** {len(self.analysis_results['syntax_errors'])}\n")
                f.write(f"- **API Endpoints Found:** {sum(len(endpoints) for endpoints in self.analysis_results['api_endpoints'].values())}\n")
                f.write(f"- **Database Files:** {len(self.analysis_results['database_analysis'])}\n\n")
                
                # Critical Files Status
                f.write("## ✅ CRITICAL FILES STATUS\n\n")
                f.write("### Existing Files:\n")
                for file_info in self.analysis_results['existing_files']:
                    f.write(f"- ✅ **{file_info['path']}** ({file_info['size']} bytes)\n")
                
                if self.analysis_results['missing_files']:
                    f.write("\n### Missing Files:\n")
                    for missing_file in self.analysis_results['missing_files']:
                        f.write(f"- ❌ **{missing_file}**\n")
                f.write("\n")
                
                # Syntax Errors
                if self.analysis_results['syntax_errors']:
                    f.write("## 🚨 SYNTAX ERRORS\n\n")
                    for error in self.analysis_results['syntax_errors']:
                        f.write(f"- **{error['file']}** (line {error['line']}): {error['error']}\n")
                    f.write("\n")
                else:
                    f.write("## ✅ NO SYNTAX ERRORS FOUND\n\n")
                
                # API Endpoints
                f.write("## 🌐 API ENDPOINTS\n\n")
                for file_path, endpoints in self.analysis_results['api_endpoints'].items():
                    f.write(f"### {file_path}\n")
                    for endpoint in endpoints:
                        f.write(f"- **{endpoint['method']}** {endpoint['path']}\n")
                    f.write("\n")
                
                # Database Analysis
                f.write("## 🗄️  DATABASE ANALYSIS\n\n")
                for db_file, db_info in self.analysis_results['database_analysis'].items():
                    f.write(f"### {db_info['file']}\n")
                    f.write(f"- **Size:** {db_info['size']} bytes\n")
                    f.write(f"- **Tables:** {len(db_info['tables'])}\n")
                    for table_name, table_info in db_info['tables'].items():
                        f.write(f"  - **{table_name}:** {table_info['row_count']} rows, {table_info['columns']} columns\n")
                    f.write("\n")
                
                # Functionality Map
                f.write("## 🗺️  FUNCTIONALITY MAP\n\n")
                for file_path, func_map in self.analysis_results['functionality_map'].items():
                    f.write(f"### {file_path}\n")
                    f.write(f"- **Functions:** {len(func_map['functions'])}\n")
                    f.write(f"- **Classes:** {len(func_map['classes'])}\n")
                    f.write(f"- **Imports:** {len(func_map['imports'])}\n")
                    f.write(f"- **API Endpoints:** {len(func_map.get('api_endpoints', []))}\n")
                    f.write(f"- **Syntax Valid:** {'✅' if func_map['syntax_valid'] else '❌'}\n")
                    
                    if func_map['import_errors']:
                        f.write(f"- **Import Errors:** {len(func_map['import_errors'])}\n")
                        for error in func_map['import_errors'][:3]:  # Show first 3
                            f.write(f"  - {error}\n")
                    f.write("\n")
        
            # Save JSON report
            json_report_path = self.root_path / 'fixed_analysis_results.json'
            with open(json_report_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, default=str)
            
            print(f"📊 Fixed reports saved:")
            print(f"  - Markdown: {report_path}")
            print(f"  - JSON: {json_report_path}")
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")

    def trace_application_usage(self):
        """Trace which files are actually used by the application starting from entry points"""
        print("🔗 Tracing actual application usage...")
        
        # Define entry points
        entry_points = [
            "main.py",
            "dashboardtest/app.py",
            "backendtest/main.py",
            "backendtest/app.py"
        ]
        
        self.used_files = set()
        
        # Trace usage from each entry point
        for entry_point in entry_points:
            entry_path = self.root_path / entry_point
            if entry_path.exists():
                print(f"  📍 Tracing from: {entry_point}")
                self.trace_imports_recursively(entry_path, set())
        
        # Filter analysis results to only include used files
        self.filter_to_used_files()
        
        print(f"✅ Found {len(self.used_files)} files actually used by the application")
    
    def trace_imports_recursively(self, file_path: Path, visited=None):
        """Recursively trace imports from a file"""
        if visited is None:
            visited = set()
        
        # Convert to string for comparison
        file_str = str(file_path)
        if file_str in visited:
            return
        visited.add(file_str)
        
        # Add this file to used files
        try:
            relative_path = file_path.relative_to(self.root_path)
            self.used_files.add(str(relative_path))
        except ValueError:
            # File is outside root path
            return
        
        # Read and analyze imports
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.resolve_and_trace_import(alias.name, file_path, visited)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self.resolve_and_trace_import(node.module, file_path, visited)
            except SyntaxError:
                pass  # Skip files with syntax errors
                        
        except Exception as e:
            print(f"⚠️  Error tracing imports from {file_path}: {e}")
    
    def resolve_and_trace_import(self, import_name: str, current_file: Path, visited: Set[str]):
        """Resolve an import to a file path and trace it"""
        # Skip standard library and third-party imports
        if not import_name or '.' not in import_name:
            # Check if it's a local file
            potential_paths = [
                self.root_path / f"{import_name}.py",
                self.root_path / import_name / "__init__.py"
            ]
        else:
            # Handle relative imports
            parts = import_name.split('.')
            
            # Try different potential paths
            potential_paths = []
            
            # Try as direct file
            potential_paths.append(self.root_path / f"{'/'.join(parts)}.py")
            
            # Try as package
            potential_paths.append(self.root_path / '/'.join(parts) / "__init__.py")
            
            # Try relative to current file's directory
            current_dir = current_file.parent
            potential_paths.append(current_dir / f"{parts[-1]}.py")
            
            # Try application directories
            for app_dir in ["dashboardtest", "backendtest"]:
                app_path = self.root_path / app_dir
                if len(parts) == 1:
                    potential_paths.append(app_path / f"{parts[0]}.py")
                else:
                    potential_paths.append(app_path / f"{'/'.join(parts[1:])}.py")
        
        # Check each potential path
        for path in potential_paths:
            if path.exists() and path.is_file():
                self.trace_imports_recursively(path, visited)
                break
    
    def filter_to_used_files(self):
        """Filter analysis results to only include files actually used by the application"""
        print("🔍 Filtering analysis to only used files...")
        
        # Filter files_analyzed to only include used files
        original_count = len(self.analysis_results['files_analyzed'])
        self.analysis_results['files_analyzed'] = [
            file_info for file_info in self.analysis_results['files_analyzed']
            if file_info['path'] in self.used_files or file_info['type'] == '.db'  # Keep database files
        ]
        filtered_count = len(self.analysis_results['files_analyzed'])
        
        print(f"📊 Filtered from {original_count} to {filtered_count} files")
        
        # Also filter functionality_map
        used_functionality = {}
        for file_path, func_data in self.analysis_results['functionality_map'].items():
            if file_path in self.used_files:
                used_functionality[file_path] = func_data
        
        self.analysis_results['functionality_map'] = used_functionality
        
        # Update existing_files to only include used files
        self.analysis_results['existing_files'] = [
            file_info for file_info in self.analysis_results['existing_files']
            if any(file_info['path'] == used_file for used_file in self.used_files)
        ]

def main():
    """Main analysis function"""
    root_path = r"c:\Users\Hari\Desktop\Testin dub"
    
    print("🔧 Starting FIXED Comprehensive Codebase Analysis")
    print("=" * 60)
    
    analyzer = FixedComprehensiveAnalyzer(root_path)
    results = analyzer.run_complete_analysis()
    
    print("\n🎉 FIXED analysis complete!")
    print(f"📊 Total files analyzed: {len(results['files_analyzed'])}")
    print(f"✅ Existing critical files: {len(results['existing_files'])}")
    print(f"❌ Missing critical files: {len(results['missing_files'])}")
    print(f"🚨 Syntax errors: {len(results['syntax_errors'])}")
    print(f"🌐 API endpoints: {sum(len(endpoints) for endpoints in results['api_endpoints'].values())}")
    print(f"🗄️  Database files: {len(results['database_analysis'])}")
    
    if results['missing_files']:
        print(f"\n⚠️  Missing files:")
        for missing in results['missing_files']:
            print(f"  - {missing}")
    else:
        print(f"\n✅ All critical files found!")

if __name__ == "__main__":
    main()
