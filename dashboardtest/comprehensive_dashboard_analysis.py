#!/usr/bin/env python3
"""
Comprehensive Dashboard Analysis Script
Performs a deep dive analysis of all dashboard components, callbacks, and potential issues.
"""

import os
import re
import json
from collections import defaultdict, Counter
import ast
import sys

def analyze_file(file_path):
    """Read and analyze a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def extract_callback_inputs_outputs(content):
    """Extract all callback inputs and outputs from file content."""
    callbacks = []
    
    # Find all @app.callback decorators
    callback_pattern = r'@app\.callback\s*\(\s*([^)]+)\)'
    matches = re.finditer(callback_pattern, content, re.DOTALL)
    
    for match in matches:
        callback_content = match.group(1)
        
        # Extract Output, Input, State
        outputs = re.findall(r'Output\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_content)
        inputs = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_content)
        states = re.findall(r'State\s*\(\s*[\'"]([^\'"]+)[\'"]', callback_content)
        
        callbacks.append({
            'outputs': outputs,
            'inputs': inputs,
            'states': states,
            'full_decorator': callback_content
        })
    
    return callbacks

def extract_component_ids(content):
    """Extract all component IDs from layout content."""
    # Find all id= patterns
    id_pattern = r'id\s*=\s*[\'"]([^\'"]+)[\'"]'
    ids = re.findall(id_pattern, content)
    
    # Find all children= patterns that might contain ids
    children_pattern = r'children\s*=\s*\[([^\]]+)\]'
    children_matches = re.findall(children_pattern, content, re.DOTALL)
    
    for child_content in children_matches:
        child_ids = re.findall(id_pattern, child_content)
        ids.extend(child_ids)
    
    return list(set(ids))

def find_button_components(content):
    """Find all button components and their IDs."""
    buttons = []
    
    # Find dbc.Button patterns
    button_pattern = r'dbc\.Button\s*\([^)]+\)'
    button_matches = re.finditer(button_pattern, content, re.DOTALL)
    
    for match in button_matches:
        button_content = match.group(0)
        # Extract id from button
        id_match = re.search(r'id\s*=\s*[\'"]([^\'"]+)[\'"]', button_content)
        if id_match:
            buttons.append({
                'id': id_match.group(1),
                'content': button_content
            })
    
    # Find html.Button patterns
    html_button_pattern = r'html\.Button\s*\([^)]+\)'
    html_button_matches = re.finditer(html_button_pattern, content, re.DOTALL)
    
    for match in html_button_matches:
        button_content = match.group(0)
        id_match = re.search(r'id\s*=\s*[\'"]([^\'"]+)[\'"]', button_content)
        if id_match:
            buttons.append({
                'id': id_match.group(1),
                'content': button_content
            })
    
    return buttons

def analyze_callback_conflicts(callbacks):
    """Analyze callback conflicts (multiple callbacks with same inputs)."""
    input_usage = defaultdict(list)
    
    for i, callback in enumerate(callbacks):
        for input_id in callback['inputs']:
            input_usage[input_id].append(i)
    
    conflicts = {}
    for input_id, callback_indices in input_usage.items():
        if len(callback_indices) > 1:
            conflicts[input_id] = callback_indices
    
    return conflicts

def check_api_endpoints(content):
    """Check for API endpoint calls in the content."""
    endpoints = []
    
    # Find requests.get/post patterns
    request_patterns = [
        r'requests\.get\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'requests\.post\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'requests\.put\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'requests\.delete\s*\(\s*[\'"]([^\'"]+)[\'"]'
    ]
    
    for pattern in request_patterns:
        matches = re.findall(pattern, content)
        endpoints.extend(matches)
    
    return endpoints

def main():
    """Main analysis function."""
    dashboard_path = "c:\\Users\\Hari\\Desktop\\Testin dub\\dashboardtest"
    
    print("=== COMPREHENSIVE DASHBOARD ANALYSIS ===")
    print(f"Analyzing dashboard at: {dashboard_path}")
    print("=" * 50)
    
    # Files to analyze
    files_to_analyze = [
        'callbacks.py',
        'layout.py',
        'dash_app.py',
        'app.py',
        'futures_callbacks.py',
        'binance_exact_callbacks.py'
    ]
    
    all_callbacks = []
    all_component_ids = []
    all_buttons = []
    all_endpoints = []
    
    print("\n1. ANALYZING FILES:")
    print("-" * 30)
    
    for filename in files_to_analyze:
        file_path = os.path.join(dashboard_path, filename)
        
        if os.path.exists(file_path):
            print(f"✓ Analyzing {filename}")
            content = analyze_file(file_path)
            
            if content:
                # Extract callbacks
                callbacks = extract_callback_inputs_outputs(content)
                all_callbacks.extend(callbacks)
                
                # Extract component IDs
                component_ids = extract_component_ids(content)
                all_component_ids.extend(component_ids)
                
                # Extract buttons
                buttons = find_button_components(content)
                all_buttons.extend(buttons)
                
                # Extract API endpoints
                endpoints = check_api_endpoints(content)
                all_endpoints.extend(endpoints)
                
                print(f"  - Found {len(callbacks)} callbacks")
                print(f"  - Found {len(component_ids)} component IDs")
                print(f"  - Found {len(buttons)} buttons")
                print(f"  - Found {len(endpoints)} API endpoints")
        else:
            print(f"✗ {filename} not found")
    
    print(f"\n2. SUMMARY:")
    print("-" * 30)
    print(f"Total callbacks found: {len(all_callbacks)}")
    print(f"Total component IDs found: {len(set(all_component_ids))}")
    print(f"Total buttons found: {len(all_buttons)}")
    print(f"Total API endpoints found: {len(set(all_endpoints))}")
    
    # Analyze callback conflicts
    print(f"\n3. CALLBACK CONFLICT ANALYSIS:")
    print("-" * 30)
    conflicts = analyze_callback_conflicts(all_callbacks)
    
    if conflicts:
        print("⚠️  CALLBACK CONFLICTS DETECTED:")
        for input_id, callback_indices in conflicts.items():
            print(f"  - Input '{input_id}' used by {len(callback_indices)} callbacks (indices: {callback_indices})")
            print("    This is a CRITICAL ISSUE - Dash doesn't allow multiple callbacks with the same Input!")
    else:
        print("✓ No callback conflicts detected")
    
    # Check button-callback mapping
    print(f"\n4. BUTTON-CALLBACK MAPPING:")
    print("-" * 30)
    
    button_ids = [btn['id'] for btn in all_buttons]
    callback_input_ids = set()
    for callback in all_callbacks:
        callback_input_ids.update(callback['inputs'])
    
    print("Button IDs found in layout:")
    for btn_id in button_ids:
        print(f"  - {btn_id}")
    
    print("\nButton IDs referenced in callbacks:")
    button_callback_refs = [id for id in callback_input_ids if 'btn' in id.lower() or 'button' in id.lower()]
    for btn_id in button_callback_refs:
        print(f"  - {btn_id}")
    
    # Check for missing buttons
    missing_buttons = set(button_callback_refs) - set(button_ids)
    orphaned_buttons = set(button_ids) - set(button_callback_refs)
    
    if missing_buttons:
        print(f"\n⚠️  MISSING BUTTONS (referenced in callbacks but not in layout):")
        for btn_id in missing_buttons:
            print(f"  - {btn_id}")
    
    if orphaned_buttons:
        print(f"\n⚠️  ORPHANED BUTTONS (in layout but not referenced in callbacks):")
        for btn_id in orphaned_buttons:
            print(f"  - {btn_id}")
    
    # Check component ID duplicates
    print(f"\n5. COMPONENT ID ANALYSIS:")
    print("-" * 30)
    
    id_counts = Counter(all_component_ids)
    duplicates = {id: count for id, count in id_counts.items() if count > 1}
    
    if duplicates:
        print("⚠️  DUPLICATE COMPONENT IDs:")
        for id, count in duplicates.items():
            print(f"  - '{id}' appears {count} times")
    else:
        print("✓ No duplicate component IDs detected")
    
    # API endpoint analysis
    print(f"\n6. API ENDPOINT ANALYSIS:")
    print("-" * 30)
    
    unique_endpoints = set(all_endpoints)
    for endpoint in unique_endpoints:
        print(f"  - {endpoint}")
    
    # Generate detailed report
    print(f"\n7. DETAILED CONFLICT REPORT:")
    print("-" * 30)
    
    if conflicts:
        for input_id, callback_indices in conflicts.items():
            print(f"\nCONFLICT: Input '{input_id}'")
            print(f"Used by {len(callback_indices)} callbacks:")
            
            for i, callback_index in enumerate(callback_indices):
                callback = all_callbacks[callback_index]
                print(f"  Callback {i+1}:")
                print(f"    - Outputs: {callback['outputs']}")
                print(f"    - Inputs: {callback['inputs']}")
                print(f"    - States: {callback['states']}")
                print(f"    - Decorator: {callback['full_decorator'][:100]}...")
    
    print(f"\n8. RECOMMENDATIONS:")
    print("-" * 30)
    
    if conflicts:
        print("🔴 CRITICAL FIXES NEEDED:")
        print("  1. Remove duplicate callback inputs - only ONE callback per Input ID allowed")
        print("  2. Combine callbacks or use different trigger mechanisms")
        
    if missing_buttons:
        print("🟡 MEDIUM PRIORITY:")
        print("  1. Add missing button components to layout")
        print("  2. Or remove unused callback references")
    
    if duplicates:
        print("🟡 MEDIUM PRIORITY:")
        print("  1. Remove duplicate component IDs")
        print("  2. Ensure each component has unique ID")
    
    if not conflicts and not missing_buttons and not duplicates:
        print("✅ No major structural issues detected!")
        print("   Check browser console for runtime errors")
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    
    # Save detailed report
    report_path = os.path.join(dashboard_path, 'comprehensive_analysis_report.json')
    
    report = {
        'total_callbacks': len(all_callbacks),
        'total_component_ids': len(set(all_component_ids)),
        'total_buttons': len(all_buttons),
        'callback_conflicts': conflicts,
        'missing_buttons': list(missing_buttons),
        'orphaned_buttons': list(orphaned_buttons),
        'duplicate_ids': duplicates,
        'api_endpoints': list(unique_endpoints),
        'button_ids': button_ids,
        'callback_input_ids': list(callback_input_ids)
    }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Detailed report saved to: {report_path}")

if __name__ == "__main__":
    main()
