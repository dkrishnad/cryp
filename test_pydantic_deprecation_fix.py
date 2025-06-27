#!/usr/bin/env python3
"""
Test script to verify that all Pydantic deprecation warnings have been resolved.
This script will test model serialization across the entire codebase.
"""

import sys
import warnings
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

def test_pydantic_models():
    """Test all Pydantic models to ensure no deprecation warnings."""
    
    print("🔍 Testing Pydantic model serialization for deprecation warnings...")
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        
        try:
            # Test backend models
            from backend.main import Position, AccountInfo, TradingSignal, AutoTradingSettings
            from backend.futures_trading import FuturesPosition, FuturesAccountInfo, FuturesSettings
            from backend.binance_futures_exact import BinancePosition, BinanceAccountInfo, BinanceOrder
            
            print("✅ Successfully imported all Pydantic models")
            
            # Test Position model
            position = Position(
                symbol="BTCUSDT",
                side="long",
                size=0.1,
                entry_price=50000.0,
                current_price=51000.0,
                unrealized_pnl=100.0,
                status="open"
            )
            
            # Test model_dump (should not trigger warnings)
            position_data = position.model_dump()
            print(f"✅ Position.model_dump() works: {len(position_data)} fields")
            
            # Test AccountInfo model
            account_info = AccountInfo(
                balance=1000.0,
                available_balance=900.0,
                margin_level=0.0,
                total_pnl=100.0
            )
            
            account_data = account_info.model_dump()
            print(f"✅ AccountInfo.model_dump() works: {len(account_data)} fields")
            
            # Test TradingSignal model
            signal = TradingSignal(
                symbol="BTCUSDT",
                signal="buy",
                confidence=0.85,
                price=50000.0,
                timestamp="2024-01-01T00:00:00Z"
            )
            
            signal_data = signal.model_dump()
            print(f"✅ TradingSignal.model_dump() works: {len(signal_data)} fields")
            
            # Test AutoTradingSettings model
            settings = AutoTradingSettings(
                enabled=True,
                max_position_size=100.0,
                risk_percentage=2.0,
                stop_loss_percentage=5.0,
                take_profit_percentage=10.0
            )
            
            settings_data = settings.model_dump()
            print(f"✅ AutoTradingSettings.model_dump() works: {len(settings_data)} fields")
            
            # Test FuturesPosition model
            futures_position = FuturesPosition(
                symbol="BTCUSDT",
                side="LONG",
                size=0.1,
                entry_price=50000.0,
                mark_price=51000.0,
                unrealized_pnl=100.0,
                leverage=10,
                margin=500.0,
                status="open"
            )
            
            futures_data = futures_position.model_dump()
            print(f"✅ FuturesPosition.model_dump() works: {len(futures_data)} fields")
            
            # Test FuturesAccountInfo model
            futures_account = FuturesAccountInfo(
                total_wallet_balance=1000.0,
                total_unrealized_pnl=100.0,
                total_margin_balance=1100.0,
                total_position_initial_margin=500.0,
                total_open_order_initial_margin=0.0,
                available_balance=600.0,
                max_withdraw_amount=600.0
            )
            
            futures_account_data = futures_account.model_dump()
            print(f"✅ FuturesAccountInfo.model_dump() works: {len(futures_account_data)} fields")
            
            # Test FuturesSettings model
            futures_settings = FuturesSettings(
                leverage=10,
                margin_type="isolated",
                max_position_size=1000.0,
                risk_percentage=2.0,
                stop_loss_percentage=5.0,
                take_profit_percentage=10.0
            )
            
            futures_settings_data = futures_settings.model_dump()
            print(f"✅ FuturesSettings.model_dump() works: {len(futures_settings_data)} fields")
            
            # Test BinancePosition model
            binance_position = BinancePosition(
                symbol="BTCUSDT",
                position_side="LONG",
                position_amt="0.1",
                entry_price="50000.0",
                mark_price="51000.0",
                unrealized_pnl="100.0",
                percentage="2.0"
            )
            
            binance_position_data = binance_position.model_dump()
            print(f"✅ BinancePosition.model_dump() works: {len(binance_position_data)} fields")
            
            # Test BinanceAccountInfo model
            binance_account = BinanceAccountInfo(
                total_wallet_balance="1000.0",
                total_unrealized_pnl="100.0",
                total_margin_balance="1100.0",
                total_position_initial_margin="500.0",
                total_open_order_initial_margin="0.0",
                available_balance="600.0",
                max_withdraw_amount="600.0"
            )
            
            binance_account_data = binance_account.model_dump()
            print(f"✅ BinanceAccountInfo.model_dump() works: {len(binance_account_data)} fields")
            
            # Test BinanceOrder model
            binance_order = BinanceOrder(
                order_id="12345",
                symbol="BTCUSDT",
                side="BUY",
                type="LIMIT",
                quantity="0.1",
                price="50000.0",
                status="NEW",
                time_in_force="GTC"
            )
            
            binance_order_data = binance_order.model_dump()
            print(f"✅ BinanceOrder.model_dump() works: {len(binance_order_data)} fields")
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error testing models: {e}")
            return False
    
    # Check for Pydantic deprecation warnings
    pydantic_warnings = [
        w for w in warning_list 
        if "pydantic" in str(w.message).lower() or ".dict()" in str(w.message)
    ]
    
    if pydantic_warnings:
        print(f"\n❌ Found {len(pydantic_warnings)} Pydantic deprecation warnings:")
        for warning in pydantic_warnings:
            print(f"  - {warning.message}")
            print(f"    File: {warning.filename}:{warning.lineno}")
        return False
    else:
        print(f"\n✅ No Pydantic deprecation warnings found!")
        print(f"   Total warnings captured: {len(warning_list)}")
        
        # Show other warnings if any
        if warning_list:
            print("\n📝 Other warnings found:")
            for warning in warning_list[:5]:  # Show first 5
                print(f"  - {warning.message}")
    
    return True

def test_dict_method_usage():
    """Verify no .dict() method calls remain in the codebase."""
    
    print("\n🔍 Checking for remaining .dict() method calls...")
    
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    dict_calls_found = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    if '.dict()' in line and not line.strip().startswith('#'):
                        dict_calls_found.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.strip()
                        })
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    if dict_calls_found:
        print(f"❌ Found {len(dict_calls_found)} remaining .dict() calls:")
        for call in dict_calls_found:
            rel_path = os.path.relpath(call['file'], project_root)
            print(f"  - {rel_path}:{call['line']} -> {call['content']}")
        return False
    else:
        print("✅ No .dict() method calls found in codebase!")
        return True

def main():
    """Main test function."""
    
    print("=" * 70)
    print("🧪 PYDANTIC DEPRECATION WARNING FIX VERIFICATION")
    print("=" * 70)
    
    # Test 1: Model serialization
    models_ok = test_pydantic_models()
    
    # Test 2: .dict() method usage
    dict_calls_ok = test_dict_method_usage()
    
    print("\n" + "=" * 70)
    if models_ok and dict_calls_ok:
        print("🎉 ALL TESTS PASSED! Pydantic deprecation warnings have been resolved.")
        print("✅ All .dict() calls have been replaced with .model_dump()")
        print("✅ No Pydantic deprecation warnings detected")
    else:
        print("❌ SOME TESTS FAILED. Please review the issues above.")
        
    print("=" * 70)
    
    return models_ok and dict_calls_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
