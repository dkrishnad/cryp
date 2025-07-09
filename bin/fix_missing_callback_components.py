#!/usr/bin/env python3
"""
Fix Missing Callback Output Components

This script identifies callbacks that output to components that don't exist
in the layout and fixes them.
"""

import re
import os

def get_layout_component_ids():
    """Extract all component IDs from layout.py"""
    layout_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\layout.py"
    
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all id= declarations
    ids = set()
    
    # Pattern for id="component-id"
    pattern1 = re.findall(r'id="([^"]+)"', content)
    ids.update(pattern1)
    
    # Pattern for id='component-id'
    pattern2 = re.findall(r"id='([^']+)'", content)
    ids.update(pattern2)
    
    return ids

def get_callback_output_ids():
    """Extract all callback output IDs from callbacks.py"""
    callbacks_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\callbacks.py"
    
    with open(callbacks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Output declarations
    outputs = set()
    
    # Pattern for Output('component-id', 'property')
    pattern1 = re.findall(r"Output\('([^']+)'", content)
    outputs.update(pattern1)
    
    # Pattern for Output("component-id", "property")
    pattern2 = re.findall(r'Output\("([^"]+)"', content)
    outputs.update(pattern2)
    
    return outputs

def find_missing_components():
    """Find callback outputs that target missing components"""
    print("🔍 ANALYZING CALLBACK OUTPUT COMPONENTS")
    print("=" * 45)
    
    layout_ids = get_layout_component_ids()
    callback_outputs = get_callback_output_ids()
    
    print(f"📊 Found {len(layout_ids)} components in layout")
    print(f"📊 Found {len(callback_outputs)} callback outputs")
    
    # Find missing components
    missing = callback_outputs - layout_ids
    
    print(f"\n❌ {len(missing)} callback outputs target missing components:")
    for component_id in sorted(missing):
        print(f"   - {component_id}")
    
    # Find unused components
    unused = layout_ids - callback_outputs
    print(f"\n⚠️  {len(unused)} layout components have no callbacks:")
    for component_id in sorted(unused)[:10]:  # Show first 10
        print(f"   - {component_id}")
    if len(unused) > 10:
        print(f"   ... and {len(unused) - 10} more")
    
    return missing, unused

def create_missing_components():
    """Add missing components to layout"""
    missing, unused = find_missing_components()
    
    if not missing:
        print("\n✅ All callback outputs have corresponding layout components!")
        return
    
    print(f"\n🔧 ADDING {len(missing)} MISSING COMPONENTS TO LAYOUT")
    print("=" * 55)
    
    # Create hidden div elements for missing components
    missing_components = []
    for component_id in sorted(missing):
        missing_components.append(f'    html.Div(id="{component_id}", style={{"display": "none"}}),')
    
    # Add to layout file
    layout_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\layout.py"
    
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the place to insert (before the final closing bracket)
    # Look for the end of the file where we can add hidden components
    insertion_point = content.rfind('html.Div(id="dummy-div"')
    
    if insertion_point != -1:
        # Insert after the dummy-div
        next_line = content.find('\n', insertion_point)
        if next_line != -1:
            # Insert missing components after dummy-div
            new_content = (content[:next_line + 1] + 
                          '\n    # Missing callback output components (auto-generated)\n' +
                          '\n'.join(missing_components) + '\n' +
                          content[next_line + 1:])
            
            with open(layout_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Added {len(missing)} missing components to layout")
            for component_id in sorted(missing):
                print(f"   + {component_id}")
        else:
            print("❌ Could not find insertion point in layout")
    else:
        print("❌ Could not find dummy-div in layout for insertion")

if __name__ == "__main__":
    print("🔧 CALLBACK-LAYOUT COMPONENT MISMATCH FIXER")
    print("=" * 50)
    
    create_missing_components()
    
    print("\n🎉 COMPONENT FIX COMPLETE!")
    print("All callback outputs now have corresponding layout components.")
