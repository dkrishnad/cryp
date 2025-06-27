#!/usr/bin/env python3
"""
Comprehensive Dashboard Feature Analysis
Step-by-step check of all dashboard components and their callbacks
"""
import os
import re

def extract_component_ids():
    """Extract all component IDs from layout.py"""
    print("📋 Step 1: Extracting component IDs from layout.py...")
    
    with open("dashboard/layout.py", "r") as f:
        layout_content = f.read()
    
    # Extract all id= patterns
    id_pattern = r'id=["\']([\w-]+)["\']'
    ids = re.findall(id_pattern, layout_content)
    
    # Categorize IDs
    buttons = [id for id in ids if 'btn' in id]
    outputs = [id for id in ids if any(x in id for x in ['output', 'table', 'display', 'content', 'children'])]
    stores = [id for id in ids if 'store' in id]
    inputs = [id for id in ids if any(x in id for x in ['input', 'dropdown', 'slider', 'checklist'])]
    tabs = [id for id in ids if 'tab' in id]
    
    print(f"✅ Found {len(ids)} total component IDs")
    print(f"  - {len(buttons)} buttons")
    print(f"  - {len(outputs)} output divs")
    print(f"  - {len(stores)} stores")
    print(f"  - {len(inputs)} input components")
    print(f"  - {len(tabs)} tab components")
    
    return {
        'all_ids': ids,
        'buttons': buttons,
        'outputs': outputs,
        'stores': stores,
        'inputs': inputs,
        'tabs': tabs
    }

def check_callback_coverage(component_ids):
    """Check which components have callbacks defined"""
    print("\n📋 Step 2: Checking callback coverage...")
    
    with open("dashboard/callbacks.py", "r") as f:
        callbacks_content = f.read()
    
    # Check for Output patterns
    output_pattern = r'Output\(["\']([^"\']+)["\']'
    callback_outputs = re.findall(output_pattern, callbacks_content)
    
    # Check for Input patterns  
    input_pattern = r'Input\(["\']([^"\']+)["\']'
    callback_inputs = re.findall(input_pattern, callbacks_content)
    
    print(f"✅ Found {len(set(callback_outputs))} unique callback outputs")
    print(f"✅ Found {len(set(callback_inputs))} unique callback inputs")
    
    # Check coverage for each category
    categories = ['buttons', 'outputs', 'inputs', 'tabs']
    
    for category in categories:
        components = component_ids[category]
        covered = []
        missing = []
        
        for component in components:
            if component in callback_outputs or component in callback_inputs:
                covered.append(component)
            else:
                missing.append(component)
        
        print(f"\n{category.upper()} Coverage:")
        print(f"  ✅ Covered: {len(covered)}/{len(components)}")
        if missing:
            print(f"  ❌ Missing callbacks:")
            for item in missing[:5]:  # Show first 5
                print(f"    - {item}")
            if len(missing) > 5:
                print(f"    ... and {len(missing) - 5} more")
    
    return {
        'callback_outputs': callback_outputs,
        'callback_inputs': callback_inputs,
        'coverage_stats': {cat: len([c for c in component_ids[cat] if c in callback_outputs or c in callback_inputs]) 
                          for cat in categories}
    }

def check_duplicate_ids(component_ids):
    """Check for duplicate component IDs"""
    print("\n📋 Step 3: Checking for duplicate IDs...")
    
    all_ids = component_ids['all_ids']
    duplicates = []
    
    for id_name in set(all_ids):
        count = all_ids.count(id_name)
        if count > 1:
            duplicates.append((id_name, count))
    
    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicate IDs:")
        for id_name, count in duplicates:
            print(f"  - {id_name}: appears {count} times")
    else:
        print("✅ No duplicate IDs found")
    
    return duplicates

