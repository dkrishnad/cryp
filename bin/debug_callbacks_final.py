#!/usr/bin/env python3
"""
Final callback debugging to identify and fix all remaining issues
"""
import sys
import os
import importlib.util
import traceback
import re

def analyze_callbacks_final():
    """Comprehensive final analysis of callback issues"""
    
    print("=== FINAL CALLBACK ANALYSIS ===")
    
    # 1. Check if all callback modules can be imported
    dashboard_dir = os.path.join(os.getcwd(), 'dashboard')
    callback_files = [
        'callbacks.py',
        'layout.py', 
        'dash_app.py',
        'auto_trading_layout.py',
        'futures_trading_layout.py',
        'binance_exact_layout.py',
        'email_config_layout.py',
        'hybrid_learning_layout.py'
    ]
    
    print("\n1. CHECKING MODULE IMPORTS:")
    for file in callback_files:
        file_path = os.path.join(dashboard_dir, file)
        if os.path.exists(file_path):
            try:
                spec = importlib.util.spec_from_file_location(file[:-3], file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"  ✅ {file}: Successfully imported")
                else:
                    print(f"  ❌ {file}: Could not create module spec")
            except Exception as e:
                print(f"  ❌ {file}: Error - {e}")
                traceback.print_exc()
        else:
            print(f"  ⚠️  {file}: File not found")
    
    # 2. Analyze callback structure in callbacks.py
    print("\n2. ANALYZING CALLBACK STRUCTURE:")
    callbacks_path = os.path.join(dashboard_dir, 'callbacks.py')
    if os.path.exists(callbacks_path):
        with open(callbacks_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Count callback decorators
        callback_decorators = re.findall(r'@app\.callback\s*\(', content)
        callback_functions = re.findall(r'def\s+(\w+)\s*\(.*\):', content)
        output_patterns = re.findall(r'Output\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
        input_patterns = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
        
        print(f"  Total @app.callback decorators: {len(callback_decorators)}")
        print(f"  Total callback functions: {len(callback_functions)}")
        print(f"  Total Output components: {len(output_patterns)}")
        print(f"  Total Input components: {len(input_patterns)}")
        
        # Check for duplicate outputs
        output_counts = {}
        for output in output_patterns:
            output_counts[output] = output_counts.get(output, 0) + 1
        
        duplicates = {k: v for k, v in output_counts.items() if v > 1}
        if duplicates:
            print(f"  ⚠️  Potential duplicate outputs: {duplicates}")
        else:
            print("  ✅ No duplicate outputs found")
            
        # Check for common problematic patterns
        print("\n3. CHECKING FOR COMMON ISSUES:")
        
        # Check for missing component IDs in layout
        layout_path = os.path.join(dashboard_dir, 'layout.py')
        if os.path.exists(layout_path):
            with open(layout_path, 'r', encoding='utf-8') as f:
                layout_content = f.read()
            
            # Find all id= declarations in layout
            layout_ids = re.findall(r'id\s*=\s*[\'"]([^\'"]+)[\'"]', layout_content)
            layout_ids = set(layout_ids)
            
            missing_outputs = []
            missing_inputs = []
            
            for output_id in set(output_patterns):
                if output_id not in layout_ids:
                    missing_outputs.append(output_id)
            
            for input_id in set(input_patterns):
                if input_id not in layout_ids:
                    missing_inputs.append(input_id)
            
            if missing_outputs:
                print(f"  ❌ Missing output component IDs in layout: {missing_outputs}")
            else:
                print("  ✅ All output component IDs found in layout")
                
            if missing_inputs:
                print(f"  ❌ Missing input component IDs in layout: {missing_inputs}")
            else:
                print("  ✅ All input component IDs found in layout")
    
    # 3. Check for interval callback issues
    print("\n4. CHECKING INTERVAL CALLBACKS:")
    if os.path.exists(callbacks_path):
        interval_callbacks = re.findall(r'Input\s*\(\s*[\'"]([^\'\"]*interval[^\'\"]*)[\'"].*?[\'"]n_intervals[\'"]', content)
        print(f"  Found {len(interval_callbacks)} interval callbacks: {interval_callbacks}")
        
        # Check if prevent_initial_call is used
        prevent_initial_calls = content.count('prevent_initial_call=True')
        print(f"  Callbacks with prevent_initial_call=True: {prevent_initial_calls}")
    else:
        print("  ⚠️  callbacks.py not found")
    
    # 4. Check backend connectivity
    print("\n5. CHECKING BACKEND CONNECTIVITY:")
    try:
        import requests
        backend_endpoints = [
            'http://localhost:8000/health',
            'http://localhost:8000/balance',
            'http://localhost:8000/live_price/btcusdt',
            'http://localhost:8000/prediction/btcusdt'
        ]
        
        for endpoint in backend_endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                print(f"  ✅ {endpoint}: Status {response.status_code}")
            except Exception as e:
                print(f"  ❌ {endpoint}: Error - {e}")
                
    except ImportError:
        print("  ⚠️  requests module not available")
    
    print("\n=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    analyze_callbacks_final()
