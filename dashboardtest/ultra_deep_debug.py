#!/usr/bin/env python3
"""
ULTRA DEEP DIVE - Dashboard Debug Analysis
Check every single component, ID, callback, and potential issue
"""

import os
import re
import json
from datetime import datetime

def analyze_layout_ids():
    """Extract all IDs from layout files"""
    print("\n🔍 ULTRA DEEP: LAYOUT ID ANALYSIS")
    print("="*60)
    
    layout_files = [
        "layout.py",
        "auto_trading_layout.py", 
        "futures_trading_layout.py",
        "email_config_layout.py",
        "hybrid_learning_layout.py",
        "binance_exact_layout.py"
    ]
    
    all_ids = {}
    duplicates = []
    
    for file in layout_files:
        if os.path.exists(file):
            print(f"\n📄 Analyzing {file}...")
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all id= patterns
            id_patterns = re.findall(r'id=["\']([^"\']+)["\']', content)
            file_ids = {}
            
            for id_val in id_patterns:
                if id_val in file_ids:
                    file_ids[id_val] += 1
                else:
                    file_ids[id_val] = 1
                
                # Check for duplicates across files
                if id_val in all_ids:
                    duplicates.append((id_val, all_ids[id_val], file))
                else:
                    all_ids[id_val] = file
            
            print(f"   📊 Found {len(file_ids)} unique IDs")
            
            # Check for duplicates within file
            file_duplicates = {k: v for k, v in file_ids.items() if v > 1}
            if file_duplicates:
                print(f"   ❌ DUPLICATES IN FILE: {file_duplicates}")
            else:
                print(f"   ✅ No duplicates in file")
        else:
            print(f"   ❌ File not found: {file}")
    
    print(f"\n📊 TOTAL UNIQUE IDS: {len(all_ids)}")
    
    if duplicates:
        print(f"\n❌ CROSS-FILE DUPLICATES FOUND:")
        for dup_id, file1, file2 in duplicates:
            print(f"   🔴 '{dup_id}': {file1} & {file2}")
    else:
        print(f"\n✅ NO CROSS-FILE DUPLICATES")
    
    return all_ids, duplicates

def analyze_callback_registrations():
    """Deep analysis of callback registrations"""
    print("\n🔍 ULTRA DEEP: CALLBACK REGISTRATION ANALYSIS")
    print("="*60)
    
    callback_files = [
        "callbacks.py",
        "futures_callbacks.py", 
        "binance_exact_callbacks.py"
    ]
    
    total_callbacks = 0
    callback_inputs = []
    callback_outputs = []
    
    for file in callback_files:
        if os.path.exists(file):
            print(f"\n📄 Analyzing {file}...")
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count @app.callback decorators
            callbacks = re.findall(r'@app\.callback\s*\(', content)
            print(f"   📊 Found {len(callbacks)} @app.callback decorators")
            total_callbacks += len(callbacks)
            
            # Extract Input() patterns
            inputs = re.findall(r'Input\(["\']([^"\']+)["\'],\s*["\']([^"\']+)["\']', content)
            for input_id, input_prop in inputs:
                callback_inputs.append((input_id, input_prop, file))
            print(f"   📊 Found {len(inputs)} Input declarations")
            
            # Extract Output() patterns  
            outputs = re.findall(r'Output\(["\']([^"\']+)["\'],\s*["\']([^"\']+)["\']', content)
            for output_id, output_prop in outputs:
                callback_outputs.append((output_id, output_prop, file))
            print(f"   📊 Found {len(outputs)} Output declarations")
            
        else:
            print(f"   ❌ File not found: {file}")
    
    print(f"\n📊 TOTAL CALLBACKS: {total_callbacks}")
    print(f"📊 TOTAL INPUTS: {len(callback_inputs)}")
    print(f"📊 TOTAL OUTPUTS: {len(callback_outputs)}")
    
    return callback_inputs, callback_outputs

def analyze_button_callback_mapping(layout_ids, callback_inputs):
    """Check if every button has a corresponding callback"""
    print("\n🔍 ULTRA DEEP: BUTTON-CALLBACK MAPPING")
    print("="*60)
    
    # Find button IDs from layout
    button_patterns = [
        r'dbc\.Button[^}]*id=["\']([^"\']+)["\']',
        r'html\.Button[^}]*id=["\']([^"\']+)["\']',
        r'dcc\.Button[^}]*id=["\']([^"\']+)["\']'
    ]
    
    button_ids = set()
    for file, ids in layout_ids.items():
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in button_patterns:
                matches = re.findall(pattern, content)
                button_ids.update(matches)
    
    print(f"📊 BUTTON IDs FOUND: {len(button_ids)}")
    for btn_id in sorted(button_ids):
        print(f"   🔘 {btn_id}")
    
    # Check which buttons have callbacks
    input_ids = {inp[0] for inp in callback_inputs}
    
    print(f"\n📊 CALLBACK INPUT IDs: {len(input_ids)}")
    
    mapped_buttons = button_ids & input_ids
    unmapped_buttons = button_ids - input_ids
    extra_inputs = input_ids - button_ids
    
    print(f"\n✅ MAPPED BUTTONS ({len(mapped_buttons)}):")
    for btn in sorted(mapped_buttons):
        print(f"   ✅ {btn}")
    
    print(f"\n❌ UNMAPPED BUTTONS ({len(unmapped_buttons)}):")
    for btn in sorted(unmapped_buttons):
        print(f"   ❌ {btn}")
    
    print(f"\n⚠️  EXTRA CALLBACK INPUTS ({len(extra_inputs)}):")
    for inp in sorted(extra_inputs):
        print(f"   ⚠️  {inp}")
    
    return mapped_buttons, unmapped_buttons, extra_inputs

