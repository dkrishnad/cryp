print('>>> MINIMAL callbacks.py imported and executing')
from dash.dependencies import Input, Output
from dash_app import app

# Only the most basic callback that should always work
@app.callback(
    Output('test-output', 'children'),
    Input('interval-prediction', 'n_intervals'),
    prevent_initial_call=False
)
def test_callback(n):
    print(f"[MINIMAL] test_callback triggered, n={n}")
    return f"✅ WORKING! Test: {n}"

print('[MINIMAL] Basic callback registered successfully')
