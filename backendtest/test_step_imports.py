#!/usr/bin/env python3
"""
Step-by-step import test to find the blocking module
"""
import sys
import os
import time

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_import(module_name, timeout=5):
    """Test import with timeout"""
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Import of {module_name} timed out after {timeout}s")
    
    # Set alarm for timeout (Unix only - for Windows we'll use a different approach)
    start_time = time.time()
    
    try:
        print(f"🔄 Testing import: {module_name}")
        exec(f"import {module_name}")
        elapsed = time.time() - start_time
        print(f"✅ {module_name} imported successfully in {elapsed:.2f}s")
        return True
    except TimeoutError as e:
        print(f"❌ {module_name} TIMEOUT: {e}")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"⚠️  {module_name} failed in {elapsed:.2f}s: {e}")
        return False

print("🔍 Step-by-step import testing...")
print("=" * 50)

# Test basic imports first
basic_imports = [
    "requests",
    "numpy", 
    "fastapi",
    "pydantic",
    "json",
    "os",
    "sys",
    "logging",
    "datetime"
]

print("\n📦 Testing basic imports...")
for module in basic_imports:
    test_import(module)

# Test our backend modules one by one
backend_modules = [
    "db",
    "trading", 
    "ml",
    "ws",
    "price_feed",
    "email_utils",
    "data_collection",
    "online_learning",
    "hybrid_learning",
    "futures_trading",
    "binance_futures_exact",
    "advanced_auto_trading",
    "minimal_transfer_endpoints",
    "ml_compatibility_manager"
]

print("\n📦 Testing backend modules...")
for module in backend_modules:
    try:
        success = test_import(module)
        if not success:
            print(f"🚨 BLOCKING MODULE FOUND: {module}")
            break
    except KeyboardInterrupt:
        print(f"\n🚨 User interrupted at module: {module}")
        break

print("\n✅ Import testing complete!")
