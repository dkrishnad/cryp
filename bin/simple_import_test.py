import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Test importing from backend
try:
    sys.path.insert(0, 'backend')
    sys.path.insert(0, '.')
    
    print("Attempting to import backend.main...")
    
    # First check if files exist
    backend_main = os.path.join('backend', 'main.py')
    print(f"backend/main.py exists: {os.path.exists(backend_main)}")
    
    futures_trading = 'futures_trading.py'
    print(f"futures_trading.py exists: {os.path.exists(futures_trading)}")
    
    # Try the import
    import backend.main as main
    print("✅ SUCCESS: Backend imported successfully!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Other Error: {e}")
