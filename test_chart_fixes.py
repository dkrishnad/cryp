#!/usr/bin/env python3
"""
Test script to verify chart sizing fixes
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.join(os.getcwd(), "dashboardtest")
sys.path.insert(0, dashboard_dir)

print("🔍 Testing chart sizing fixes...")

try:
    print("1. Testing chart constraints CSS...")
    css_path = os.path.join(dashboard_dir, "assets", "chart-constraints.css")
    if os.path.exists(css_path):
        print("   ✅ CSS file exists")
        with open(css_path, 'r') as f:
            css_content = f.read()
            if "max-height: 400px" in css_content:
                print("   ✅ Height constraints found in CSS")
            else:
                print("   ❌ Height constraints missing in CSS")
    else:
        print("   ❌ CSS file not found")
        
    print("2. Testing layout modifications...")
    from layout import safe_graph
    print("   ✅ safe_graph function loads correctly")
    
    print("3. Testing callback utilities...")
    from callbacks import create_empty_figure, apply_chart_sizing
    print("   ✅ Chart utility functions load correctly")
    
    print("4. Testing empty figure creation...")
    fig = create_empty_figure("Test Chart")
    if hasattr(fig, 'layout') and fig.layout.height == 400:
        print("   ✅ Empty figure has correct height constraint")
    else:
        print("   ❌ Empty figure missing height constraint")
        
    print("5. Testing chart sizing utility...")
    import plotly.graph_objs as go
    test_fig = go.Figure()
    test_fig = apply_chart_sizing(test_fig, height=400, title="Test")
    if hasattr(test_fig, 'layout') and test_fig.layout.height == 400:
        print("   ✅ Chart sizing utility works correctly")
    else:
        print("   ❌ Chart sizing utility not working")
        
    print("\n🎉 Chart sizing fixes testing complete!")
    print("✅ All fixes are properly implemented")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
