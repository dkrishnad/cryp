#!/usr/bin/env python3
"""
Find callbacks that return dictionaries instead of Dash components
"""
import re
import os
import sys

def find_dict_returns_in_callbacks():
    """Find callbacks that return dictionaries where components are expected"""
    
    callback_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/futures_callbacks.py", 
        "dashboardtest/binance_exact_callbacks.py"
    ]
    
    issues = []
    
    for file_path in callback_files:
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            continue
            
        print(f"🔍 Analyzing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all callback definitions
            callback_pattern = r'@(?:app\.callback|dash\.callback)\s*\(\s*([^)]+)\s*\)\s*def\s+([^(]+)\([^)]*\):'
            callbacks = re.findall(callback_pattern, content, re.MULTILINE | re.DOTALL)
            
            for callback_def, func_name in callbacks:
                # Extract the function body
                func_pattern = rf'def\s+{re.escape(func_name)}\([^)]*\):(.*?)(?=\n@|\ndef\s|\nclass\s|\n#|\Z)'
                func_match = re.search(func_pattern, content, re.DOTALL)
                
                if func_match:
                    func_body = func_match.group(1)
                    
                    # Check for return statements that return plain dictionaries
                    return_patterns = [
                        r'return\s+\{[^}]*\}(?:\s*,\s*\{[^}]*\})*\s*$',  # Pure dict returns
                        r'return\s+\{[^}]*:"[^"]*"[^}]*\}(?:\s*,\s*\{[^}]*\})*\s*$',  # Dict with strings
                    ]
                    
                    for pattern in return_patterns:
                        returns = re.findall(pattern, func_body, re.MULTILINE)
                        if returns:
                            # Check if this is a style/property return vs component return
                            output_match = re.search(r'Output\s*\(\s*["\']([^"\']+)["\']', callback_def)
                            if output_match:
                                output_id = output_match.group(1)
                                # Check if it's returning to 'children' property
                                if 'children' in callback_def:
                                    issues.append({
                                        'file': file_path,
                                        'function': func_name,
                                        'output_id': output_id,
                                        'returns': returns,
                                        'callback_def': callback_def.strip()
                                    })
                                    print(f"❌ ISSUE: {func_name} in {file_path}")
                                    print(f"   Returns dict to children: {returns}")
                                    print(f"   Output ID: {output_id}")
                                    print()
                                
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            
    return issues

def check_layout_functions():
    """Check if layout functions return dictionaries"""
    
    layout_files = [
        "dashboardtest/layout.py",
        "dashboardtest/auto_trading_layout.py",
        "dashboardtest/futures_trading_layout.py",
        "dashboardtest/binance_exact_layout.py",
        "dashboardtest/email_config_layout.py",
        "dashboardtest/hybrid_learning_layout.py"
    ]
    
    issues = []
    
    for file_path in layout_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"🔍 Checking layout functions in: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for function definitions that might return layouts
            func_pattern = r'def\s+([^(]+)\([^)]*\):(.*?)(?=\ndef\s|\nclass\s|\n#|\Z)'
            functions = re.findall(func_pattern, content, re.DOTALL)
            
            for func_name, func_body in functions:
                # Check if function returns a dictionary
                if re.search(r'return\s+\{[^}]*\}', func_body):
                    print(f"⚠️  {func_name} returns dictionary in {file_path}")
                    issues.append({
                        'file': file_path,
                        'function': func_name,
                        'type': 'layout_function'
                    })
                    
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
            
    return issues

if __name__ == "__main__":
    print("🔍 Finding callbacks that return dictionaries instead of Dash components...")
    print("=" * 70)
    
    callback_issues = find_dict_returns_in_callbacks()
    layout_issues = check_layout_functions()
    
    print("\n" + "=" * 70)
    print("📋 SUMMARY:")
    print(f"Callback issues found: {len(callback_issues)}")
    print(f"Layout issues found: {len(layout_issues)}")
    
    if callback_issues:
        print("\n❌ CALLBACK ISSUES:")
        for issue in callback_issues:
            print(f"  - {issue['function']} in {issue['file']}")
            print(f"    Output: {issue['output_id']}")
            
    if layout_issues:
        print("\n❌ LAYOUT ISSUES:")
        for issue in layout_issues:
            print(f"  - {issue['function']} in {issue['file']}")
            
    if not callback_issues and not layout_issues:
        print("✅ No obvious dict return issues found")
        print("The issue might be in the layout structure or component creation")
