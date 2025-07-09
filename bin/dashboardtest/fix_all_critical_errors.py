#!/usr/bin/env python3
"""
Fix all duplicate callback outputs identified in the analysis
"""
import re

def fix_duplicate_callbacks():
    """Fix all duplicate callback outputs"""
    
    # Read callbacks.py
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    duplicate_outputs = [
        'backtest-progress',
        'retrain-progress', 
        'sidebar-amount-input',
        'email-config-status'
    ]
    
    print("🔧 Fixing duplicate callback outputs...")
    
    # For each duplicate output, find all instances and merge or remove
    for output_id in duplicate_outputs:
        print(f"\n📍 Fixing: {output_id}")
        
        # Find all callback decorators that use this output
        pattern = r'@app\.callback\s*\(\s*([^)]*Output\s*\(\s*["\']' + re.escape(output_id) + r'["\'][^)]*\)[^)]*)\s*\)'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        print(f"   Found {len(matches)} callbacks using this output")
        
        if len(matches) > 1:
            # Keep only the first callback, comment out the rest
            for i, match in enumerate(matches[1:], 1):
                # Find the entire callback function
                start_pos = match.start()
                
                # Find the function definition that follows
                func_pattern = r'(def\s+[^(]+\([^)]*\):[^@]*?)(?=@app\.callback|\Z)'
                func_match = re.search(func_pattern, content[start_pos:], re.DOTALL)
                
                if func_match:
                    end_pos = start_pos + func_match.end()
                    
                    # Comment out this duplicate callback
                    callback_text = content[start_pos:end_pos]
                    commented_callback = '\n'.join(['# DUPLICATE REMOVED: ' + line for line in callback_text.split('\n')])
                    
                    content = content[:start_pos] + commented_callback + content[end_pos:]
                    print(f"   ✅ Commented out duplicate callback #{i+1}")
    
    # Write the fixed content
    with open('callbacks.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📊 DUPLICATE CALLBACK FIXES COMPLETE!")

def fix_javascript_port():
    """Fix the port reference in realtime_client.js"""
    
    js_file = 'assets/realtime_client.js'
    
    try:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace port 8001 with 8000
        content = content.replace('localhost:8001', 'localhost:8000')
        content = content.replace(':8001/', ':8000/')
        
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed JavaScript port reference (8001 → 8000)")
        
    except FileNotFoundError:
        print(f"⚠️ {js_file} not found, skipping JavaScript fix")

if __name__ == "__main__":
    print("=== FIXING ALL CRITICAL ERRORS ===")
    
    fix_duplicate_callbacks()
    fix_javascript_port()
    
    print("\n🎉 ALL CRITICAL FIXES COMPLETE!")
    print("Now restart both servers:")
    print("1. Backend: python main.py")
    print("2. Dashboard: python app.py")
