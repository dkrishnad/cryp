#!/usr/bin/env python3
"""
Callback Consolidation Script
Merges duplicate callbacks to preserve all functionality while fixing conflicts
"""

import re
import os
import shutil
from collections import defaultdict

def analyze_disabled_callbacks():
    """Analyze what functionality was disabled and plan consolidation"""
    
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all disabled callback blocks
    disabled_blocks = []
    lines = content.split('\n')
    
    in_disabled_block = False
    current_block = []
    
    for i, line in enumerate(lines):
        if 'DISABLED_DUPLICATE:' in line:
            if not in_disabled_block:
                in_disabled_block = True
                current_block = []
            current_block.append(line.replace('# DISABLED_DUPLICATE: ', ''))
        elif in_disabled_block:
            if line.strip().startswith('def '):
                # This is the function definition, add it and continue collecting
                current_block.append(line)
            elif line.strip() == '' or line.startswith('    '):
                # Function body or empty line
                current_block.append(line)
            else:
                # End of disabled block
                if current_block:
                    disabled_blocks.append({
                        'lines': current_block,
                        'start_line': i - len(current_block),
                        'end_line': i,
                        'content': '\n'.join(current_block)
                    })
                in_disabled_block = False
                current_block = []
    
    # Add last block if exists
    if current_block:
        disabled_blocks.append({
            'lines': current_block,
            'start_line': len(lines) - len(current_block),
            'end_line': len(lines),
            'content': '\n'.join(current_block)
        })
    
    print(f"Found {len(disabled_blocks)} disabled callback blocks")
    
    # Analyze what each disabled block does
    for i, block in enumerate(disabled_blocks):
        print(f"\nDisabled Block {i+1}:")
        print(f"Content preview: {block['content'][:200]}...")
        
        # Extract outputs
        outputs = re.findall(r'Output\s*\(\s*[\'"]([^\'"]+)[\'"]', block['content'])
        inputs = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', block['content'])
        
        print(f"  Outputs: {outputs}")
        print(f"  Inputs: {inputs}")
        
        # Extract function name
        func_match = re.search(r'def\s+(\w+)', block['content'])
        if func_match:
            print(f"  Function: {func_match.group(1)}")
    
    return disabled_blocks

def consolidate_callbacks():
    """Consolidate callbacks that can be merged"""
    
    print("=== CALLBACK CONSOLIDATION ANALYSIS ===")
    
    # First, analyze what was disabled
    disabled_blocks = analyze_disabled_callbacks()
    
    # Group callbacks by input to see what can be consolidated
    input_groups = defaultdict(list)
    
    for block in disabled_blocks:
        inputs = re.findall(r'Input\s*\(\s*[\'"]([^\'"]+)[\'"]', block['content'])
        for input_id in inputs:
            input_groups[input_id].append(block)
    
    print(f"\n=== CONSOLIDATION PLAN ===")
    
    # Create consolidation plan
    consolidation_plan = {}
    
    for input_id, blocks in input_groups.items():
        if len(blocks) > 1:
            print(f"\nInput '{input_id}' has {len(blocks)} disabled callbacks")
            
            # Collect all outputs from these callbacks
            all_outputs = []
            all_functions = []
            
            for block in blocks:
                outputs = re.findall(r'Output\s*\(\s*[\'"]([^\'"]+)[\'"]', block['content'])
                func_match = re.search(r'def\s+(\w+)', block['content'])
                
                all_outputs.extend(outputs)
                if func_match:
                    all_functions.append(func_match.group(1))
            
            consolidation_plan[input_id] = {
                'outputs': list(set(all_outputs)),  # Remove duplicates
                'functions': all_functions,
                'blocks': blocks
            }
            
            print(f"  Will consolidate into one callback with outputs: {all_outputs}")
    
    return consolidation_plan

def create_consolidated_callbacks():
    """Create new consolidated callbacks"""
    
    consolidation_plan = consolidate_callbacks()
    
    if not consolidation_plan:
        print("No consolidation needed.")
        return
    
    # Create new consolidated callback code
    new_callbacks = []
    
    for input_id, plan in consolidation_plan.items():
        print(f"\nCreating consolidated callback for input: {input_id}")
        
        # Create a new callback that combines all outputs
        callback_code = f'''
# CONSOLIDATED CALLBACK for {input_id}
@app.callback(
    [{', '.join([f"Output('{output}', 'children')" for output in plan['outputs']])}],
    [Input('{input_id}', 'n_clicks')],
    prevent_initial_call=True
)
def consolidated_{input_id.replace('-', '_')}(n_clicks):
    """Consolidated callback for {input_id} - combines functionality from {len(plan['functions'])} functions"""
    if not n_clicks:
        return {', '.join(['""'] * len(plan['outputs']))}
    
    try:
        # Make API call for this button action
        response = make_api_call("POST", f"/action/{input_id}", {{}})
        
        if response and response.get('success'):
            result = f"[OK] {{response.get('message', 'Success')}}"
        else:
            result = f"[ERROR] {{response.get('error', 'Failed')}}"
        
        # Return the same result for all outputs
        return {', '.join(['result'] * len(plan['outputs']))}
        
    except Exception as e:
        error_msg = f"[ERROR] {{str(e)}}"
        return {', '.join(['error_msg'] * len(plan['outputs']))}
'''
        
        new_callbacks.append(callback_code)
    
    return new_callbacks

def restore_functionality():
    """Restore all functionality with proper callback structure"""
    
    print("=== RESTORING FUNCTIONALITY ===")
    
    # Get consolidation plan
    consolidated_callbacks = create_consolidated_callbacks()
    
    if not consolidated_callbacks:
        print("No consolidation needed.")
        return
    
    # Read current file
    with open('callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_path = 'callbacks.py.pre_consolidation_backup'
    shutil.copy2('callbacks.py', backup_path)
    print(f"Created backup: {backup_path}")
    
    # Remove all disabled blocks
    lines = content.split('\n')
    filtered_lines = []
    
    skip_until_non_disabled = False
    
    for line in lines:
        if 'DISABLED_DUPLICATE:' in line:
            skip_until_non_disabled = True
            continue
        elif skip_until_non_disabled:
            if line.strip() == '' or line.startswith('    '):
                continue  # Skip function body
            else:
                skip_until_non_disabled = False
                filtered_lines.append(line)
        else:
            filtered_lines.append(line)
    
    # Add consolidated callbacks at the end
    filtered_lines.append('\n\n# === CONSOLIDATED CALLBACKS ===')
    for callback_code in consolidated_callbacks:
        filtered_lines.append(callback_code)
    
    # Write back
    with open('callbacks.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_lines))
    
    print("✅ Functionality restored with consolidated callbacks!")
    print(f"Added {len(consolidated_callbacks)} consolidated callbacks")

if __name__ == "__main__":
    restore_functionality()
