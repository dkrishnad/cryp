#!/usr/bin/env python3
"""
Correct test using the right component IDs
"""
from dash_app import app
from layout import layout
import callbacks

# Set layout
app.layout = layout

print(f"App ready with {len(app.callback_map)} callbacks registered")

# Let's verify the test callback from callbacks.py is working
# It should trigger on interval-prediction and update test-output

if __name__ == "__main__":
    print("Starting dashboard on http://localhost:8050...")
    print("The test callback should trigger on 'interval-prediction' and update 'test-output'")
    print("You should see '[DASH TEST] test_callback triggered' messages in the terminal")
    
    try:
        app.run(debug=True, port=8050, host="0.0.0.0")
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
