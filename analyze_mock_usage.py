#!/usr/bin/env python3
"""
Analyze main.py to determine which modules are real vs mock
and suggest improvements to reduce unnecessary mocking.
"""

import os
import sys

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

def check_module_availability():
    """Check which modules are actually available vs mocked"""
    
    results = {
        'available': [],
        'missing': [],
        'mocked_unnecessarily': []
    }
    
    modules_to_check = [
        ('db', ['initialize_database', 'get_trades', 'save_trade']),
        ('trading', ['open_virtual_trade']),
        ('ml', ['real_predict']),
        ('ws', ['router']),
        ('hybrid_learning', ['hybrid_orchestrator']),
        ('online_learning', ['online_learning_manager']),
        ('data_collection', ['get_data_collector']),
        ('email_utils', ['get_email_config', 'send_email']),
        ('price_feed', ['get_binance_price']),
        ('futures_trading', ['FuturesTradingEngine', 'FuturesSignal']),
        ('binance_futures_exact', ['BinanceFuturesTradingEngine']),
        ('advanced_auto_trading', ['AdvancedAutoTradingEngine', 'TradingSignal'])
    ]
    
    for module_name, expected_items in modules_to_check:
        try:
            print(f"\n[CHECK] Testing module: {module_name}")
            module = __import__(module_name)
            
            # Check if expected items exist
            missing_items = []
            for item in expected_items:
                if not hasattr(module, item):
                    missing_items.append(item)
            
            if missing_items:
                print(f"  [PARTIAL] Module exists but missing: {missing_items}")
                results['available'].append(f"{module_name} (partial)")
            else:
                print(f"  [OK] Module fully available")
                results['available'].append(module_name)
                
        except ImportError as e:
            print(f"  [MISSING] {e}")
            results['missing'].append(module_name)
        except Exception as e:
            print(f"  [ERROR] {e}")
            results['missing'].append(f"{module_name} (error)")
    
    return results

def analyze_main_py_mocks():
    """Analyze main.py to see which mocks are being used"""
    
    main_py_path = os.path.join(backend_dir, 'main.py')
    
    if not os.path.exists(main_py_path):
        print(f"[ERROR] main.py not found at {main_py_path}")
        return
        
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n" + "="*60)
    print("MOCK ANALYSIS IN MAIN.PY")
    print("="*60)
    
    # Find mock patterns
    mock_patterns = [
        'def initialize_database(): pass',
        'def open_virtual_trade(',
        'def real_predict(',
        'class MockOrchestrator:',
        'class MockOnlineLearning:',
        'class MockDataCollector:',
        'class MockFuturesEngine:',
        'class MockBinanceFuturesEngine:',
        'class AdvancedAutoTradingEngine:',  # In the except block
    ]
    
    for pattern in mock_patterns:
        if pattern in content:
            print(f"[MOCK FOUND] {pattern}")
        else:
            print(f"[NO MOCK] {pattern}")

def suggest_improvements():
    """Suggest how to improve the mock handling"""
    
    print("\n" + "="*60)
    print("SUGGESTIONS FOR IMPROVEMENT")
    print("="*60)
    
    print("""
1. GOOD PATTERNS (keep these):
   - Lazy initialization with get_* functions
   - Clear error messages when features unavailable
   - Graceful degradation instead of crashes
   - API compatibility maintained

2. POTENTIAL IMPROVEMENTS:
   - Add feature availability flags to make it clear when real vs mock
   - Create a central feature registry to track what's available
   - Add startup logging to show which features are active
   - Consider environment variables to control feature availability

3. MOCK REMOVAL STRATEGY:
   - Only remove mocks for modules that ALWAYS should be available
   - Keep mocks for truly optional features (advanced ML, futures trading)
   - Replace simple mocks with informative error handlers

4. FEATURE DETECTION:
   - Add /api/features endpoint to show what's available
   - Add dashboard indicators for feature availability
   - Log feature availability at startup
""")

if __name__ == "__main__":
    print("CRYPTO BOT - MOCK VS REAL MODULE ANALYSIS")
    print("="*60)
    
    # Check what's actually available
    results = check_module_availability()
    
    print(f"\n[SUMMARY]")
    print(f"Available modules: {len(results['available'])}")
    print(f"Missing modules: {len(results['missing'])}")
    
    print(f"\nAVAILABLE: {', '.join(results['available'])}")
    print(f"MISSING: {', '.join(results['missing'])}")
    
    # Analyze main.py mocks
    analyze_main_py_mocks()
    
    # Provide suggestions
    suggest_improvements()
