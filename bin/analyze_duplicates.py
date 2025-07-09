import re

# Read the file
with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Extract function names from both sections
original_functions = []
duplicate_functions = []

# Section 1: lines 1-1649 (0-indexed: 0-1648)
for i in range(0, min(1649, len(lines))):
    if lines[i].strip().startswith('def '):
        func_name = lines[i].strip().split('def ')[1].split('(')[0]
        original_functions.append((func_name, i+1))

# Section 2: lines 1650-3382 (0-indexed: 1649-3381)
for i in range(1649, min(3382, len(lines))):
    if lines[i].strip().startswith('def '):
        func_name = lines[i].strip().split('def ')[1].split('(')[0]
        duplicate_functions.append((func_name, i+1))

print('ORIGINAL SECTION FUNCTIONS (lines 1-1649):')
for func, line in original_functions:
    print(f'  {func} (line {line})')

print('\nDUPLICATE SECTION FUNCTIONS (lines 1650-3382):')
for func, line in duplicate_functions:
    print(f'  {func} (line {line})')

print('\nFUNCTIONS ONLY IN DUPLICATE SECTION:')
orig_names = set(f[0] for f in original_functions)
dup_names = set(f[0] for f in duplicate_functions)
only_in_dup = dup_names - orig_names
for name in only_in_dup:
    line = [f[1] for f in duplicate_functions if f[0] == name][0]
    print(f'  {name} (line {line}) - UNIQUE TO DUPLICATE SECTION')

print('\nFUNCTIONS ONLY IN ORIGINAL SECTION:')
only_in_orig = orig_names - dup_names
for name in only_in_orig:
    line = [f[1] for f in original_functions if f[0] == name][0]
    print(f'  {name} (line {line}) - UNIQUE TO ORIGINAL SECTION')

print(f'\nSUMMARY:')
print(f'Original section: {len(original_functions)} functions')
print(f'Duplicate section: {len(duplicate_functions)} functions')
print(f'Functions unique to duplicate section: {len(only_in_dup)}')
print(f'Functions unique to original section: {len(only_in_orig)}')