def analyze_api_calls():
    """Check all make_api_call usage"""
    print("\n🔍 ULTRA DEEP: API CALL ANALYSIS")
    print("="*60)
    
    callback_files = ["callbacks.py", "futures_callbacks.py", "binance_exact_callbacks.py"]
    
    api_calls = []
    for file in callback_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find make_api_call patterns
            calls = re.findall(r'make_api_call\(["\']([^"\']+)["\'],\s*["\']([^"\']+)["\']', content)
            for method, endpoint in calls:
                api_calls.append((method, endpoint, file))
    
    print(f"📊 API CALLS FOUND: {len(api_calls)}")
    
    # Group by endpoint
    endpoint_counts = {}
    for method, endpoint, file in api_calls:
        key = f"{method.upper()} {endpoint}"
        if key in endpoint_counts:
            endpoint_counts[key] += 1
        else:
            endpoint_counts[key] = 1
        print(f"   📡 {method.upper()} {endpoint} (in {file})")
    
    return api_calls

def analyze_debug_logging():
    """Check debug logging setup"""
    print("\n🔍 ULTRA DEEP: DEBUG LOGGING ANALYSIS") 
    print("="*60)
    
    # Check debug_logger.py
    if os.path.exists("debug_logger.py"):
        print("✅ debug_logger.py exists")
        with open("debug_logger.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key functions
        functions = ["debug_callback", "debug_api_call", "log_button_click"]
        for func in functions:
            if f"def {func}" in content:
                print(f"   ✅ Function {func} defined")
            else:
                print(f"   ❌ Function {func} missing")
    else:
        print("❌ debug_logger.py not found")
    
    # Check log files
    log_files = ["dashboard_debug.log", "debug.log"]
    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            print(f"✅ {log_file}: {size} bytes, {len(lines)} lines")
            
            # Check for recent debug entries
            recent_debug = [line for line in lines[-20:] if "DEBUG" in line]
            recent_error = [line for line in lines[-20:] if "ERROR" in line]
            
            print(f"   📊 Recent DEBUG entries: {len(recent_debug)}")
            print(f"   📊 Recent ERROR entries: {len(recent_error)}")
            
            if recent_error:
                print("   🔴 Recent errors:")
                for error in recent_error[-3:]:
                    print(f"      {error.strip()}")
        else:
            print(f"❌ {log_file} not found")

def check_import_issues():
    """Check for import issues in dashboard files"""
    print("\n🔍 ULTRA DEEP: IMPORT ANALYSIS")
    print("="*60)
    
    files_to_check = [
        "app.py", "dash_app.py", "callbacks.py", "layout.py", 
        "debug_logger.py", "utils.py"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"\n📄 Checking imports in {file}...")
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find import statements
            imports = re.findall(r'^(?:from\s+[\w.]+\s+)?import\s+[\w,\s*]+', content, re.MULTILINE)
            print(f"   📊 Found {len(imports)} import statements")
            
            # Check for specific critical imports
            critical_imports = {
                "dash": "import dash" in content or "from dash import" in content,
                "callbacks": "import callbacks" in content or "from callbacks import" in content,
                "layout": "import layout" in content or "from layout import" in content,
                "debug_logger": "import debug_logger" in content or "from debug_logger import" in content
            }
            
            for imp, found in critical_imports.items():
                status = "✅" if found else "❌"
                print(f"   {status} {imp}")
        else:
            print(f"❌ File not found: {file}")

def main():
    print("🔍 ULTRA DEEP DIVE - DASHBOARD DEBUG ANALYSIS")
    print("="*70)
    print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {os.getcwd()}")
    
    # 1. Layout ID Analysis
    layout_ids, duplicates = analyze_layout_ids()
    
    # 2. Callback Registration Analysis
    callback_inputs, callback_outputs = analyze_callback_registrations()
    
    # 3. Button-Callback Mapping
    mapped, unmapped, extra = analyze_button_callback_mapping({"layout.py": layout_ids}, callback_inputs)
    
    # 4. API Call Analysis
    api_calls = analyze_api_calls()
    
    # 5. Debug Logging Analysis
    analyze_debug_logging()
    
    # 6. Import Analysis
    check_import_issues()
    
    # Final Summary
    print("\n🎯 ULTRA DEEP ANALYSIS SUMMARY")
    print("="*70)
    
    issues = []
    if duplicates:
        issues.append(f"Duplicate IDs: {len(duplicates)}")
    if unmapped:
        issues.append(f"Unmapped buttons: {len(unmapped)}")
    
    if issues:
        print(f"❌ CRITICAL ISSUES: {', '.join(issues)}")
        print("\n🔧 PRIORITY FIXES:")
        if duplicates:
            print("   1. Fix duplicate component IDs")
        if unmapped:
            print("   2. Add callbacks for unmapped buttons")
    else:
        print("✅ NO CRITICAL ISSUES FOUND")
        print("\n💡 NEXT STEPS:")
        print("   1. Check browser console for JavaScript errors")
        print("   2. Test individual button clicks with debug logging")
        print("   3. Verify dashboard is properly loading in browser")

if __name__ == "__main__":
    main()
