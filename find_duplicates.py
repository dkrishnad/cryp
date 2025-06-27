import re
from collections import Counter

with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all Output component IDs
outputs = re.findall(r'Output\s*\(\s*[\'\"](.*?)[\'\"]', content)
output_counts = Counter(outputs)

print('DUPLICATE CALLBACK OUTPUTS:')
duplicates = []
for output, count in output_counts.items():
    if count > 1:
        print(f'{output}: {count} times')
        duplicates.append(output)
        
print(f'\nTotal outputs: {len(outputs)}')
print(f'Unique outputs: {len(output_counts)}')
print(f'Duplicates found: {len(duplicates)}')
