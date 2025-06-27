#!/usr/bin/env python3
"""
Quick test to see if layout loads properly
"""
import sys
import traceback

try:
    print("Importing layout...")
    from layout import layout
    print("Layout imported successfully!")
    print(f"Layout type: {type(layout)}")
    
    # Check if layout has children
    if hasattr(layout, 'children'):
        print(f"Layout has {len(layout.children)} children")
    
    print("SUCCESS: Layout loaded without errors")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
