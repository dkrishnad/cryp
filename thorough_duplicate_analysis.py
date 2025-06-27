import re

# Read the file
with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find all callback decorators and their outputs
callbacks = []
for i, line in enumerate(lines):
    if '@app.callback' in line:
        # Collect all lines for this callback until the function definition
        callback_lines = []
        j = i
        while j < len(lines) and not lines[j].strip().startswith('def '):
            callback_lines.append(lines[j])
            j += 1
        if j < len(lines):
            callback_lines.append(lines[j])  # Add the function definition line
        
        # Extract outputs from the callback
        callback_text = '\n'.join(callback_lines)
        outputs = []
        
        # Find Output declarations
        output_matches = re.findall(r"Output\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]", callback_text)
        for output_match in output_matches:
            outputs.append(f"{output_match[0]}.{output_match[1]}")
        
        # Get function name
        func_match = re.search(r'def\s+(\w+)\s*\(', callback_text)
        func_name = func_match.group(1) if func_match else "unknown"
        
        # Check for allow_duplicate
        has_allow_duplicate = 'allow_duplicate=True' in callback_text
        
        callbacks.append({
            'line': i + 1,
            'func_name': func_name,
            'outputs': outputs,
            'allow_duplicate': has_allow_duplicate,
            'callback_text': callback_text
        })

# Group by output to find duplicates
output_groups = {}
for callback in callbacks:
    for output in callback['outputs']:
        if output not in output_groups:
            output_groups[output] = []
        output_groups[output].append(callback)

# Report duplicates
print("=" * 80)
print("DUPLICATE CALLBACK OUTPUT ANALYSIS")
print("=" * 80)

duplicates_found = 0
for output, cbs in output_groups.items():
    if len(cbs) > 1:
        duplicates_found += 1
        print(f"\n{duplicates_found}. DUPLICATE OUTPUT: {output}")
        print(f"   Found in {len(cbs)} callbacks:")
        
        for i, cb in enumerate(cbs):
            print(f"   Callback {i+1}:")
            print(f"     Line: {cb['line']}")
            print(f"     Function: {cb['func_name']}()")
            print(f"     Allow Duplicate: {cb['allow_duplicate']}")
            print(f"     All Outputs: {cb['outputs']}")
            
            # Show the first few lines of the callback for context
            first_lines = cb['callback_text'].split('\n')[:3]
            for line in first_lines:
                if line.strip():
                    print(f"     Code: {line.strip()}")
            print()

print(f"\nSUMMARY:")
print(f"Total callbacks found: {len(callbacks)}")
print(f"Duplicate outputs found: {duplicates_found}")
print(f"Outputs with duplicates: {len([k for k, v in output_groups.items() if len(v) > 1])}")

# Check for functions with same name
print("\n" + "=" * 80)
print("DUPLICATE FUNCTION NAME ANALYSIS")
print("=" * 80)

func_groups = {}
for callback in callbacks:
    func_name = callback['func_name']
    if func_name not in func_groups:
        func_groups[func_name] = []
    func_groups[func_name].append(callback)

func_duplicates = 0
for func_name, cbs in func_groups.items():
    if len(cbs) > 1:
        func_duplicates += 1
        print(f"\n{func_duplicates}. DUPLICATE FUNCTION: {func_name}()")
        print(f"   Found {len(cbs)} times:")
        for i, cb in enumerate(cbs):
            print(f"     {i+1}. Line {cb['line']} - Outputs: {cb['outputs']}")

print(f"\nFunction duplicates found: {func_duplicates}")
