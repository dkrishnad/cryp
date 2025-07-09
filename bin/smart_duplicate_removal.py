#!/usr/bin/env python3
"""
Smart duplicate removal - only remove TRUE duplicates, preserve advanced features
"""

import re
from collections import defaultdict

def identify_true_duplicates():
    """Identify only TRUE duplicates (same function name + same outputs)"""
    
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.splitlines()
    
    # Extract all callbacks with their details
    callbacks = []
    callback_pattern = r'@app\.callback\((.*?)\)'
    output_pattern = r'Output\([\'"]([^\'"]+)[\'"],\s*[\'"]([^\'"]+)[\'"](?:,\s*allow_duplicate=True)?\)'
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('@app.callback'):
            # Found a callback, collect the full decorator
            callback_start = i
            decorator_lines = [line]
            i += 1
            
            # Continue collecting decorator lines until we hit the function definition
            while i < len(lines) and not lines[i].strip().startswith('def '):
                if lines[i].strip():  # Skip empty lines
                    decorator_lines.append(lines[i].strip())
                i += 1
            
            # Get the function name
            if i < len(lines):
                func_line = lines[i].strip()
                func_match = re.match(r'def\s+(\w+)\s*\(', func_line)
                func_name = func_match.group(1) if func_match else "unknown"
                
                # Get function end line
                func_end = i
                indent_level = len(lines[i]) - len(lines[i].lstrip())
                j = i + 1
                while j < len(lines):
                    current_line = lines[j]
                    if current_line.strip() == '':
                        j += 1
                        continue
                    current_indent = len(current_line) - len(current_line.lstrip())
                    if current_indent <= indent_level and current_line.strip():
                        func_end = j - 1
                        break
                    j += 1
                else:
                    func_end = len(lines) - 1
            else:
                func_name = "unknown"
                func_end = i
            
            # Join all decorator lines and extract outputs
            full_decorator = ' '.join(decorator_lines)
            outputs = re.findall(output_pattern, full_decorator)
            
            callback_info = {
                'line_start': callback_start + 1,  # 1-indexed
                'line_end': func_end + 1,
                'function_name': func_name,
                'outputs': outputs,
                'full_decorator': full_decorator,
                'has_allow_duplicate': 'allow_duplicate=True' in full_decorator
            }
            callbacks.append(callback_info)
        
        i += 1
    
    print(f"Found {len(callbacks)} total callbacks")
    
    # Group by function name and outputs to find TRUE duplicates
    function_groups = defaultdict(list)
    
    for callback in callbacks:
        # Create a key based on function name AND outputs
        outputs_key = tuple(sorted([f"{out[0]}.{out[1]}" for out in callback['outputs']]))
        key = (callback['function_name'], outputs_key)
        function_groups[key].append(callback)
    
    # Find TRUE duplicates (same function name + same outputs)
    true_duplicates = []
    for key, group in function_groups.items():
        if len(group) > 1:
            func_name, outputs = key
            print(f"\nTRUE DUPLICATE: {func_name}() with outputs {list(outputs)}")
            
            # Keep the first occurrence (usually original), mark others for removal
            original = group[0]
            duplicates = group[1:]
            
            for dup in duplicates:
                print(f"  REMOVE: Lines {dup['line_start']}-{dup['line_end']} (has allow_duplicate: {dup['has_allow_duplicate']})")
                true_duplicates.append(dup)
            
            print(f"  KEEP: Lines {original['line_start']}-{original['line_end']} (original)")
    
    print(f"\nSUMMARY:")
    print(f"Total callbacks: {len(callbacks)}")
    print(f"True duplicates to remove: {len(true_duplicates)}")
    print(f"Original callbacks to keep: {len(callbacks) - len(true_duplicates)}")
    
    return callbacks, true_duplicates

def create_clean_file():
    """Create clean file with only true duplicates removed"""
    callbacks, true_duplicates = identify_true_duplicates()
    
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Sort duplicates by line number in reverse order (remove from bottom up)
    true_duplicates.sort(key=lambda x: x['line_start'], reverse=True)
    
    # Remove true duplicates
    for dup in true_duplicates:
        start_line = dup['line_start'] - 1  # Convert to 0-indexed
        end_line = dup['line_end'] - 1
        
        print(f"Removing {dup['function_name']}() from lines {start_line+1}-{end_line+1}")
        
        # Remove the lines
        del lines[start_line:end_line+1]
    
    # Write clean file
    with open(r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks_truly_clean.py", 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nClean file created: callbacks_truly_clean.py")
    print(f"Original: {len(lines) + sum(dup['line_end'] - dup['line_start'] + 1 for dup in true_duplicates)} lines")
    print(f"Clean: {len(lines)} lines")
    print(f"Removed: {sum(dup['line_end'] - dup['line_start'] + 1 for dup in true_duplicates)} lines")

if __name__ == "__main__":
    create_clean_file()
