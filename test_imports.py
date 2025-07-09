#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
"""

import sys
import os
import traceback

# Add backend directory to Python path
backend_dir = os.path.join(os.getcwd(), "backendtest")
dashboard_dir = os.path.join(os.getcwd(), "dashboardtest")

for path in [backend_dir, dashboard_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing critical imports...")
    
    # Backend imports
    test_results = {}
    
    # Test futures trading imports
    try:
        from futures_trading import FuturesTradingEngine, FuturesSignal, FuturesPosition, FuturesAccountInfo, FuturesSettings, PositionSide, PositionStatus
        test_results["futures_trading"] = "✅ SUCCESS"
    except Exception as e:
        test_results["futures_trading"] = f"❌ FAILED: {e}"
    
    # Test binance futures exact imports
    try:
        from binance_futures_exact import BinanceFuturesTradingEngine, OrderSide, OrderType, PositionSide, TimeInForce, WorkingType, OrderStatus
        test_results["binance_futures_exact"] = "✅ SUCCESS"
    except Exception as e:
        test_results["binance_futures_exact"] = f"❌ FAILED: {e}"
    
    # Test advanced auto trading imports
    try:
        from advanced_auto_trading import AdvancedAutoTradingEngine, TradingSignal, AISignal
        test_results["advanced_auto_trading"] = "✅ SUCCESS"
    except Exception as e:
        test_results["advanced_auto_trading"] = f"❌ FAILED: {e}"
    
    # Test websocket imports
    try:
        from ws import router
        test_results["ws_router"] = "✅ SUCCESS"
    except Exception as e:
        test_results["ws_router"] = f"❌ FAILED: {e}"
    
    # Test hybrid learning imports
    try:
        from hybrid_learning import hybrid_orchestrator
        test_results["hybrid_orchestrator"] = "✅ SUCCESS"
    except Exception as e:
        test_results["hybrid_orchestrator"] = f"❌ FAILED: {e}"
    
    # Test online learning imports
    try:
        from online_learning import online_learning_manager
        test_results["online_learning_manager"] = "✅ SUCCESS"
    except Exception as e:
        test_results["online_learning_manager"] = f"❌ FAILED: {e}"
    
    # Test ML compatibility manager imports
    try:
        from ml_compatibility_manager import MLCompatibilityManager
        test_results["ml_compatibility_manager"] = "✅ SUCCESS"
    except Exception as e:
        test_results["ml_compatibility_manager"] = f"❌ FAILED: {e}"
    
    # Test storage manager imports
    try:
        from storage_manager import StorageManager
        test_results["storage_manager"] = "✅ SUCCESS"
    except Exception as e:
        test_results["storage_manager"] = f"❌ FAILED: {e}"
    
    # Test dashboard imports
    try:
        from dash_app import app
        test_results["dash_app"] = "✅ SUCCESS"
    except Exception as e:
        test_results["dash_app"] = f"❌ FAILED: {e}"
    
    try:
        from layout import layout
        test_results["layout"] = "✅ SUCCESS"
    except Exception as e:
        test_results["layout"] = f"❌ FAILED: {e}"
    
    # Test simple transfer lifecycle
    try:
        from simple_transfer_lifecycle import SimpleTransferLearningLifecycle
        test_results["simple_transfer_lifecycle"] = "✅ SUCCESS"
    except Exception as e:
        test_results["simple_transfer_lifecycle"] = f"❌ FAILED: {e}"
    
    # Test data collection import with missing classes
    try:
        from data_collection import get_data_collector, DataCollector, TechnicalIndicators
        test_results["data_collection_classes"] = "✅ SUCCESS"
    except Exception as e:
        test_results["data_collection_classes"] = f"❌ FAILED: {e}"
    
    print("\n📊 IMPORT TEST RESULTS:")
    print("=" * 80)
    for module, result in test_results.items():
        print(f"{module:30} {result}")
    
    failed_count = sum(1 for result in test_results.values() if "FAILED" in result)
    total_count = len(test_results)
    success_count = total_count - failed_count
    
    print("=" * 80)
    print(f"✅ Success: {success_count}/{total_count}")
    print(f"❌ Failed:  {failed_count}/{total_count}")
    
    if failed_count > 0:
        print(f"\n🔧 FAILED IMPORTS NEED FIXING:")
        for module, result in test_results.items():
            if "FAILED" in result:
                print(f"  - {module}: {result}")
    
    return failed_count == 0

if __name__ == "__main__":
    print("IMPORT VALIDATION TEST")
    print("=" * 80)
    success = test_imports()
    if success:
        print("\n🎉 All imports working correctly!")
    else:
        print("\n🚨 Some imports need fixing!")
    sys.exit(0 if success else 1)
