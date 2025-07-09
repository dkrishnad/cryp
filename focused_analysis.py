#!/usr/bin/env python3
"""
Focused Application Analysis - Buttons, Charts, Callbacks, Data Flow
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

def analyze_buttons_and_charts():
    """Analyze all buttons, charts, and UI components"""
    root_path = Path(r"c:\Users\Hari\Desktop\Testin dub")
    
    print("🔍 ANALYZING BUTTONS, CHARTS, AND UI COMPONENTS")
    print("=" * 60)
    
    # Files to analyze
    key_files = [
        'dashboardtest/layout.py',
        'dashboardtest/callbacks.py',
        'dashboardtest/app.py',
        'main.py'
    ]
    
    analysis_results = {
        'buttons': [],
        'charts': [],
        'callbacks': [],
        'components': [],
        'data_flow': [],
        'issues': []
    }
    
    for file_path in key_files:
        full_path = root_path / file_path
        if not full_path.exists():
            analysis_results['issues'].append(f"Missing file: {file_path}")
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 ANALYZING: {file_path}")
            print("-" * 40)
            
            # Find buttons
            button_patterns = [
                r'dbc\.Button\s*\(\s*[\'"]([^\'\"]*)[\'"].*?id\s*=\s*[\'"]([^\'\"]+)[\'"]',
                r'html\.Button\s*\(\s*[\'"]([^\'\"]*)[\'"].*?id\s*=\s*[\'"]([^\'\"]+)[\'"]',
                r'id\s*=\s*[\'"]([^\'\"]*button[^\'\"]*)[\'"]',
                r'id\s*=\s*[\'"]([^\'\"]*btn[^\'\"]*)[\'"]'
            ]
            
            buttons_found = []
            for pattern in button_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        if len(match) == 2:
                            buttons_found.append({'text': match[0], 'id': match[1], 'file': file_path})
                        else:
                            buttons_found.append({'text': '', 'id': match[0], 'file': file_path})
                    else:
                        buttons_found.append({'text': '', 'id': match, 'file': file_path})
            
            print(f"🔘 Found {len(buttons_found)} buttons:")
            for btn in buttons_found:
                print(f"   • {btn['id']}: {btn['text'][:30]}...")
                analysis_results['buttons'].append(btn)
            
            # Find charts
            chart_patterns = [
                r'dcc\.Graph\s*\(\s*id\s*=\s*[\'"]([^\'\"]+)[\'"]',
                r'go\.Figure\s*\(',
                r'px\.\w+\s*\(',
                r'plotly',
                r'chart',
                r'graph'
            ]
            
            charts_found = []
            for pattern in chart_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    charts_found.append({'id': match, 'file': file_path})
            
            print(f"📊 Found {len(charts_found)} chart components:")
            for chart in charts_found:
                print(f"   • {chart['id']}")
                analysis_results['charts'].append(chart)
            
            # Find callbacks
            callback_patterns = [
                r'@app\.callback\s*\(\s*(.*?)\s*\)\s*def\s+(\w+)\s*\(',
                r'def\s+(\w*callback\w*)\s*\('
            ]
            
            callbacks_found = []
            for pattern in callback_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        callbacks_found.append({'definition': match[0], 'function': match[1], 'file': file_path})
                    else:
                        callbacks_found.append({'definition': '', 'function': match, 'file': file_path})
            
            print(f"📱 Found {len(callbacks_found)} callbacks:")
            for cb in callbacks_found:
                print(f"   • {cb['function']}")
                analysis_results['callbacks'].append(cb)
            
            # Find other components
            component_patterns = [
                r'dbc\.\w+\s*\(',
                r'html\.\w+\s*\(',
                r'dcc\.\w+\s*\(',
                r'id\s*=\s*[\'"]([^\'\"]+)[\'"]'
            ]
            
            components_found = set()
            for pattern in component_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                components_found.update(matches)
            
            print(f"🧩 Found {len(components_found)} total components")
            analysis_results['components'].extend(list(components_found))
            
        except Exception as e:
            error_msg = f"Error analyzing {file_path}: {str(e)}"
            print(f"❌ {error_msg}")
            analysis_results['issues'].append(error_msg)
    
    return analysis_results

def analyze_callback_button_mapping():
    """Analyze the mapping between buttons and callbacks"""
    root_path = Path(r"c:\Users\Hari\Desktop\Testin dub")
    
    print("\n🔗 ANALYZING BUTTON-CALLBACK MAPPING")
    print("=" * 60)
    
    # Read callbacks file
    callbacks_file = root_path / 'dashboardtest/callbacks.py'
    layout_file = root_path / 'dashboardtest/layout.py'
    
    if not callbacks_file.exists():
        print("❌ Callbacks file not found")
        return {}
    
    try:
        with open(callbacks_file, 'r', encoding='utf-8') as f:
            callbacks_content = f.read()
        
        # Extract all Input/Output mappings
        callback_mappings = []
        
        # Find complete callback definitions
        callback_pattern = r'@app\.callback\s*\(\s*(.*?)\s*\)\s*def\s+(\w+)\s*\('
        callbacks = re.findall(callback_pattern, callbacks_content, re.DOTALL)
        
        print(f"📱 Found {len(callbacks)} callback functions")
        
        for callback_def, func_name in callbacks:
            # Extract Outputs
            output_pattern = r'Output\s*\(\s*[\'"]([^\'\"]+)[\'"]'
            outputs = re.findall(output_pattern, callback_def)
            
            # Extract Inputs
            input_pattern = r'Input\s*\(\s*[\'"]([^\'\"]+)[\'"]'
            inputs = re.findall(input_pattern, callback_def)
            
            # Extract States
            state_pattern = r'State\s*\(\s*[\'"]([^\'\"]+)[\'"]'
            states = re.findall(state_pattern, callback_def)
            
            mapping = {
                'function': func_name,
                'outputs': outputs,
                'inputs': inputs,
                'states': states
            }
            
            callback_mappings.append(mapping)
            
            print(f"\n🔄 {func_name}:")
            print(f"   Outputs: {outputs}")
            print(f"   Inputs: {inputs}")
            if states:
                print(f"   States: {states}")
        
        # Check for orphaned components
        if layout_file.exists():
            with open(layout_file, 'r', encoding='utf-8') as f:
                layout_content = f.read()
            
            # Find all IDs in layout
            layout_ids = set(re.findall(r'id\s*=\s*[\'"]([^\'\"]+)[\'"]', layout_content))
            
            # Find all callback component IDs
            callback_ids = set()
            for mapping in callback_mappings:
                callback_ids.update(mapping['outputs'])
                callback_ids.update(mapping['inputs'])
                callback_ids.update(mapping['states'])
            
            orphaned_layout = layout_ids - callback_ids
            orphaned_callbacks = callback_ids - layout_ids
            
            print(f"\n📊 COMPONENT MAPPING ANALYSIS:")
            print(f"   Layout components: {len(layout_ids)}")
            print(f"   Callback components: {len(callback_ids)}")
            print(f"   Orphaned layout components: {len(orphaned_layout)}")
            print(f"   Orphaned callback components: {len(orphaned_callbacks)}")
            
            if orphaned_layout:
                print(f"\n⚠️  Layout components without callbacks:")
                for component in sorted(orphaned_layout):
                    print(f"   • {component}")
            
            if orphaned_callbacks:
                print(f"\n⚠️  Callback components not in layout:")
                for component in sorted(orphaned_callbacks):
                    print(f"   • {component}")
        
        return callback_mappings
        
    except Exception as e:
        print(f"❌ Error analyzing callback mappings: {e}")
        return {}

def analyze_data_flow():
    """Analyze data flow through the application"""
    root_path = Path(r"c:\Users\Hari\Desktop\Testin dub")
    
    print("\n🔄 ANALYZING DATA FLOW")
    print("=" * 60)
    
    # Key files for data flow
    data_files = [
        'backendtest/data_collection.py',
        'backendtest/app.py',
        'dashboardtest/callbacks.py',
        'main.py'
    ]
    
    data_flow_analysis = {
        'api_calls': [],
        'database_operations': [],
        'data_transformations': [],
        'external_services': []
    }
    
    for file_path in data_files:
        full_path = root_path / file_path
        if not full_path.exists():
            continue
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 {file_path}:")
            
            # API calls
            api_patterns = [
                r'requests\.(get|post|put|delete)\s*\(',
                r'make_api_call\s*\(',
                r'aiohttp\.',
                r'api\.binance\.com',
                r'@app\.route'
            ]
            
            api_calls = []
            for pattern in api_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                api_calls.extend(matches)
            
            print(f"   🌐 API calls: {len(api_calls)}")
            data_flow_analysis['api_calls'].extend(api_calls)
            
            # Database operations
            db_patterns = [
                r'sqlite3\.connect',
                r'cursor\.execute',
                r'CREATE TABLE',
                r'INSERT INTO',
                r'SELECT.*FROM',
                r'UPDATE.*SET',
                r'DELETE FROM'
            ]
            
            db_ops = []
            for pattern in db_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                db_ops.extend(matches)
            
            print(f"   🗄️  Database operations: {len(db_ops)}")
            data_flow_analysis['database_operations'].extend(db_ops)
            
            # Data transformations
            transform_patterns = [
                r'pd\.DataFrame',
                r'pd\.read_',
                r'\.to_dict\(',
                r'\.to_json\(',
                r'json\.loads',
                r'json\.dumps',
                r'np\.',
                r'talib\.'
            ]
            
            transforms = []
            for pattern in transform_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                transforms.extend(matches)
            
            print(f"   🔄 Data transformations: {len(transforms)}")
            data_flow_analysis['data_transformations'].extend(transforms)
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
    
    return data_flow_analysis

def check_file_integrity():
    """Check integrity of all key files"""
    root_path = Path(r"c:\Users\Hari\Desktop\Testin dub")
    
    print("\n🔍 CHECKING FILE INTEGRITY")
    print("=" * 60)
    
    # Define all key files
    key_files = {
        'main.py': 'Main application entry point',
        'dashboardtest/app.py': 'Dashboard application',
        'dashboardtest/layout.py': 'Dashboard layout',
        'dashboardtest/callbacks.py': 'Dashboard callbacks',
        'backendtest/app.py': 'Backend API application',
        'backendtest/data_collection.py': 'Data collection system',
        'backendtest/trading.py': 'Trading logic',
        'backendtest/ml_models.py': 'ML models',
        'trades.db': 'Main database'
    }
    
    integrity_results = {
        'existing_files': [],
        'missing_files': [],
        'file_sizes': {},
        'syntax_errors': [],
        'import_errors': []
    }
    
    for file_path, description in key_files.items():
        full_path = root_path / file_path
        
        if full_path.exists():
            try:
                stat = full_path.stat()
                file_info = {
                    'path': file_path,
                    'description': description,
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                }
                integrity_results['existing_files'].append(file_info)
                integrity_results['file_sizes'][file_path] = stat.st_size
                
                print(f"✅ {file_path}: {stat.st_size} bytes - {description}")
                
                # Check Python files for syntax
                if file_path.endswith('.py'):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Try to compile
                        compile(content, file_path, 'exec')
                        
                        # Check for basic imports
                        if 'import' in content:
                            print(f"   📦 Contains import statements")
                        
                    except SyntaxError as e:
                        error_info = f"Syntax error in {file_path}: {e}"
                        integrity_results['syntax_errors'].append(error_info)
                        print(f"   ❌ {error_info}")
                    except Exception as e:
                        error_info = f"Error reading {file_path}: {e}"
                        integrity_results['import_errors'].append(error_info)
                        print(f"   ⚠️  {error_info}")
                
            except Exception as e:
                print(f"❌ Error checking {file_path}: {e}")
        else:
            integrity_results['missing_files'].append(file_path)
            print(f"❌ {file_path}: MISSING - {description}")
    
    print(f"\n📊 INTEGRITY SUMMARY:")
    print(f"   ✅ Existing files: {len(integrity_results['existing_files'])}")
    print(f"   ❌ Missing files: {len(integrity_results['missing_files'])}")
    print(f"   🚨 Syntax errors: {len(integrity_results['syntax_errors'])}")
    print(f"   ⚠️  Import errors: {len(integrity_results['import_errors'])}")
    
    return integrity_results

def main():
    """Main analysis function"""
    print("🚀 COMPREHENSIVE APPLICATION ANALYSIS")
    print("=" * 80)
    
    # Run all analyses
    buttons_charts = analyze_buttons_and_charts()
    callback_mappings = analyze_callback_button_mapping()
    data_flow = analyze_data_flow()
    file_integrity = check_file_integrity()
    
    # Generate summary
    print("\n📋 FINAL SUMMARY")
    print("=" * 80)
    
    print(f"🔘 Total Buttons: {len(buttons_charts['buttons'])}")
    print(f"📊 Total Charts: {len(buttons_charts['charts'])}")
    print(f"📱 Total Callbacks: {len(buttons_charts['callbacks'])}")
    print(f"🧩 Total Components: {len(set(buttons_charts['components']))}")
    print(f"🌐 API Calls: {len(data_flow['api_calls'])}")
    print(f"🗄️  Database Operations: {len(data_flow['database_operations'])}")
    print(f"🔄 Data Transformations: {len(data_flow['data_transformations'])}")
    print(f"✅ Existing Files: {len(file_integrity['existing_files'])}")
    print(f"❌ Missing Files: {len(file_integrity['missing_files'])}")
    print(f"🚨 Issues Found: {len(buttons_charts['issues'])}")
    
    # Save results
    results = {
        'buttons_charts': buttons_charts,
        'callback_mappings': callback_mappings,
        'data_flow': data_flow,
        'file_integrity': file_integrity
    }
    
    # Save to JSON
    with open('focused_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to: focused_analysis_results.json")
    
    if file_integrity['missing_files']:
        print(f"\n⚠️  CRITICAL: Missing files detected!")
        for missing in file_integrity['missing_files']:
            print(f"   • {missing}")
    
    if file_integrity['syntax_errors']:
        print(f"\n🚨 CRITICAL: Syntax errors detected!")
        for error in file_integrity['syntax_errors']:
            print(f"   • {error}")
    
    if buttons_charts['issues']:
        print(f"\n⚠️  Issues found during analysis:")
        for issue in buttons_charts['issues']:
            print(f"   • {issue}")

if __name__ == "__main__":
    main()
