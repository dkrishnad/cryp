#!/usr/bin/env python3
"""
Comprehensive Dashboard Analysis Tool
Checks all components, callbacks, and identifies missing functionality
"""

import os
import re
import json
from pathlib import Path

def analyze_layout_components():
    """Extract all component IDs from layout.py"""
    print("=== ANALYZING LAYOUT COMPONENTS ===\n")
    
    with open("dashboard/layout.py", "r", encoding="utf-8") as f:
        layout_content = f.read()
    
    # Find all id patterns
    id_patterns = [
        r'id="([^"]+)"',
        r"id='([^']+)'",
    ]
    
    all_ids = set()
    for pattern in id_patterns:
        matches = re.findall(pattern, layout_content)
        all_ids.update(matches)
    
    # Categorize IDs
    categories = {
        "Inputs/Controls": [],
        "Outputs/Display": [],
        "Buttons": [],
        "Tables": [],
        "Graphs": [],
        "Stores": [],
        "Intervals": [],
        "Uploads": [],
        "Tabs": [],
        "Other": []
    }
    
    for component_id in sorted(all_ids):
        if any(word in component_id for word in ["btn", "button"]):
            categories["Buttons"].append(component_id)
        elif any(word in component_id for word in ["table", "datatable"]):
            categories["Tables"].append(component_id)
        elif any(word in component_id for word in ["graph", "chart"]):
            categories["Graphs"].append(component_id)
        elif any(word in component_id for word in ["store", "cache"]):
            categories["Stores"].append(component_id)
        elif "interval" in component_id:
            categories["Intervals"].append(component_id)
        elif "upload" in component_id:
            categories["Uploads"].append(component_id)
        elif "tab" in component_id:
            categories["Tabs"].append(component_id)
        elif any(word in component_id for word in ["input", "dropdown", "slider", "checklist", "radio", "toggle", "switch"]):
            categories["Inputs/Controls"].append(component_id)
        elif any(word in component_id for word in ["output", "result", "display", "status", "list", "metrics", "monitor"]):
            categories["Outputs/Display"].append(component_id)
        else:
            categories["Other"].append(component_id)
    
    print(f"Found {len(all_ids)} total components:\n")
    
    for category, items in categories.items():
        if items:
            print(f"{category} ({len(items)}):")
            for item in items:
                print(f"   {item}")
            print()
    
    return categories

def analyze_callbacks():
    """Extract all callbacks from callbacks.py"""
    
    print("=== ANALYZING CALLBACKS ===\n")
    
    with open("dashboard/callbacks.py", "r", encoding="utf-8") as f:
        callbacks_content = f.read()
    
    # Find callback decorators and their inputs/outputs
    callback_pattern = r'@app\.callback\((.*?)\)\s*def\s+(\w+)'
    callbacks = re.findall(callback_pattern, callbacks_content, re.DOTALL)
    
    print(f"Found {len(callbacks)} callbacks:\n")
    
    callback_info = []
    for i, (params, func_name) in enumerate(callbacks):
        # Extract outputs and inputs
        output_pattern = r'Output\([\'"]([^\'"]+)[\'"]'
        input_pattern = r'Input\([\'"]([^\'"]+)[\'"]'
        
        outputs = re.findall(output_pattern, params)
        inputs = re.findall(input_pattern, params)
        
        callback_info.append({
            "function": func_name,
            "outputs": outputs,
            "inputs": inputs
        })
        
        print(f"{i+1}. {func_name}")
        print(f"   Outputs: {outputs}")
        print(f"   Inputs: {inputs}")
        print()
    
    return callback_info

def find_missing_callbacks(components, callbacks):
    """Find components that need callbacks but don't have them"""
    
    print("=== FINDING MISSING CALLBACKS ===\n")
    
    # Get all component IDs that have callbacks
    components_with_callbacks = set()
    for cb in callbacks:
        components_with_callbacks.update(cb["outputs"])
        components_with_callbacks.update(cb["inputs"])
    
    # Find missing callbacks
    missing_callbacks = {}
    
    # Buttons should have callbacks (as inputs)
    button_inputs = set()
    for cb in callbacks:
        for inp in cb["inputs"]:
            if any(word in inp for word in ["btn", "button"]):
                button_inputs.add(inp)
    
    missing_callbacks["Buttons without callbacks"] = []
    for btn in components["Buttons"]:
        if btn not in button_inputs:
            missing_callbacks["Buttons without callbacks"].append(btn)
    
    # Output divs should have callbacks
    output_callbacks = set()
    for cb in callbacks:
        output_callbacks.update(cb["outputs"])
    
    missing_callbacks["Output divs without callbacks"] = []
    for output in components["Outputs/Display"]:
        if output not in output_callbacks:
            missing_callbacks["Output divs without callbacks"].append(output)
    
    # Tables should have callbacks
    missing_callbacks["Tables without callbacks"] = []
    for table in components["Tables"]:
        if table not in output_callbacks:
            missing_callbacks["Tables without callbacks"].append(table)
    
    # Graphs should have callbacks
    missing_callbacks["Graphs without callbacks"] = []
    for graph in components["Graphs"]:
        if graph not in output_callbacks:
            missing_callbacks["Graphs without callbacks"].append(graph)
    
    # Print results
    for category, missing in missing_callbacks.items():
        if missing:
            print(f"{category} ({len(missing)}):")
            for item in missing:
                print(f"   ❌ {item}")
            print()
        else:
            print(f"{category}: ✅ All have callbacks\n")
    
    return missing_callbacks