def check_critical_components():
    """Check for critical dashboard components"""
    print("\n📋 Step 4: Checking critical components...")
    
    critical_components = {
        'live-price': 'Live price display',
        'virtual-balance': 'Virtual balance display', 
        'sidebar-symbol': 'Symbol dropdown',
        'auto-trading-tab-content': 'Auto trading tab',
        'futures-trading-tab-content': 'Futures trading tab',
        'binance-exact-tab-content': 'Binance exact tab',
        'hybrid-learning-tab-content': 'ML/AI tab',
        'email-config-tab-content': 'Email config tab'
    }
    
    # Check if these exist in layout
    with open("dashboard/layout.py", "r") as f:
        layout_content = f.read()
    
    # Check if these have callbacks
    with open("dashboard/callbacks.py", "r") as f:
        callbacks_content = f.read()
    
    missing_in_layout = []
    missing_callbacks = []
    
    for component_id, description in critical_components.items():
        # Check layout
        if f'id="{component_id}"' not in layout_content and f"id='{component_id}'" not in layout_content:
            missing_in_layout.append((component_id, description))
        
        # Check callbacks
        if component_id not in callbacks_content:
            missing_callbacks.append((component_id, description))
    
    print("Critical Components Status:")
    if missing_in_layout:
        print(f"❌ Missing in layout: {len(missing_in_layout)}")
        for comp_id, desc in missing_in_layout:
            print(f"  - {comp_id}: {desc}")
    
    if missing_callbacks:
        print(f"❌ Missing callbacks: {len(missing_callbacks)}")
        for comp_id, desc in missing_callbacks:
            print(f"  - {comp_id}: {desc}")
    
    if not missing_in_layout and not missing_callbacks:
        print("✅ All critical components present and have callbacks")
    
    return {
        'missing_in_layout': missing_in_layout,
        'missing_callbacks': missing_callbacks
    }

def check_button_functionality():
    """Check if all buttons have proper callbacks"""
    print("\n📋 Step 5: Checking button functionality...")
    
    with open("dashboard/callbacks.py", "r") as f:
        callbacks_content = f.read()
    
    # Extract button IDs from layout
    with open("dashboard/layout.py", "r") as f:
        layout_content = f.read()
    
    button_pattern = r'dbc\.Button.*?id=["\']([\w-]+)["\']'
    buttons = re.findall(button_pattern, layout_content, re.DOTALL)
    
    buttons_with_callbacks = []
    buttons_without_callbacks = []
    
    for button in buttons:
        # Check if button has any callback (as Input or State)
        if f'Input(\'{button}\'' in callbacks_content or f'Input("{button}"' in callbacks_content:
            buttons_with_callbacks.append(button)
        else:
            buttons_without_callbacks.append(button)
    
    print(f"Button Functionality Status:")
    print(f"✅ Buttons with callbacks: {len(buttons_with_callbacks)}")
    print(f"❌ Buttons without callbacks: {len(buttons_without_callbacks)}")
    
    if buttons_without_callbacks:
        print("Buttons missing callbacks:")
        for button in buttons_without_callbacks[:10]:  # Show first 10
            print(f"  - {button}")
        if len(buttons_without_callbacks) > 10:
            print(f"  ... and {len(buttons_without_callbacks) - 10} more")
    
    return {
        'working_buttons': buttons_with_callbacks,
        'broken_buttons': buttons_without_callbacks
    }

def check_api_endpoints():
    """Check if API endpoints are properly configured"""
    print("\n📋 Step 6: Checking API endpoint configuration...")
    
    with open("dashboard/callbacks.py", "r") as f:
        callbacks_content = f.read()
    
    # Extract API calls
    api_pattern = r'requests\.\w+\(["\']([^"\']+)["\']'
    api_calls = re.findall(api_pattern, callbacks_content)
    
    # Count unique endpoints
    unique_endpoints = list(set(api_calls))
    
    print(f"✅ Found {len(api_calls)} total API calls")
    print(f"✅ Found {len(unique_endpoints)} unique endpoints")
    
    # Check for common endpoints
    critical_endpoints = [
        'http://localhost:8001/health',
        'http://localhost:8001/price',
        'http://localhost:8001/virtual_balance',
        'http://localhost:8001/auto_trading/status',
        'http://localhost:8001/futures/account'
    ]
    
    missing_endpoints = []
    for endpoint in critical_endpoints:
        if not any(endpoint in call for call in api_calls):
            missing_endpoints.append(endpoint)
    
    if missing_endpoints:
        print(f"❌ Missing critical endpoints: {len(missing_endpoints)}")
        for endpoint in missing_endpoints:
            print(f"  - {endpoint}")
    else:
        print("✅ All critical endpoints found")
    
    return {
        'total_api_calls': len(api_calls),
        'unique_endpoints': unique_endpoints,
        'missing_critical': missing_endpoints
    }

