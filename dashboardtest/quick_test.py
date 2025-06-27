print("Dashboard quick test starting...")
try:
    print("Step 1: Import dash")
    import dash
    print("Step 2: Import dbc")  
    import dash_bootstrap_components
    print("Step 3: Import layout")
    from layout import layout
    print("Step 4: Create app")
    app = dash.Dash(__name__)
    app.layout = layout
    print("SUCCESS: All tests passed!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
