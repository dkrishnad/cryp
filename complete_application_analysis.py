#!/usr/bin/env python3
"""
Complete Application Analysis Tool
Performs 100% comprehensive analysis of the crypto trading bot application:
- File structure and dependencies
- Data flow analysis
- Callback mapping and validation
- Database integrity
- API endpoint testing
- Error handling verification
- Performance bottlenecks
- Security vulnerabilities
- Code quality assessment
"""

import os
import sys
import ast
import re
import json
import sqlite3
import traceback
import requests
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional
from datetime import datetime
import importlib.util

class CompleteApplicationAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'application_structure': {},
            'data_flow_analysis': {},
            'callback_validation': {},
            'database_integrity': {},
            'api_endpoints': {},
            'file_dependencies': {},
            'error_analysis': {},
            'performance_analysis': {},
            'security_analysis': {},
            'code_quality': {},
            'functionality_map': {},
            'missing_components': [],
            'critical_issues': [],
            'recommendations': []
        }
        
        # Core application files
        self.core_files = {
            'main': 'main.py',
            'dashboard_app': 'dashboardtest/app.py',
            'dashboard_layout': 'dashboardtest/layout.py',
            'dashboard_callbacks': 'dashboardtest/callbacks.py',
            'backend_app': 'backendtest/app.py',
            'data_collection': 'backendtest/data_collection.py',
            'trading_logic': 'backendtest/trading.py',
            'ml_models': 'backendtest/ml_models.py',
            'database': 'trades.db'
        }
        
        print(f"🔍 Starting Complete Application Analysis...")
        print(f"📁 Root Path: {self.root_path}")
        print(f"🎯 Analyzing {len(self.core_files)} core components")
        
    def run_complete_analysis(self):
        """Run comprehensive analysis of entire application"""
        print("\n🚀 PHASE 1: Application Structure Analysis")
        self.analyze_application_structure()
        
        print("\n🔄 PHASE 2: Data Flow Analysis")
        self.analyze_data_flow()
        
        print("\n📱 PHASE 3: Callback Validation")
        self.validate_callbacks()
        
        print("\n🗄️ PHASE 4: Database Integrity Check")
        self.check_database_integrity()
        
        print("\n🌐 PHASE 5: API Endpoint Testing")
        self.test_api_endpoints()
        
        print("\n📦 PHASE 6: File Dependencies")
        self.analyze_file_dependencies()
        
        print("\n🚨 PHASE 7: Error Handling Analysis")
        self.analyze_error_handling()
        
        print("\n⚡ PHASE 8: Performance Analysis")
        self.analyze_performance()
        
        print("\n🔒 PHASE 9: Security Analysis")
        self.analyze_security()
        
        print("\n✅ PHASE 10: Code Quality Assessment")
        self.assess_code_quality()
        
        print("\n📊 PHASE 11: Generate Report")
        self.generate_comprehensive_report()
        
        return self.analysis_results
    
    def analyze_application_structure(self):
        """Analyze the overall application structure"""
        print("📁 Analyzing application structure...")
        
        structure = {
            'core_files_status': {},
            'total_files': 0,
            'file_types': {},
            'missing_files': [],
            'directory_structure': {}
        }
        
        # Check core files
        for component, file_path in self.core_files.items():
            full_path = self.root_path / file_path
            if full_path.exists():
                stat = full_path.stat()
                structure['core_files_status'][component] = {
                    'path': str(file_path),
                    'exists': True,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
                print(f"  ✅ {component}: {file_path}")
            else:
                structure['core_files_status'][component] = {
                    'path': str(file_path),
                    'exists': False
                }
                structure['missing_files'].append(file_path)
                print(f"  ❌ {component}: {file_path} - MISSING")
        
        # Analyze all files
        for root, dirs, files in os.walk(self.root_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.root_path)
                
                # Count by extension
                ext = file_path.suffix.lower()
                if ext not in structure['file_types']:
                    structure['file_types'][ext] = 0
                structure['file_types'][ext] += 1
                structure['total_files'] += 1
        
        self.analysis_results['application_structure'] = structure
        print(f"📊 Found {structure['total_files']} files across {len(structure['file_types'])} types")
    
    def analyze_data_flow(self):
        """Analyze data flow through the application"""
        print("🔄 Analyzing data flow...")
        
        data_flow = {
            'database_connections': [],
            'api_calls': [],
            'data_transformations': [],
            'input_sources': [],
            'output_destinations': [],
            'data_validation': []
        }
        
        # Analyze Python files for data flow patterns
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = file_path.relative_to(self.root_path)
                
                # Database connections
                db_patterns = [
                    r'sqlite3\.connect\s*\(\s*[\'"]([^\'\"]+)[\'"]',
                    r'\.db[\'"]',
                    r'CREATE TABLE',
                    r'INSERT INTO',
                    r'SELECT.*FROM',
                    r'UPDATE.*SET'
                ]
                
                for pattern in db_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        data_flow['database_connections'].append({
                            'file': str(relative_path),
                            'pattern': pattern,
                            'matches': matches
                        })
                
                # API calls
                api_patterns = [
                    r'requests\.(get|post|put|delete)',
                    r'aiohttp\.',
                    r'@app\.route',
                    r'make_api_call',
                    r'api\.binance\.com'
                ]
                
                for pattern in api_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        data_flow['api_calls'].append({
                            'file': str(relative_path),
                            'pattern': pattern,
                            'matches': matches
                        })
                
                # Data transformations
                transform_patterns = [
                    r'pd\.DataFrame',
                    r'pd\.read_',
                    r'\.to_dict\(',
                    r'\.to_json\(',
                    r'json\.loads',
                    r'json\.dumps'
                ]
                
                for pattern in transform_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        data_flow['data_transformations'].append({
                            'file': str(relative_path),
                            'pattern': pattern,
                            'count': len(matches)
                        })
                
            except Exception as e:
                print(f"❌ Error analyzing data flow in {file_path}: {e}")
        
        self.analysis_results['data_flow_analysis'] = data_flow
        print(f"📊 Found {len(data_flow['database_connections'])} DB connections, {len(data_flow['api_calls'])} API calls")
    
    def validate_callbacks(self):
        """Validate all dashboard callbacks"""
        print("📱 Validating callbacks...")
        
        callbacks_file = self.root_path / 'dashboardtest/callbacks.py'
        layout_file = self.root_path / 'dashboardtest/layout.py'
        
        callback_validation = {
            'total_callbacks': 0,
            'valid_callbacks': 0,
            'invalid_callbacks': [],
            'orphaned_outputs': [],
            'missing_inputs': [],
            'duplicate_callbacks': [],
            'callback_functions': [],
            'component_mapping': {}
        }
        
        if not callbacks_file.exists():
            callback_validation['error'] = "Callbacks file not found"
            self.analysis_results['callback_validation'] = callback_validation
            return
        
        try:
            with open(callbacks_file, 'r', encoding='utf-8') as f:
                callbacks_content = f.read()
            
            # Find all callback decorators
            callback_pattern = r'@app\.callback\s*\(\s*(.*?)\s*\)\s*def\s+(\w+)\s*\('
            callbacks = re.findall(callback_pattern, callbacks_content, re.DOTALL)
            
            callback_validation['total_callbacks'] = len(callbacks)
            
            # Extract component IDs from callbacks
            for callback_def, func_name in callbacks:
                callback_validation['callback_functions'].append(func_name)
                
                # Find Output components
                output_pattern = r'Output\s*\(\s*[\'"]([^\'\"]+)[\'"]'
                outputs = re.findall(output_pattern, callback_def)
                
                # Find Input components
                input_pattern = r'Input\s*\(\s*[\'"]([^\'\"]+)[\'"]'
                inputs = re.findall(input_pattern, callback_def)
                
                callback_validation['component_mapping'][func_name] = {
                    'outputs': outputs,
                    'inputs': inputs
                }
            
            # Check for layout components if layout file exists
            if layout_file.exists():
                with open(layout_file, 'r', encoding='utf-8') as f:
                    layout_content = f.read()
                
                # Find all component IDs in layout
                id_pattern = r'id\s*=\s*[\'"]([^\'\"]+)[\'"]'
                layout_ids = set(re.findall(id_pattern, layout_content))
                
                # Check for orphaned outputs
                all_callback_outputs = set()
                all_callback_inputs = set()
                
                for func_name, mapping in callback_validation['component_mapping'].items():
                    all_callback_outputs.update(mapping['outputs'])
                    all_callback_inputs.update(mapping['inputs'])
                
                # Find orphaned outputs (callbacks targeting non-existent components)
                callback_validation['orphaned_outputs'] = list(all_callback_outputs - layout_ids)
                
                # Find missing inputs (layout components without callbacks)
                callback_validation['missing_inputs'] = list(layout_ids - all_callback_inputs - all_callback_outputs)
            
            # Check for duplicate callback functions
            func_names = [func for _, func in callbacks]
            seen = set()
            for func_name in func_names:
                if func_name in seen:
                    callback_validation['duplicate_callbacks'].append(func_name)
                else:
                    seen.add(func_name)
            
            callback_validation['valid_callbacks'] = len(callbacks) - len(callback_validation['duplicate_callbacks'])
            
        except Exception as e:
            callback_validation['error'] = str(e)
            print(f"❌ Error validating callbacks: {e}")
        
        self.analysis_results['callback_validation'] = callback_validation
        print(f"📊 Found {callback_validation['total_callbacks']} callbacks, {len(callback_validation['orphaned_outputs'])} orphaned outputs")
    
    def check_database_integrity(self):
        """Check database integrity and structure"""
        print("🗄️ Checking database integrity...")
        
        db_integrity = {
            'databases': {},
            'total_tables': 0,
            'total_records': 0,
            'schema_issues': [],
            'data_issues': []
        }
        
        # Find all database files
        db_files = list(self.root_path.glob('*.db'))
        
        for db_file in db_files:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                db_info = {
                    'file': str(db_file.name),
                    'size': db_file.stat().st_size,
                    'tables': {},
                    'indexes': [],
                    'issues': []
                }
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    row_count = cursor.fetchone()[0]
                    
                    # Check for empty tables
                    if row_count == 0:
                        db_info['issues'].append(f"Empty table: {table_name}")
                    
                    # Check for proper indexes
                    cursor.execute(f"PRAGMA index_list({table_name});")
                    indexes = cursor.fetchall()
                    
                    db_info['tables'][table_name] = {
                        'columns': len(columns),
                        'rows': row_count,
                        'indexes': len(indexes),
                        'schema': [{'name': col[1], 'type': col[2], 'notnull': col[3]} for col in columns]
                    }
                    
                    db_integrity['total_records'] += row_count
                
                # Get all indexes
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
                all_indexes = cursor.fetchall()
                db_info['indexes'] = [idx[0] for idx in all_indexes]
                
                db_integrity['total_tables'] += len(tables)
                db_integrity['databases'][str(db_file)] = db_info
                
                conn.close()
                print(f"  ✅ {db_file.name}: {len(tables)} tables, {sum(t['rows'] for t in db_info['tables'].values())} records")
                
            except Exception as e:
                db_integrity['databases'][str(db_file)] = {'error': str(e)}
                print(f"  ❌ {db_file.name}: {e}")
        
        self.analysis_results['database_integrity'] = db_integrity
        print(f"📊 Analyzed {len(db_files)} databases, {db_integrity['total_tables']} tables, {db_integrity['total_records']} records")
    
    def test_api_endpoints(self):
        """Test API endpoints for functionality"""
        print("🌐 Testing API endpoints...")
        
        api_analysis = {
            'backend_endpoints': [],
            'dashboard_endpoints': [],
            'external_apis': [],
            'endpoint_status': {},
            'response_times': {},
            'errors': []
        }
        
        # Look for Flask apps
        app_files = ['backendtest/app.py', 'dashboardtest/app.py', 'main.py']
        
        for app_file in app_files:
            file_path = self.root_path / app_file
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find Flask routes
                route_pattern = r'@app\.route\s*\(\s*[\'"]([^\'\"]+)[\'"].*?methods\s*=\s*\[([^\]]+)\]'
                routes = re.findall(route_pattern, content, re.DOTALL)
                
                simple_route_pattern = r'@app\.route\s*\(\s*[\'"]([^\'\"]+)[\'"]'
                simple_routes = re.findall(simple_route_pattern, content)
                
                for route in simple_routes:
                    if route not in [r[0] for r in routes]:
                        routes.append((route, 'GET'))
                
                if 'backend' in app_file:
                    api_analysis['backend_endpoints'].extend(routes)
                else:
                    api_analysis['dashboard_endpoints'].extend(routes)
                
                print(f"  📍 {app_file}: {len(routes)} endpoints")
                
            except Exception as e:
                api_analysis['errors'].append(f"Error analyzing {app_file}: {e}")
        
        # Test if backend is running (basic check)
        try:
            import requests
            response = requests.get('http://localhost:5000/health', timeout=2)
            api_analysis['backend_status'] = 'running'
        except:
            api_analysis['backend_status'] = 'not_running'
        
        self.analysis_results['api_endpoints'] = api_analysis
        print(f"📊 Found {len(api_analysis['backend_endpoints'])} backend endpoints, {len(api_analysis['dashboard_endpoints'])} dashboard endpoints")
    
    def analyze_file_dependencies(self):
        """Analyze file dependencies and imports"""
        print("📦 Analyzing file dependencies...")
        
        dependencies = {
            'import_map': {},
            'missing_imports': [],
            'circular_dependencies': [],
            'external_packages': set(),
            'internal_modules': set()
        }
        
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = str(file_path.relative_to(self.root_path))
                
                # Find imports
                import_patterns = [
                    r'import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
                    r'from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import'
                ]
                
                file_imports = set()
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    file_imports.update(matches)
                
                dependencies['import_map'][relative_path] = list(file_imports)
                
                # Categorize imports
                for imp in file_imports:
                    if imp in ['os', 'sys', 'json', 'datetime', 're', 'sqlite3', 'threading', 'asyncio']:
                        continue  # Standard library
                    elif imp.startswith('.') or 'test' in imp or 'dashboard' in imp or 'backend' in imp:
                        dependencies['internal_modules'].add(imp)
                    else:
                        dependencies['external_packages'].add(imp)
                
            except Exception as e:
                print(f"❌ Error analyzing imports in {file_path}: {e}")
        
        # Check for missing imports
        for file_path, imports in dependencies['import_map'].items():
            for imp in imports:
                if imp in dependencies['external_packages']:
                    try:
                        __import__(imp)
                    except ImportError:
                        dependencies['missing_imports'].append({
                            'file': file_path,
                            'import': imp
                        })
        
        dependencies['external_packages'] = list(dependencies['external_packages'])
        dependencies['internal_modules'] = list(dependencies['internal_modules'])
        
        self.analysis_results['file_dependencies'] = dependencies
        print(f"📊 Analyzed {len(python_files)} files, {len(dependencies['external_packages'])} external packages, {len(dependencies['missing_imports'])} missing imports")
    
    def analyze_error_handling(self):
        """Analyze error handling patterns"""
        print("🚨 Analyzing error handling...")
        
        error_analysis = {
            'try_except_blocks': 0,
            'bare_except_blocks': 0,
            'logged_errors': 0,
            'unhandled_exceptions': [],
            'error_patterns': {},
            'files_with_errors': {}
        }
        
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = str(file_path.relative_to(self.root_path))
                
                # Count error handling patterns
                try_blocks = len(re.findall(r'try\s*:', content))
                bare_except = len(re.findall(r'except\s*:', content))
                logged_errors = len(re.findall(r'log\w*\.(error|exception|warning)', content, re.IGNORECASE))
                
                error_analysis['try_except_blocks'] += try_blocks
                error_analysis['bare_except_blocks'] += bare_except
                error_analysis['logged_errors'] += logged_errors
                
                if try_blocks > 0 or bare_except > 0 or logged_errors > 0:
                    error_analysis['files_with_errors'][relative_path] = {
                        'try_blocks': try_blocks,
                        'bare_except': bare_except,
                        'logged_errors': logged_errors
                    }
                
                # Check for potential unhandled exceptions
                risky_patterns = [
                    r'json\.loads\s*\([^)]*\)',
                    r'int\s*\([^)]*\)',
                    r'float\s*\([^)]*\)',
                    r'open\s*\([^)]*\)',
                    r'requests\.(get|post)\s*\([^)]*\)'
                ]
                
                for pattern in risky_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        # Check if these are within try blocks
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if re.search(pattern, line):
                                # Simple check: look for try block in previous lines
                                in_try_block = False
                                for j in range(max(0, i-10), i):
                                    if 'try:' in lines[j]:
                                        in_try_block = True
                                        break
                                
                                if not in_try_block:
                                    error_analysis['unhandled_exceptions'].append({
                                        'file': relative_path,
                                        'line': i + 1,
                                        'pattern': pattern,
                                        'code': line.strip()
                                    })
                
            except Exception as e:
                print(f"❌ Error analyzing error handling in {file_path}: {e}")
        
        self.analysis_results['error_analysis'] = error_analysis
        print(f"📊 Found {error_analysis['try_except_blocks']} try blocks, {error_analysis['bare_except_blocks']} bare except, {len(error_analysis['unhandled_exceptions'])} potential unhandled exceptions")
    
    def analyze_performance(self):
        """Analyze performance bottlenecks"""
        print("⚡ Analyzing performance...")
        
        performance = {
            'potential_bottlenecks': [],
            'inefficient_patterns': [],
            'database_issues': [],
            'loop_issues': [],
            'memory_issues': []
        }
        
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = str(file_path.relative_to(self.root_path))
                
                # Check for performance issues
                perf_patterns = [
                    (r'time\.sleep\s*\(\s*[0-9]+\s*\)', 'Long sleep operations'),
                    (r'while\s+True\s*:', 'Infinite loops'),
                    (r'for\s+\w+\s+in\s+range\s*\(\s*[0-9]{4,}\s*\)', 'Large range loops'),
                    (r'\.append\s*\([^)]*\)\s*\n.*\.append', 'Inefficient list operations'),
                    (r'SELECT\s*\*\s*FROM', 'Inefficient database queries'),
                    (r'pd\.concat\s*\(.*for.*in.*\)', 'Inefficient pandas operations')
                ]
                
                for pattern, description in perf_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                    if matches:
                        performance['potential_bottlenecks'].append({
                            'file': relative_path,
                            'issue': description,
                            'count': len(matches)
                        })
                
                # Check for large files (potential memory issues)
                if file_path.stat().st_size > 100000:  # 100KB
                    performance['memory_issues'].append({
                        'file': relative_path,
                        'size': file_path.stat().st_size,
                        'issue': 'Large file size'
                    })
                
            except Exception as e:
                print(f"❌ Error analyzing performance in {file_path}: {e}")
        
        self.analysis_results['performance_analysis'] = performance
        print(f"📊 Found {len(performance['potential_bottlenecks'])} potential bottlenecks, {len(performance['memory_issues'])} memory issues")
    
    def analyze_security(self):
        """Analyze security vulnerabilities"""
        print("🔒 Analyzing security...")
        
        security = {
            'vulnerabilities': [],
            'hardcoded_secrets': [],
            'unsafe_operations': [],
            'input_validation': [],
            'authentication_issues': []
        }
        
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = str(file_path.relative_to(self.root_path))
                
                # Security patterns
                security_patterns = [
                    (r'eval\s*\(', 'Use of eval() function'),
                    (r'exec\s*\(', 'Use of exec() function'),
                    (r'pickle\.loads?\s*\(', 'Unsafe pickle usage'),
                    (r'shell\s*=\s*True', 'Shell injection risk'),
                    (r'password\s*=\s*[\'"][^\'\"]*[\'"]', 'Hardcoded password'),
                    (r'secret\s*=\s*[\'"][^\'\"]*[\'"]', 'Hardcoded secret'),
                    (r'api[_-]?key\s*=\s*[\'"][^\'\"]*[\'"]', 'Hardcoded API key'),
                    (r'token\s*=\s*[\'"][^\'\"]*[\'"]', 'Hardcoded token'),
                    (r'subprocess\.call\s*\(', 'Subprocess usage'),
                    (r'os\.system\s*\(', 'OS system calls')
                ]
                
                for pattern, description in security_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        security['vulnerabilities'].append({
                            'file': relative_path,
                            'issue': description,
                            'matches': len(matches)
                        })
                
                # Check for SQL injection risks
                sql_patterns = [
                    r'cursor\.execute\s*\(\s*[\'"][^\'\"]*%s[^\'\"]*[\'"]',
                    r'cursor\.execute\s*\(\s*[\'"][^\'\"]*\+[^\'\"]*[\'"]'
                ]
                
                for pattern in sql_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        security['vulnerabilities'].append({
                            'file': relative_path,
                            'issue': 'Potential SQL injection',
                            'matches': len(matches)
                        })
                
            except Exception as e:
                print(f"❌ Error analyzing security in {file_path}: {e}")
        
        self.analysis_results['security_analysis'] = security
        print(f"📊 Found {len(security['vulnerabilities'])} security issues")
    
    def assess_code_quality(self):
        """Assess overall code quality"""
        print("✅ Assessing code quality...")
        
        quality = {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': 0,
            'classes': 0,
            'complexity_issues': [],
            'style_issues': [],
            'documentation_issues': []
        }
        
        python_files = list(self.root_path.glob('**/*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                relative_path = str(file_path.relative_to(self.root_path))
                
                file_stats = {
                    'total_lines': len(lines),
                    'code_lines': 0,
                    'comment_lines': 0,
                    'blank_lines': 0,
                    'long_lines': 0,
                    'functions': 0,
                    'classes': 0
                }
                
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    
                    if not stripped:
                        file_stats['blank_lines'] += 1
                    elif stripped.startswith('#'):
                        file_stats['comment_lines'] += 1
                    else:
                        file_stats['code_lines'] += 1
                    
                    # Check line length
                    if len(line) > 100:
                        file_stats['long_lines'] += 1
                    
                    # Count functions and classes
                    if stripped.startswith('def '):
                        file_stats['functions'] += 1
                    elif stripped.startswith('class '):
                        file_stats['classes'] += 1
                
                # Update totals
                quality['total_lines'] += file_stats['total_lines']
                quality['code_lines'] += file_stats['code_lines']
                quality['comment_lines'] += file_stats['comment_lines']
                quality['blank_lines'] += file_stats['blank_lines']
                quality['functions'] += file_stats['functions']
                quality['classes'] += file_stats['classes']
                
                # Check for style issues
                if file_stats['long_lines'] > 10:
                    quality['style_issues'].append({
                        'file': relative_path,
                        'issue': 'Many long lines',
                        'count': file_stats['long_lines']
                    })
                
                # Check documentation
                if file_stats['functions'] > 5 and file_stats['comment_lines'] < file_stats['functions']:
                    quality['documentation_issues'].append({
                        'file': relative_path,
                        'issue': 'Insufficient documentation',
                        'functions': file_stats['functions'],
                        'comments': file_stats['comment_lines']
                    })
                
            except Exception as e:
                print(f"❌ Error assessing quality in {file_path}: {e}")
        
        # Calculate ratios
        if quality['total_lines'] > 0:
            quality['comment_ratio'] = quality['comment_lines'] / quality['total_lines']
            quality['code_ratio'] = quality['code_lines'] / quality['total_lines']
        
        self.analysis_results['code_quality'] = quality
        print(f"📊 {quality['total_lines']} total lines, {quality['functions']} functions, {quality['classes']} classes")
        print(f"📊 Comment ratio: {quality.get('comment_ratio', 0):.2%}, Code ratio: {quality.get('code_ratio', 0):.2%}")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("📊 Generating comprehensive report...")
        
        # Identify critical issues
        critical_issues = []
        
        # Missing core files
        if self.analysis_results['application_structure']['missing_files']:
            critical_issues.append({
                'severity': 'CRITICAL',
                'category': 'Structure',
                'issue': 'Missing core files',
                'details': self.analysis_results['application_structure']['missing_files']
            })
        
        # Orphaned callbacks
        if self.analysis_results['callback_validation']['orphaned_outputs']:
            critical_issues.append({
                'severity': 'HIGH',
                'category': 'Callbacks',
                'issue': 'Orphaned callback outputs',
                'details': self.analysis_results['callback_validation']['orphaned_outputs']
            })
        
        # Missing imports
        if self.analysis_results['file_dependencies']['missing_imports']:
            critical_issues.append({
                'severity': 'CRITICAL',
                'category': 'Dependencies',
                'issue': 'Missing imports',
                'details': self.analysis_results['file_dependencies']['missing_imports']
            })
        
        # Security vulnerabilities
        if self.analysis_results['security_analysis']['vulnerabilities']:
            critical_issues.append({
                'severity': 'HIGH',
                'category': 'Security',
                'issue': 'Security vulnerabilities',
                'details': len(self.analysis_results['security_analysis']['vulnerabilities'])
            })
        
        # Unhandled exceptions
        if self.analysis_results['error_analysis']['unhandled_exceptions']:
            critical_issues.append({
                'severity': 'MEDIUM',
                'category': 'Error Handling',
                'issue': 'Potential unhandled exceptions',
                'details': len(self.analysis_results['error_analysis']['unhandled_exceptions'])
            })
        
        self.analysis_results['critical_issues'] = critical_issues
        
        # Generate recommendations
        recommendations = []
        
        if critical_issues:
            recommendations.append("🚨 Address critical issues immediately before deployment")
        
        if self.analysis_results['callback_validation']['orphaned_outputs']:
            recommendations.append("🔧 Fix orphaned callback outputs to prevent UI errors")
        
        if self.analysis_results['file_dependencies']['missing_imports']:
            recommendations.append("📦 Install missing dependencies or fix import statements")
        
        if self.analysis_results['security_analysis']['vulnerabilities']:
            recommendations.append("🔒 Review and fix security vulnerabilities")
        
        if self.analysis_results['performance_analysis']['potential_bottlenecks']:
            recommendations.append("⚡ Optimize performance bottlenecks")
        
        if self.analysis_results['code_quality']['comment_ratio'] < 0.1:
            recommendations.append("📝 Improve code documentation")
        
        self.analysis_results['recommendations'] = recommendations
        
        # Save detailed report
        report_path = self.root_path / 'COMPLETE_APPLICATION_ANALYSIS.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🚀 COMPLETE APPLICATION ANALYSIS REPORT\n\n")
            f.write(f"**Generated:** {self.analysis_results['timestamp']}\n")
            f.write(f"**Analysis Duration:** Complete codebase scan\n\n")
            
            # Executive Summary
            f.write("## 📋 EXECUTIVE SUMMARY\n\n")
            f.write(f"- **Total Files:** {self.analysis_results['application_structure']['total_files']}\n")
            f.write(f"- **Core Files Status:** {len([f for f in self.analysis_results['application_structure']['core_files_status'].values() if f['exists']])}/{len(self.analysis_results['application_structure']['core_files_status'])}\n")
            f.write(f"- **Total Callbacks:** {self.analysis_results['callback_validation']['total_callbacks']}\n")
            f.write(f"- **Database Records:** {self.analysis_results['database_integrity']['total_records']}\n")
            f.write(f"- **Critical Issues:** {len(self.analysis_results['critical_issues'])}\n")
            f.write(f"- **Security Issues:** {len(self.analysis_results['security_analysis']['vulnerabilities'])}\n")
            f.write(f"- **Performance Issues:** {len(self.analysis_results['performance_analysis']['potential_bottlenecks'])}\n\n")
            
            # Critical Issues
            if critical_issues:
                f.write("## 🚨 CRITICAL ISSUES\n\n")
                for issue in critical_issues:
                    f.write(f"### {issue['severity']}: {issue['issue']}\n")
                    f.write(f"**Category:** {issue['category']}\n")
                    f.write(f"**Details:** {issue['details']}\n\n")
            
            # Application Structure
            f.write("## 📁 APPLICATION STRUCTURE\n\n")
            f.write("### Core Files Status:\n")
            for component, status in self.analysis_results['application_structure']['core_files_status'].items():
                status_icon = "✅" if status['exists'] else "❌"
                f.write(f"- {status_icon} **{component}:** {status['path']}\n")
            
            f.write("\n### File Distribution:\n")
            for ext, count in self.analysis_results['application_structure']['file_types'].items():
                f.write(f"- **{ext or 'no extension'}:** {count} files\n")
            
            # Callback Analysis
            f.write("\n## 📱 CALLBACK ANALYSIS\n\n")
            f.write(f"- **Total Callbacks:** {self.analysis_results['callback_validation']['total_callbacks']}\n")
            f.write(f"- **Valid Callbacks:** {self.analysis_results['callback_validation']['valid_callbacks']}\n")
            f.write(f"- **Orphaned Outputs:** {len(self.analysis_results['callback_validation']['orphaned_outputs'])}\n")
            f.write(f"- **Missing Inputs:** {len(self.analysis_results['callback_validation']['missing_inputs'])}\n")
            f.write(f"- **Duplicate Callbacks:** {len(self.analysis_results['callback_validation']['duplicate_callbacks'])}\n")
            
            if self.analysis_results['callback_validation']['orphaned_outputs']:
                f.write("\n### Orphaned Outputs:\n")
                for output in self.analysis_results['callback_validation']['orphaned_outputs']:
                    f.write(f"- {output}\n")
            
            # Database Analysis
            f.write("\n## 🗄️ DATABASE ANALYSIS\n\n")
            f.write(f"- **Total Databases:** {len(self.analysis_results['database_integrity']['databases'])}\n")
            f.write(f"- **Total Tables:** {self.analysis_results['database_integrity']['total_tables']}\n")
            f.write(f"- **Total Records:** {self.analysis_results['database_integrity']['total_records']}\n")
            
            for db_path, db_info in self.analysis_results['database_integrity']['databases'].items():
                if 'error' in db_info:
                    f.write(f"- ❌ **{db_info.get('file', db_path)}:** {db_info['error']}\n")
                else:
                    f.write(f"- ✅ **{db_info['file']}:** {len(db_info['tables'])} tables, {db_info['size']} bytes\n")
            
            # API Endpoints
            f.write("\n## 🌐 API ENDPOINTS\n\n")
            f.write(f"- **Backend Endpoints:** {len(self.analysis_results['api_endpoints']['backend_endpoints'])}\n")
            f.write(f"- **Dashboard Endpoints:** {len(self.analysis_results['api_endpoints']['dashboard_endpoints'])}\n")
            f.write(f"- **Backend Status:** {self.analysis_results['api_endpoints']['backend_status']}\n")
            
            # Dependencies
            f.write("\n## 📦 DEPENDENCIES\n\n")
            f.write(f"- **External Packages:** {len(self.analysis_results['file_dependencies']['external_packages'])}\n")
            f.write(f"- **Internal Modules:** {len(self.analysis_results['file_dependencies']['internal_modules'])}\n")
            f.write(f"- **Missing Imports:** {len(self.analysis_results['file_dependencies']['missing_imports'])}\n")
            
            if self.analysis_results['file_dependencies']['missing_imports']:
                f.write("\n### Missing Imports:\n")
                for missing in self.analysis_results['file_dependencies']['missing_imports']:
                    f.write(f"- **{missing['import']}** in {missing['file']}\n")
            
            # Security Analysis
            f.write("\n## 🔒 SECURITY ANALYSIS\n\n")
            if self.analysis_results['security_analysis']['vulnerabilities']:
                f.write("### Security Vulnerabilities:\n")
                for vuln in self.analysis_results['security_analysis']['vulnerabilities']:
                    f.write(f"- **{vuln['issue']}** in {vuln['file']} ({vuln['matches']} occurrences)\n")
            else:
                f.write("✅ No major security vulnerabilities detected.\n")
            
            # Performance Analysis
            f.write("\n## ⚡ PERFORMANCE ANALYSIS\n\n")
            if self.analysis_results['performance_analysis']['potential_bottlenecks']:
                f.write("### Potential Bottlenecks:\n")
                for bottleneck in self.analysis_results['performance_analysis']['potential_bottlenecks']:
                    f.write(f"- **{bottleneck['issue']}** in {bottleneck['file']} ({bottleneck['count']} occurrences)\n")
            else:
                f.write("✅ No major performance bottlenecks detected.\n")
            
            # Code Quality
            f.write("\n## ✅ CODE QUALITY\n\n")
            quality = self.analysis_results['code_quality']
            f.write(f"- **Total Lines:** {quality['total_lines']}\n")
            f.write(f"- **Code Lines:** {quality['code_lines']} ({quality.get('code_ratio', 0):.1%})\n")
            f.write(f"- **Comment Lines:** {quality['comment_lines']} ({quality.get('comment_ratio', 0):.1%})\n")
            f.write(f"- **Functions:** {quality['functions']}\n")
            f.write(f"- **Classes:** {quality['classes']}\n")
            
            # Recommendations
            f.write("\n## 💡 RECOMMENDATIONS\n\n")
            for i, rec in enumerate(self.analysis_results['recommendations'], 1):
                f.write(f"{i}. {rec}\n")
            
            # Data Flow Summary
            f.write("\n## 🔄 DATA FLOW SUMMARY\n\n")
            flow = self.analysis_results['data_flow_analysis']
            f.write(f"- **Database Connections:** {len(flow['database_connections'])}\n")
            f.write(f"- **API Calls:** {len(flow['api_calls'])}\n")
            f.write(f"- **Data Transformations:** {len(flow['data_transformations'])}\n")
            
            f.write("\n---\n")
            f.write("*This report provides a comprehensive analysis of the entire application codebase.*\n")
            f.write("*Address critical issues before deployment for optimal performance and security.*\n")
        
        # Save JSON report
        json_path = self.root_path / 'complete_analysis_results.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        print(f"📊 Analysis complete!")
        print(f"📄 Report saved: {report_path}")
        print(f"📄 JSON data saved: {json_path}")
        
        # Print summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   🔍 {self.analysis_results['application_structure']['total_files']} files analyzed")
        print(f"   📱 {self.analysis_results['callback_validation']['total_callbacks']} callbacks found")
        print(f"   🗄️ {self.analysis_results['database_integrity']['total_records']} database records")
        print(f"   🚨 {len(self.analysis_results['critical_issues'])} critical issues")
        print(f"   🔒 {len(self.analysis_results['security_analysis']['vulnerabilities'])} security issues")
        print(f"   ⚡ {len(self.analysis_results['performance_analysis']['potential_bottlenecks'])} performance issues")
        
        return self.analysis_results

def main():
    """Main analysis function"""
    root_path = r"c:\Users\Hari\Desktop\Testin dub"
    
    analyzer = CompleteApplicationAnalyzer(root_path)
    results = analyzer.run_complete_analysis()
    
    print(f"\n🎉 Complete application analysis finished!")
    
    if results['critical_issues']:
        print(f"\n⚠️  CRITICAL ISSUES FOUND:")
        for issue in results['critical_issues']:
            print(f"   🚨 {issue['severity']}: {issue['issue']}")
    else:
        print(f"\n✅ No critical issues found!")
    
    print(f"\n📋 Next steps:")
    for rec in results['recommendations']:
        print(f"   • {rec}")

if __name__ == "__main__":
    main()
