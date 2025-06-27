#!/usr/bin/env python3
"""
Test the specific callbacks that weren't working
"""
from dash_app import app
from layout import layout
import callbacks
from dash import Input, Output, State, callback

# Set layout
app.layout = layout

# Test the specific interval callback that should trigger
@app.callback(
    Output("test-output", "children"),
    Input("interval-indicators", "n_intervals")
)
def debug_interval_callback(n_intervals):
    print(f"[DEBUG] Interval callback triggered with n_intervals: {n_intervals}")
    return f"Test callback working! Count: {n_intervals}"

print("Testing app setup...")
print(f"Layout type: {type(app.layout)}")
print(f"Callbacks registered: {len(app.callback_map)}")

# Check if interval component exists in layout
def find_component(component, component_id):
    """Recursively find a component by ID"""
    if hasattr(component, 'id') and component.id == component_id:
        return component
    
    if hasattr(component, 'children'):
        if isinstance(component.children, list):
            for child in component.children:
                result = find_component(child, component_id)
                if result:
                    return result
        else:
            return find_component(component.children, component_id)
    
    return None

interval_comp = find_component(app.layout, "interval-indicators")
if interval_comp:
    print(f"Found interval-indicators component: {interval_comp}")
    print(f"Interval: {interval_comp.interval}ms")
else:
    print("ERROR: interval-indicators component not found in layout!")

test_output_comp = find_component(app.layout, "test-output")
if test_output_comp:
    print(f"Found test-output component: {test_output_comp}")
else:
    print("ERROR: test-output component not found in layout!")

# Test that would normally start the server
print("App setup complete. Ready to run server.")
