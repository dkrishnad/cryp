#!/usr/bin/env python3
"""
QUICK CALLBACK AND API MAPPING ANALYZER
Analyzes all button-to-API mappings without starting servers
"""
import sys
import os
import re
import json
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

def safe_print(msg):
    """Safe printing with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    try:
        print(f"[{timestamp}] {msg}")
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(f"[{timestamp}] {msg.encode('ascii', 'replace').decode('ascii')}")
        sys.stdout.flush()

def analyze_callbacks_file():
    """Analyze the callbacks.py file for button mappings"""
    safe_print("🔍 Analyzing callbacks.py for button-to-API mappings...")
    
    callback_file = os.path.join('dashboardtest', 'callbacks.py')
    if not os.path.exists(callback_file):
        safe_print("❌ callbacks.py not found")
        return {}
    
    button_mappings = {}
    api_calls = {}
    
    try:
        with open(callback_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all @app.callback decorators and their associated functions
        callback_pattern = r'@app\.callback\s*\(\s*Output\([\'"]([^\'"]+)[\'"].*?\)\s*def\s+([^(]+)\([^)]*\):'
        callbacks = re.findall(callback_pattern, content, re.DOTALL)
        
        safe_print(f"  📊 Found {len(callbacks)} callback functions")
        
        # Find all button IDs in Input() calls
        input_pattern = r'Input\([\'"]([^\'"]*btn[^\'"]*)[\'"]'
        button_inputs = re.findall(input_pattern, content)
        
        safe_print(f"  🔘 Found {len(set(button_inputs))} unique button IDs")
        
        # Find all API calls
        api_pattern = r'requests\.(get|post|put|delete)\s*\(\s*[\'"]([^\'"]+)[\'"]'
        api_calls_found = re.findall(api_pattern, content)
        
        safe_print(f"  🌐 Found {len(api_calls_found)} API calls")
        
        # Map buttons to their callback functions
        for output_id, func_name in callbacks:
            # Find the function body
            func_pattern = rf'def\s+{re.escape(func_name)}\([^)]*\):(.*?)(?=\n@|\ndef\s|\nclass\s|\Z)'
            func_match = re.search(func_pattern, content, re.DOTALL)
            
            if func_match:
                func_body = func_match.group(1)
                
                # Find button inputs in this function
                callback_buttons = re.findall(r'Input\([\'"]([^\'"]*btn[^\'"]*)[\'"]', func_body)
                
                # Find API calls in this function
                callback_apis = re.findall(r'requests\.(get|post|put|delete)\s*\(\s*[\'"]([^\'"]+)[\'"]', func_body)
                
                if callback_buttons:
                    for button in callback_buttons:
                        button_mappings[button] = {
                            'output_id': output_id,
                            'function': func_name,
                            'api_calls': [f"{method.upper()} {url}" for method, url in callback_apis]
                        }
        
        return button_mappings
        
    except Exception as e:
        safe_print(f"❌ Error analyzing callbacks: {e}")
        return {}

def analyze_backend_endpoints():
    """Analyze backend files for available endpoints"""
    safe_print("🔍 Analyzing backend endpoints...")
    
    backend_files = [
        'backendtest/app.py',
        'backendtest/main.py',
        'backendtest/trading.py',
        'backendtest/ml.py',
        'backendtest/futures_trading.py',
        'backendtest/auto_generated_endpoints.py'
    ]
    
    all_endpoints = {}
    
    for file_path in backend_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find FastAPI route decorators
            fastapi_pattern = r'@app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]'
            endpoints = re.findall(fastapi_pattern, content)
            
            for method, endpoint in endpoints:
                all_endpoints[endpoint] = {
                    'method': method.upper(),
                    'file': file_path
                }
            
            safe_print(f"  📄 {file_path}: {len(endpoints)} endpoints")
            
        except Exception as e:
            safe_print(f"  ❌ Error reading {file_path}: {e}")
    
    safe_print(f"  📊 Total backend endpoints: {len(all_endpoints)}")
    return all_endpoints

def find_missing_connections():
    """Find buttons without proper API connections"""
    safe_print("🔍 Finding missing button-to-API connections...")
    
    button_mappings = analyze_callbacks_file()
    backend_endpoints = analyze_backend_endpoints()
    
    missing_connections = []
    working_connections = []
    frontend_only = []
    
    for button_id, mapping in button_mappings.items():
        api_calls = mapping.get('api_calls', [])
        
        if not api_calls:
            frontend_only.append({
                'button_id': button_id,
                'output_id': mapping['output_id'],
                'function': mapping['function'],
                'issue': 'No API calls found'
            })
        else:
            has_working_endpoint = False
            for api_call in api_calls:
                method, url = api_call.split(' ', 1)
                # Extract endpoint from URL
                endpoint = url.replace('http://localhost:5000', '').replace('http://localhost:8000', '')
                
                if endpoint in backend_endpoints:
                    backend_method = backend_endpoints[endpoint]['method']
                    if method == backend_method:
                        has_working_endpoint = True
                        working_connections.append({
                            'button_id': button_id,
                            'endpoint': endpoint,
                            'method': method
                        })
                        break
            
            if not has_working_endpoint:
                missing_connections.append({
                    'button_id': button_id,
                    'output_id': mapping['output_id'],
                    'function': mapping['function'],
                    'api_calls': api_calls,
                    'issue': 'API endpoint not found in backend'
                })
    
    return {
        'working_connections': working_connections,
        'missing_connections': missing_connections,
        'frontend_only': frontend_only
    }

def generate_summary_report():
    """Generate a comprehensive summary report"""
    safe_print("📊 Generating comprehensive summary report...")
    
    connection_analysis = find_missing_connections()
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'working_connections': len(connection_analysis['working_connections']),
            'missing_connections': len(connection_analysis['missing_connections']),
            'frontend_only_buttons': len(connection_analysis['frontend_only'])
        },
        'details': connection_analysis
    }
    
    # Display summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 BUTTON-TO-API CONNECTION ANALYSIS")
    safe_print("=" * 60)
    
    summary = report['summary']
    total_buttons = sum(summary.values())
    
    safe_print(f"✅ Working Connections: {summary['working_connections']}")
    safe_print(f"❌ Missing Connections: {summary['missing_connections']}")
    safe_print(f"⚠️ Frontend-Only Buttons: {summary['frontend_only_buttons']}")
    safe_print(f"📊 Total Buttons Analyzed: {total_buttons}")
    
    if summary['working_connections'] > 0:
        safe_print("\n✅ WORKING BUTTON-TO-API CONNECTIONS:")
        for conn in connection_analysis['working_connections'][:10]:  # Show first 10
            safe_print(f"  🔘 {conn['button_id']} → {conn['method']} {conn['endpoint']}")
        
        if len(connection_analysis['working_connections']) > 10:
            safe_print(f"  ... and {len(connection_analysis['working_connections']) - 10} more")
    
    if summary['missing_connections'] > 0:
        safe_print("\n❌ MISSING BUTTON-TO-API CONNECTIONS:")
        for conn in connection_analysis['missing_connections'][:10]:  # Show first 10
            safe_print(f"  🔘 {conn['button_id']} → {conn['api_calls']}")
            safe_print(f"     Issue: {conn['issue']}")
        
        if len(connection_analysis['missing_connections']) > 10:
            safe_print(f"  ... and {len(connection_analysis['missing_connections']) - 10} more")
    
    if summary['frontend_only_buttons'] > 0:
        safe_print("\n⚠️ FRONTEND-ONLY BUTTONS (no backend calls):")
        for btn in connection_analysis['frontend_only'][:10]:  # Show first 10
            safe_print(f"  🔘 {btn['button_id']} → {btn['function']}")
        
        if len(connection_analysis['frontend_only']) > 10:
            safe_print(f"  ... and {len(connection_analysis['frontend_only']) - 10} more")
    
    # Calculate health score
    if total_buttons > 0:
        health_score = (summary['working_connections'] / total_buttons) * 100
        safe_print(f"\n🎯 BUTTON-TO-API HEALTH SCORE: {health_score:.1f}%")
        
        if health_score >= 80:
            safe_print("🎉 EXCELLENT: Most buttons are properly connected!")
        elif health_score >= 60:
            safe_print("✅ GOOD: Good button connectivity with room for improvement")
        elif health_score >= 40:
            safe_print("⚠️ FAIR: Many buttons need API connections")
        else:
            safe_print("❌ POOR: Critical connectivity issues")
    
    # Save report
    report_file = f"button_api_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        safe_print(f"\n📄 Detailed report saved to: {report_file}")
    except Exception as e:
        safe_print(f"⚠️ Could not save report: {e}")
    
    return report

if __name__ == "__main__":
    safe_print("🚀 STARTING QUICK CALLBACK AND API ANALYSIS")
    safe_print("=" * 60)
    
    try:
        report = generate_summary_report()
        safe_print("\n✅ Analysis complete!")
        
    except Exception as e:
        safe_print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
