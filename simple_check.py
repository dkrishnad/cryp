#!/usr/bin/env python3
"""
Simple Problem Detector - Write results to file
"""

import re
from collections import Counter

def main():
    results = []
    results.append("=== PROBLEM DETECTION REPORT ===")
    
    try:
        # Check callback duplicates
        with open('dashboard/callbacks.py', 'r') as f:
            content = f.read()
        
        # Find all Output declarations
        output_pattern = r'Output\([\'\"](.*?)[\'\"]'
        outputs = re.findall(output_pattern, content)
        
        # Count occurrences
        output_counts = Counter(outputs)
        duplicates = {k: v for k, v in output_counts.items() if v > 1}
        
        results.append(f"\nCALLBACK ANALYSIS:")
        results.append(f"Total outputs found: {len(outputs)}")
        results.append(f"Unique outputs: {len(output_counts)}")
        results.append(f"Duplicate outputs: {len(duplicates)}")
        
        if duplicates:
            results.append(f"\nDUPLICATE OUTPUTS FOUND:")
            for output_id, count in duplicates.items():
                results.append(f"  '{output_id}': {count} times")
        else:
            results.append("\n✅ No duplicate outputs found")
            
    except Exception as e:
        results.append(f"\nERROR checking callbacks: {e}")
    
    try:
        # Check missing components
        with open('dashboard/callbacks.py', 'r') as f:
            callbacks_content = f.read()
        
        with open('dashboard/layout.py', 'r') as f:
            layout_content = f.read()
        
        # Find all callback outputs
        output_pattern = r'Output\([\'\"](.*?)[\'\"]'
        callback_outputs = set(re.findall(output_pattern, callbacks_content))
        
        # Find all component IDs in layout
        id_pattern = r'id=[\'\"](.*?)[\'\"]'
        layout_ids = set(re.findall(id_pattern, layout_content))
        
        missing_in_layout = callback_outputs - layout_ids
        
        results.append(f"\nCOMPONENT ANALYSIS:")
        results.append(f"Callback outputs: {len(callback_outputs)}")
        results.append(f"Layout components: {len(layout_ids)}")
        results.append(f"Missing in layout: {len(missing_in_layout)}")
        
        if missing_in_layout:
            results.append(f"\nMISSING COMPONENTS:")
            for missing in sorted(missing_in_layout):
                results.append(f"  '{missing}'")
        else:
            results.append(f"\n✅ All components matched")
            
    except Exception as e:
        results.append(f"\nERROR checking components: {e}")
    
    # Write results to file
    with open('problem_report.txt', 'w') as f:
        f.write('\n'.join(results))
    
    print("Problem report saved to: problem_report.txt")
    print("Total issues found:", str(len(duplicates) + len(missing_in_layout) if 'duplicates' in locals() and 'missing_in_layout' in locals() else "Unknown"))

if __name__ == "__main__":
    main()
