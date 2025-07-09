#!/usr/bin/env python3
"""
Fix duplicate callback outputs in the dashboard
"""
import re
import sys
import os

def find_duplicate_outputs():
    """Find duplicate callback outputs in callbacks.py"""
    callbacks_file = "callbacks.py"
    
    if not os.path.exists(callbacks_file):
        print(f"❌ {callbacks_file} not found")
        return []
    
    print("🔍 Analyzing callbacks for duplicate outputs...")
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all @app.callback decorators and their outputs
    callback_pattern = r'@app\.callback\s*\(\s*(?:Output\([^)]+\)[^@]*?)+'
    callbacks = re.findall(callback_pattern, content, re.DOTALL)
    
    # Extract output IDs
    output_pattern = r'Output\s*\(\s*["\']([^"\']+)["\']'
    
    output_counts = {}
    duplicate_outputs = []
    
    for i, callback in enumerate(callbacks):
        outputs = re.findall(output_pattern, callback)
        for output_id in outputs:
            if output_id in output_counts:
                output_counts[output_id] += 1
                if output_id not in duplicate_outputs:
                    duplicate_outputs.append(output_id)
            else:
                output_counts[output_id] = 1
    
    print(f"\n📊 Analysis Results:")
    print(f"Total callbacks found: {len(callbacks)}")
    print(f"Total unique outputs: {len(output_counts)}")
    print(f"Duplicate outputs: {len(duplicate_outputs)}")
    
    if duplicate_outputs:
        print(f"\n❌ DUPLICATE OUTPUT IDs FOUND:")
        for output_id in duplicate_outputs:
            print(f"  - {output_id} (used {output_counts[output_id]} times)")
    
    return duplicate_outputs

def get_line_numbers_for_outputs(output_ids):
    """Get line numbers where duplicate outputs are defined"""
    callbacks_file = "callbacks.py"
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    results = {}
    for output_id in output_ids:
        results[output_id] = []
        for line_num, line in enumerate(lines, 1):
            if f'Output("{output_id}"' in line or f"Output('{output_id}'" in line:
                results[output_id].append(line_num)
    
    return results

if __name__ == "__main__":
    print("=== DUPLICATE CALLBACK OUTPUT ANALYZER ===")
    
    duplicate_outputs = find_duplicate_outputs()
    
    if duplicate_outputs:
        print(f"\n🔧 GETTING LINE NUMBERS...")
        line_numbers = get_line_numbers_for_outputs(duplicate_outputs)
        
        print(f"\n📍 LOCATIONS OF DUPLICATE OUTPUTS:")
        for output_id in duplicate_outputs:
            lines = line_numbers.get(output_id, [])
            print(f"\n{output_id}:")
            for line_num in lines:
                print(f"  Line {line_num}")
        
        print(f"\n⚠️ ACTION NEEDED:")
        print(f"1. Review the callbacks at the line numbers above")
        print(f"2. Merge or remove duplicate callbacks")
        print(f"3. Ensure each output ID is only used once")
        
    else:
        print(f"\n✅ NO DUPLICATE OUTPUTS FOUND!")
        print(f"The skeleton issue might be caused by other problems.")
