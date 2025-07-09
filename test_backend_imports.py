#!/usr/bin/env python3
"""
Simple test to check main.py imports and basic startup
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.getcwd(), "backendtest")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

print("🔍 Testing main.py imports...")

try:
    # Test critical imports one by one
    print("📦 Testing DB imports...")
    from db import initialize_database, get_trades, save_trade
    print("✅ DB imports successful")
    
    print("📦 Testing trading imports...")
    from trading import open_virtual_trade
    print("✅ Trading imports successful")
    
    print("📦 Testing ML imports...")
    from ml import real_predict
    print("✅ ML imports successful")
    
    print("📦 Testing WebSocket imports...")
    from ws import router as ws_router
    print("✅ WebSocket imports successful")
    
    print("📦 Testing hybrid learning imports...")
    from hybrid_learning import hybrid_orchestrator
    print("✅ Hybrid learning imports successful")
    
    print("📦 Testing online learning imports...")
    from online_learning import online_learning_manager
    print("✅ Online learning imports successful")
    
    print("📦 Testing futures trading imports...")
    from futures_trading import FuturesTradingEngine, FuturesSignal
    print("✅ Futures trading imports successful")
    
    print("📦 Testing binance futures imports...")
    from binance_futures_exact import BinanceFuturesTradingEngine
    print("✅ Binance futures imports successful")
    
    print("📦 Testing advanced auto trading imports...")
    from advanced_auto_trading import AdvancedAutoTradingEngine
    print("✅ Advanced auto trading imports successful")
    
    print("📦 Testing missing endpoints imports...")
    from missing_endpoints import get_missing_endpoints_router
    print("✅ Missing endpoints imports successful")
    
    print("\n🎉 All main.py imports working!")
    print("✅ Backend appears to be ready to start")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