def generate_fix_recommendations(analysis_results):
    """Generate recommendations to fix dashboard issues"""
    print("\n📋 Step 7: Generating fix recommendations...")
    
    recommendations = []
    
    # Check callback coverage
    for category, stats in analysis_results['callback_coverage']['coverage_stats'].items():
        total = len(analysis_results['component_ids'][category])
        if stats < total:
            missing = total - stats
            recommendations.append(f"Add callbacks for {missing} missing {category}")
    
    # Check duplicates
    if analysis_results['duplicates']:
        recommendations.append(f"Fix {len(analysis_results['duplicates'])} duplicate component IDs")
    
    # Check critical components
    critical = analysis_results['critical_components']
    if critical['missing_in_layout']:
        recommendations.append(f"Add {len(critical['missing_in_layout'])} missing critical components to layout")
    if critical['missing_callbacks']:
        recommendations.append(f"Add callbacks for {len(critical['missing_callbacks'])} critical components")
    
    # Check buttons
    broken_buttons = len(analysis_results['button_functionality']['broken_buttons'])
    if broken_buttons > 0:
        recommendations.append(f"Add callbacks for {broken_buttons} non-functional buttons")
    
    # Check API endpoints
    missing_endpoints = len(analysis_results['api_endpoints']['missing_critical'])
    if missing_endpoints > 0:
        recommendations.append(f"Fix {missing_endpoints} missing critical API endpoints")
    
    print("🔧 RECOMMENDED FIXES:")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("✅ No major issues found!")
    
    return recommendations

def main():
    print("🔍 COMPREHENSIVE DASHBOARD FEATURE ANALYSIS")
    print("="*60)
    
    # Run all checks
    component_ids = extract_component_ids()
    callback_coverage = check_callback_coverage(component_ids)
    duplicates = check_duplicate_ids(component_ids)
    critical_components = check_critical_components()
    button_functionality = check_button_functionality()
    api_endpoints = check_api_endpoints()
    
    # Compile results
    analysis_results = {
        'component_ids': component_ids,
        'callback_coverage': callback_coverage,
        'duplicates': duplicates,
        'critical_components': critical_components,
        'button_functionality': button_functionality,
        'api_endpoints': api_endpoints
    }
    
    # Generate recommendations
    recommendations = generate_fix_recommendations(analysis_results)
    
    # Final summary
    print("\n📊 ANALYSIS SUMMARY:")
    print(f"Total Components: {len(component_ids['all_ids'])}")
    print(f"Callback Coverage: {sum(callback_coverage['coverage_stats'].values())}/{sum(len(component_ids[cat]) for cat in ['buttons', 'outputs', 'inputs', 'tabs'])}")
    print(f"Duplicate IDs: {len(duplicates)}")
    print(f"Broken Buttons: {len(button_functionality['broken_buttons'])}")
    print(f"Missing Critical Components: {len(critical_components['missing_in_layout']) + len(critical_components['missing_callbacks'])}")
    
    # Save results
    import json
    from datetime import datetime
    
    with open("dashboard_analysis_report.json", "w") as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'analysis_results': {k: v for k, v in analysis_results.items() if k not in ['component_ids', 'callback_coverage']},
            'recommendations': recommendations,
            'summary': {
                'total_components': len(component_ids['all_ids']),
                'issues_found': len(recommendations)
            }
        }, f, indent=2)
    
    print(f"\n📄 Full analysis saved to: dashboard_analysis_report.json")
    
    if recommendations:
        print(f"\n⚠️  Found {len(recommendations)} issues that need attention")
        return False
    else:
        print("\n🎉 Dashboard analysis complete - no major issues found!")
        return True

if __name__ == "__main__":
    main()
