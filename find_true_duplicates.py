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

# Find functions that appear in both sections (true duplicates)
orig_names = set(f[0] for f in original_functions)
dup_names = set(f[0] for f in duplicate_functions)
true_duplicates = orig_names & dup_names

print('TRUE DUPLICATES (appear in both sections):')
for name in true_duplicates:
    orig_line = [f[1] for f in original_functions if f[0] == name][0]
    dup_line = [f[1] for f in duplicate_functions if f[0] == name][0]
    print(f'  {name}:')
    print(f'    Original: line {orig_line}')
    print(f'    Duplicate: line {dup_line}')
    print()

print(f'Total true duplicates: {len(true_duplicates)}')
