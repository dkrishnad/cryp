#!/usr/bin/env python3
"""
Simple layout fix and test.
"""

try:
    print("Testing layout import...")
    import sys
    import os
    
    # Add dashboard to path
    dashboard_dir = os.path.join(os.getcwd(), "dashboard")
    sys.path.insert(0, dashboard_dir)
    
    # Test import
    from layout import layout
    print("✓ Layout imported successfully")
    
    # Test basic structure
    if hasattr(layout, 'children'):
        print(f"✓ Layout has {len(layout.children)} main components")
    
    print("✅ Layout test passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