def check_backend_endpoints():
    """Check which backend endpoints are being used in callbacks"""
    
    print("=== CHECKING BACKEND ENDPOINT USAGE ===\n")
    
    with open("dashboard/callbacks.py", "r", encoding="utf-8") as f:
        callbacks_content = f.read()
    
    # Find all API calls
    api_pattern = r'requests\.(get|post|put|delete)\(f?"?{API_URL}([^"]+)"?'
    api_calls = re.findall(api_pattern, callbacks_content)
    
    endpoints = {}
    for method, endpoint in api_calls:
        method = method.upper()
        endpoint = endpoint.replace('"', '').replace("'", '')
        if endpoint not in endpoints:
            endpoints[endpoint] = []
        if method not in endpoints[endpoint]:
            endpoints[endpoint].append(method)
    
    print(f"Found {len(endpoints)} unique endpoints:\n")
    
    for endpoint, methods in sorted(endpoints.items()):
        print(f"{endpoint}")
        for method in methods:
            print(f"   {method}")
        print()
    
    return endpoints

def analyze_tab_content():
    """Check if all tabs have proper content"""
    
    print("=== ANALYZING TAB CONTENT ===\n")
    
    # Find tab-related callbacks
    with open("dashboard/callbacks.py", "r", encoding="utf-8") as f:
        callbacks_content = f.read()
    
    tab_callbacks = []
    lines = callbacks_content.split('\n')
    for i, line in enumerate(lines):
        if 'tab-content' in line and 'Output' in line:
            # Find the function name
            for j in range(i, min(i+10, len(lines))):
                if 'def ' in lines[j]:
                    func_name = re.search(r'def\s+(\w+)', lines[j])
                    if func_name:
                        tab_callbacks.append({
                            "output": line.strip(),
                            "function": func_name.group(1)
                        })
                    break
    
    print(f"Found {len(tab_callbacks)} tab content callbacks:")
    for tab in tab_callbacks:
        print(f"   {tab['function']}: {tab['output']}")
    
    return tab_callbacks

def generate_health_report():
    """Generate overall dashboard health report"""
    
    print("\n" + "="*60)
    print("🏥 DASHBOARD HEALTH REPORT")
    print("="*60)
    
    # Analyze everything
    components = analyze_layout_components()
    callbacks = analyze_callbacks()
    missing = find_missing_callbacks(components, callbacks)
    endpoints = check_backend_endpoints()
    tabs = analyze_tab_content()
    
    # Generate summary
    total_components = sum(len(items) for items in components.values())
    total_missing = sum(len(items) for items in missing.values())
    callback_coverage = ((total_components - total_missing) / total_components * 100) if total_components > 0 else 0
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Components: {total_components}")
    print(f"   Total Callbacks: {len(callbacks)}")
    print(f"   Missing Callbacks: {total_missing}")
    print(f"   Callback Coverage: {callback_coverage:.1f}%")
    print(f"   Backend Endpoints: {len(endpoints)}")
    print(f"   Tab Callbacks: {len(tabs)}")
    
    # Health status
    if callback_coverage >= 90:
        health_status = "🟢 EXCELLENT"
    elif callback_coverage >= 75:
        health_status = "🟡 GOOD"
    elif callback_coverage >= 50:
        health_status = "🟠 FAIR"
    else:
        health_status = "🔴 POOR"
    
    print(f"   Overall Health: {health_status}")
    
    # Priority fixes
    print(f"\n🔧 PRIORITY FIXES:")
    high_priority = []
    
    if missing.get("Buttons without callbacks"):
        high_priority.extend(missing["Buttons without callbacks"][:5])
    
    if missing.get("Tables without callbacks"):
        high_priority.extend(missing["Tables without callbacks"][:3])
    
    if missing.get("Graphs without callbacks"):
        high_priority.extend(missing["Graphs without callbacks"][:3])
    
    if high_priority:
        for i, item in enumerate(high_priority[:10], 1):
            print(f"   {i}. {item}")
    else:
        print("   ✅ No critical issues found!")
    
    return {
        "components": components,
        "callbacks": callbacks,
        "missing": missing,
        "endpoints": endpoints,
        "tabs": tabs,
        "health_score": callback_coverage
    }

if __name__ == "__main__":
    print("🔍 COMPREHENSIVE DASHBOARD ANALYSIS")
    print("="*60)
    
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run analysis
    report = generate_health_report()
    
    # Save report
    with open("dashboard_analysis_report.json", "w", encoding="utf-8") as f:
        # Convert sets to lists for JSON serialization
        json_report = {}
        for key, value in report.items():
            if isinstance(value, dict):
                json_report[key] = {k: list(v) if isinstance(v, set) else v for k, v in value.items()}
            else:
                json_report[key] = value
        json.dump(json_report, f, indent=2)
    
    print(f"\n📄 Full report saved to: dashboard_analysis_report.json")
    print(f"🌐 Dashboard URL: http://localhost:8050")
