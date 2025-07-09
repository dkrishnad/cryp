#!/usr/bin/env python3
"""
Find duplicate IDs in the layout file
"""
import re

def find_duplicate_ids():
    """Find duplicate component IDs in layout.py"""
    with open("layout.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all id= patterns
    id_pattern = r'id=["\']([^"\']+)["\']'
    ids = re.findall(id_pattern, content)
    
    # Count occurrences
    id_counts = {}
    for id_name in ids:
        id_counts[id_name] = id_counts.get(id_name, 0) + 1
    
    # Find duplicates
    duplicates = {id_name: count for id_name, count in id_counts.items() if count > 1}
    
    print(f"Total IDs found: {len(ids)}")
    print(f"Unique IDs: {len(id_counts)}")
    print(f"Duplicate IDs: {len(duplicates)}")
    
    if duplicates:
        print("\nDuplicate IDs found:")
        for id_name, count in duplicates.items():
            print(f"  {id_name}: {count} times")
            
            # Find line numbers
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if f'id="{id_name}"' in line or f"id='{id_name}'" in line:
                    print(f"    Line {i}: {line.strip()}")
    else:
        print("\n✅ No duplicate IDs found!")

if __name__ == "__main__":
    find_duplicate_ids()
