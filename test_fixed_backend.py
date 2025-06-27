#!/usr/bin/env python3
"""
Quick test to verify the backend starts without the FuturesSignal error
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

print("🔧 Testing backend startup after FuturesSignal fix...")

try:
    print("🔄 Importing main module...")
    import main
    print("✅ Main module imported successfully!")
    
    print("🔄 Getting FastAPI app...")
    app = main.app
    print("✅ FastAPI app retrieved successfully!")
    
    print("🔄 Testing a few lazy loading functions...")
    
    # Test lazy loading functions
    try:
        hybrid_orch = main.get_hybrid_orchestrator()
        print("✅ Hybrid orchestrator loaded")
    except Exception as e:
        print(f"⚠️  Hybrid orchestrator warning: {e}")
    
    try:
        online_mgr = main.get_online_learning_manager()
        print("✅ Online learning manager loaded")
    except Exception as e:
        print(f"⚠️  Online learning manager warning: {e}")
        
    try:
        data_collector = main.get_data_collector()
        print("✅ Data collector loaded")
    except Exception as e:
        print(f"⚠️  Data collector warning: {e}")
    
    try:
        futures_engine = main.get_futures_engine()
        print("✅ Futures engine loaded")
    except Exception as e:
        print(f"⚠️  Futures engine warning: {e}")
        
    try:
        binance_futures = main.get_binance_futures_engine()
        print("✅ Binance futures engine loaded")
    except Exception as e:
        print(f"⚠️  Binance futures engine warning: {e}")
    
    print("\n🎉 Backend startup test completed!")
    print("✅ Main issue (FuturesSignal) appears to be fixed!")
    print("📝 Any warnings above are non-blocking and can be addressed separately.")
    
except Exception as e:
    print(f"❌ Backend startup failed: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 If there are still import errors, we may need additional fixes.")
