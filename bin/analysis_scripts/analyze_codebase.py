#!/usr/bin/env python3
"""
Comprehensive Codebase Analysis Script
Analyzes all files for completeness, issues, and synchronization
"""

import os
import json
import re
from datetime import datetime

def analyze_codebase():
    print('=== COMPREHENSIVE CODEBASE ANALYSIS ===')
    print(f'Analysis Date: {datetime.now().isoformat()}')
    print()
    
    analysis = {
        'backend_files': [],
        'dashboard_files': [],
        'bin_files': [],
        'issues': [],
        'port_usage': {},
        'missing_endpoints': [],
        'skeleton_functions': [],
        'summary': {}
    }
    
    # Analyze backend files
    print('🔍 ANALYZING BACKEND FILES...')
    if os.path.exists('backendtest'):
        for filename in os.listdir('backendtest'):
            if filename.endswith('.py'):
                filepath = os.path.join('backendtest', filename)
                try:
                    size = os.path.getsize(filepath)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    analysis['backend_files'].append({
                        'name': filename,
                        'size': size,
                        'lines': len(content.split('\n')),
                        'endpoints': len(re.findall(r'@app\.(get|post|put|delete)', content)),
                        'functions': len(re.findall(r'def\s+\w+', content)),
                        'imports': len(re.findall(r'^import\s+|^from\s+', content, re.MULTILINE))
                    })
                except Exception as e:
                    analysis['issues'].append(f"Error reading {filepath}: {e}")
    
    # Analyze dashboard files
    print('🔍 ANALYZING DASHBOARD FILES...')
    if os.path.exists('dashboardtest'):
        for filename in os.listdir('dashboardtest'):
            if filename.endswith('.py'):
                filepath = os.path.join('dashboardtest', filename)
                try:
                    size = os.path.getsize(filepath)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for port references
                    ports = re.findall(r'localhost:(\d+)', content)
                    for port in ports:
                        if port not in analysis['port_usage']:
                            analysis['port_usage'][port] = []
                        analysis['port_usage'][port].append(filename)
                    
                    # Check for skeleton functions
                    if 'pass' in content or 'TODO' in content or 'placeholder' in content:
                        analysis['skeleton_functions'].append(filename)
                    
                    analysis['dashboard_files'].append({
                        'name': filename,
                        'size': size,
                        'lines': len(content.split('\n')),
                        'callbacks': len(re.findall(r'@app\.callback', content)),
                        'functions': len(re.findall(r'def\s+\w+', content)),
                        'ports_used': list(set(ports))
                    })
                except Exception as e:
                    analysis['issues'].append(f"Error reading {filepath}: {e}")
    
    # Check bin folder
    print('🔍 ANALYZING BIN FILES...')
    if os.path.exists('bin'):
        bin_count = 0
        for root, dirs, files in os.walk('bin'):
            bin_count += len([f for f in files if f.endswith(('.py', '.md', '.json'))])
        analysis['bin_files'] = {'count': bin_count}
    
    # Generate summary
    backend_main = next((f for f in analysis['backend_files'] if f['name'] == 'main.py'), None)
    dashboard_callbacks = next((f for f in analysis['dashboard_files'] if f['name'] == 'callbacks.py'), None)
    
    analysis['summary'] = {
        'backend_endpoints': backend_main['endpoints'] if backend_main else 0,
        'dashboard_callbacks': dashboard_callbacks['callbacks'] if dashboard_callbacks else 0,
        'port_synchronization': 'Good' if '8000' in analysis['port_usage'] and '8050' in analysis['port_usage'] else 'Issues detected',
        'skeleton_functions_found': len(analysis['skeleton_functions']),
        'files_in_bin': analysis['bin_files']['count'] if 'count' in analysis['bin_files'] else 0,
        'total_issues': len(analysis['issues'])
    }
    
    return analysis

def check_specific_issues():
    print('\n🔍 CHECKING SPECIFIC ISSUES...')
    
    issues = []
    
    # Check main.py completeness
    main_path = 'backendtest/main.py'
    if os.path.exists(main_path):
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for incomplete functions
        incomplete_patterns = [
            r'def\s+\w+.*:\s*try:\s*$',  # Functions with just try:
            r'def\s+\w+.*:\s*pass\s*$',   # Functions with just pass
            r'# TODO',                     # TODO comments
            r'raise NotImplementedError'   # Not implemented
        ]
        
        for pattern in incomplete_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                issues.append(f"main.py has {len(matches)} incomplete functions matching '{pattern}'")
    
    # Check callbacks.py completeness
    callbacks_path = 'dashboardtest/callbacks.py'
    if os.path.exists(callbacks_path):
        with open(callbacks_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for skeleton callbacks
        if 'fi_ok = True' in content:
            issues.append("callbacks.py has hardcoded skeleton implementations")
        
        # Check port consistency
        ports = re.findall(r'localhost:(\d+)', content)
        if '8001' in ports:
            issues.append("callbacks.py still references wrong port 8001")
    
    return issues

if __name__ == "__main__":
    try:
        analysis = analyze_codebase()
        specific_issues = check_specific_issues()
        
        print('\n📊 ANALYSIS RESULTS:')
        print(f"Backend Endpoints: {analysis['summary']['backend_endpoints']}")
        print(f"Dashboard Callbacks: {analysis['summary']['dashboard_callbacks']}")
        print(f"Port Synchronization: {analysis['summary']['port_synchronization']}")
        print(f"Skeleton Functions: {analysis['summary']['skeleton_functions_found']}")
        print(f"Files in Bin: {analysis['summary']['files_in_bin']}")
        print(f"Total Issues: {analysis['summary']['total_issues']}")
        
        print('\n🔧 PORT USAGE:')
        for port, files in analysis['port_usage'].items():
            print(f"Port {port}: {', '.join(files)}")
        
        if specific_issues:
            print('\n⚠️  SPECIFIC ISSUES FOUND:')
            for issue in specific_issues:
                print(f"- {issue}")
        
        if analysis['issues']:
            print('\n❌ GENERAL ISSUES:')
            for issue in analysis['issues']:
                print(f"- {issue}")
        
        # Save analysis to file
        with open('codebase_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print('\n✅ Analysis complete! Results saved to codebase_analysis.json')
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
