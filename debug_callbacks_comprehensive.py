#!/usr/bin/env python3
"""
Comprehensive Dashboard Callback Debug Analysis
This script identifies all callback issues and provides fixes
"""
import os
import sys
import re
from collections import defaultdict

def analyze_callbacks():
    """Analyze all callbacks in the dashboard/callbacks.py file"""
    
    callbacks_file = "dashboard/callbacks.py"
    if not os.path.exists(callbacks_file):
        print(f"ERROR: {callbacks_file} not found")
        return
    
    print("=== COMPREHENSIVE CALLBACK ANALYSIS ===")
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @app.callback decorators and their outputs
    callback_pattern = r'@app\.callback\((.*?)\ndef\s+(\w+)'
    callbacks = re.findall(callback_pattern, content, re.DOTALL)
    
    print(f"Found {len(callbacks)} callbacks")
    
    # Extract Output components
    output_components = defaultdict(list)
    callback_info = []
    
    for i, (callback_def, func_name) in enumerate(callbacks, 1):
        # Extract outputs
        output_pattern = r'Output\([\'"]([^\'\"]+)[\'"], [\'"]([^\'\"]+)[\'"]\)'
        outputs = re.findall(output_pattern, callback_def)
        
        # Extract inputs
        input_pattern = r'Input\([\'"]([^\'\"]+)[\'"], [\'"]([^\'\"]+)[\'"]\)'
        inputs = re.findall(input_pattern, callback_def)
        
        callback_info.append({
            'id': i,
            'function': func_name,
            'outputs': outputs,
            'inputs': inputs,
            'definition': callback_def[:200] + "..." if len(callback_def) > 200 else callback_def
        })
        
        # Track output components for duplicate detection
        for component_id, prop in outputs:
            output_components[f"{component_id}.{prop}"].append((i, func_name))
    
    # Check for duplicate outputs
    print("\n=== DUPLICATE OUTPUT ANALYSIS ===")
    duplicates_found = False
    for output_key, callbacks_list in output_components.items():
        if len(callbacks_list) > 1:
            duplicates_found = True
            print(f"DUPLICATE OUTPUT: {output_key}")
            for callback_id, func_name in callbacks_list:
                print(f"  - Callback #{callback_id}: {func_name}")
    
    if not duplicates_found:
        print("No duplicate outputs found - this is good!")
    
    # Check for common issues
    print("\n=== CALLBACK ISSUE ANALYSIS ===")
    
    issue_callbacks = []
    for callback in callback_info:
        issues = []
        
        # Check for callbacks that might have API issues
        if any("API_URL" in inp[0] for inp in callback['inputs']):
            issues.append("Uses API_URL - check backend connectivity")
        
        # Check for callbacks with complex logic
        if len(callback['outputs']) > 5:
            issues.append(f"Complex callback with {len(callback['outputs'])} outputs")
        
        # Check for interval-based callbacks (potential performance issues)
        if any("interval" in inp[0] for inp in callback['inputs']):
            issues.append("Interval-based callback - check frequency")
        
        if issues:
            issue_callbacks.append((callback, issues))
    
    if issue_callbacks:
        print(f"Found {len(issue_callbacks)} callbacks with potential issues:")
        for callback, issues in issue_callbacks:
            print(f"\nCallback #{callback['id']}: {callback['function']}")
            for issue in issues:
                print(f"  - {issue}")
            print(f"  Outputs: {[f'{o[0]}.{o[1]}' for o in callback['outputs']]}")
    else:
        print("No obvious callback issues detected")
    
    # Check layout files for missing components
    print("\n=== LAYOUT COMPONENT VERIFICATION ===")
    layout_files = [
        "dashboard/layout.py",
        "dashboard/auto_trading_layout.py", 
        "dashboard/futures_trading_layout.py",
        "dashboard/binance_exact_layout.py",
        "dashboard/email_config_layout.py",
        "dashboard/hybrid_learning_layout.py"
    ]
    
    # Get all output component IDs
    all_output_ids = set()
    for callback in callback_info:
        for component_id, prop in callback['outputs']:
            all_output_ids.add(component_id)
    
    print(f"Found {len(all_output_ids)} unique output component IDs")
    
    # Check if components exist in layout files
    missing_components = []
    for layout_file in layout_files:
        if os.path.exists(layout_file):
            with open(layout_file, 'r', encoding='utf-8') as f:
                layout_content = f.read()
            
            for component_id in list(all_output_ids):
                if f'id="{component_id}"' in layout_content or f"id='{component_id}'" in layout_content:
                    all_output_ids.discard(component_id)  # Found it
    
    if all_output_ids:
        print(f"WARNING: {len(all_output_ids)} components not found in layouts:")
        for component_id in sorted(all_output_ids):
            print(f"  - {component_id}")
    else:
        print("All callback output components found in layout files")
    
    # Generate recommendations
    print("\n=== RECOMMENDATIONS ===")
    print("1. Test each callback individually using browser dev tools")
    print("2. Check backend API responses with network tab")
    print("3. Verify all component IDs exist in layout files")
    print("4. Test interval-based callbacks for performance")
    print("5. Check for JavaScript console errors")
    
    return callback_info, duplicates_found, issue_callbacks

def fix_common_issues():
    """Apply common fixes to callback issues"""
    print("\n=== APPLYING COMMON FIXES ===")
    
    callbacks_file = "dashboard/callbacks.py"
    backup_file = f"{callbacks_file}.backup"
    
    # Create backup
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy2(callbacks_file, backup_file)
        print(f"Created backup: {backup_file}")
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_applied = []
    
    # Fix 1: Add prevent_initial_call=True for callbacks that don't need it
    if 'prevent_initial_call=False' in content:
        content = content.replace('prevent_initial_call=False', 'prevent_initial_call=True')
        fixes_applied.append("Changed prevent_initial_call to True where appropriate")
    
    # Fix 2: Add error handling wrappers
    if "except:" in content and "return no_update" not in content:
        # This is a more complex fix that would need specific analysis
        pass
    
    # Fix 3: Check for missing allow_duplicate=True
    callback_lines = content.split('\n')
    for i, line in enumerate(callback_lines):
        if '@app.callback(' in line and i < len(callback_lines) - 1:
            # Check if next lines contain allow_duplicate
            next_lines = callback_lines[i:i+10]
            callback_block = '\n'.join(next_lines)
            if 'allow_duplicate=' not in callback_block and 'Output(' in callback_block:
                # This callback might need allow_duplicate=True
                pass
    
    if fixes_applied:
        with open(callbacks_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Applied fixes:")
        for fix in fixes_applied:
            print(f"  - {fix}")
    else:
        print("No automatic fixes applied")

if __name__ == "__main__":
    analyze_callbacks()
    fix_common_issues()
