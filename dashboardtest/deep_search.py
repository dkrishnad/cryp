#!/usr/bin/env python3
"""
Deep search for components in layout
"""
from dash_app import app
from layout import layout
import callbacks

# Set layout
app.layout = layout

def deep_find_components(component, found_ids=None, depth=0):
    """Recursively find all components with IDs"""
    if found_ids is None:
        found_ids = {}
    
    # Check if this component has an ID
    if hasattr(component, 'id') and component.id:
        found_ids[component.id] = {
            'component': component,
            'depth': depth,
            'type': type(component).__name__
        }
    
    # Recursively search children
    if hasattr(component, 'children'):
        if isinstance(component.children, list):
            for child in component.children:
                deep_find_components(child, found_ids, depth + 1)
        elif component.children is not None:
            deep_find_components(component.children, found_ids, depth + 1)
    
    return found_ids

print("Deep searching for all components with IDs...")
all_components = deep_find_components(app.layout)

print(f"Found {len(all_components)} components with IDs:")
for comp_id, info in sorted(all_components.items()):
    print(f"  {comp_id}: {info['type']} (depth {info['depth']})")

# Check specifically for our target components
target_components = ["interval-indicators", "test-output", "interval-prediction", "live-price"]
print("\nChecking for target components:")
for target in target_components:
    if target in all_components:
        info = all_components[target]
        print(f"  ✓ {target}: {info['type']} found at depth {info['depth']}")
    else:
        print(f"  ✗ {target}: NOT FOUND")

print(f"\nTotal callbacks registered: {len(app.callback_map)}")
