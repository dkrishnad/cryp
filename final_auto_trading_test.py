"""
Final Auto Trading Test
Comprehensive test of all auto trading features
"""

import requests
import time
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000"
DASHBOARD_URL = "http://127.0.0.1:8050"

def test_all_features():
    """Test all auto trading features"""
    print("=== COMPREHENSIVE AUTO TRADING TEST ===")
    print(f"Timestamp: {datetime.now()}")
    
    results = {}
    
    # 1. Test Dashboard Accessibility
    print("\n1️⃣ Testing Dashboard Accessibility...")
    try:
        resp = requests.get(DASHBOARD_URL, timeout=5)
        results['dashboard'] = resp.status_code == 200
        print(f"   Dashboard: {'✅ Accessible' if results['dashboard'] else '❌ Not accessible'}")
    except Exception as e:
        results['dashboard'] = False
        print(f"   Dashboard: ❌ Error: {e}")
    
    # 2. Test Backend APIs
    print("\n2️⃣ Testing Backend APIs...")
    
    # Virtual Balance
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                balance = data.get("balance", 0)
                pnl = data.get("current_pnl", 0)
                results['virtual_balance'] = True
                print(f"   Virtual Balance: ✅ ${balance:,.2f} (P&L: ${pnl:,.2f})")
            else:
                results['virtual_balance'] = False
                print(f"   Virtual Balance: ❌ API Error: {data}")
        else:
            results['virtual_balance'] = False
            print(f"   Virtual Balance: ❌ HTTP {resp.status_code}")
    except Exception as e:
        results['virtual_balance'] = False
        print(f"   Virtual Balance: ❌ Exception: {e}")
    
    # Auto Trading Status
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                auto_trading = data.get("auto_trading", {})
                enabled = auto_trading.get("enabled", False)
                results['auto_trading_status'] = True
                print(f"   Auto Trading Status: ✅ Enabled: {enabled}")
            else:
                results['auto_trading_status'] = False
                print(f"   Auto Trading Status: ❌ API Error: {data}")
        else:
            results['auto_trading_status'] = False
            print(f"   Auto Trading Status: ❌ HTTP {resp.status_code}")
    except Exception as e:
        results['auto_trading_status'] = False
        print(f"   Auto Trading Status: ❌ Exception: {e}")
    
    # Trades API
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                count = data.get("count", 0)
                summary = data.get("summary", {})
                win_rate = summary.get("win_rate", 0)
                results['trades_api'] = True
                print(f"   Trades API: ✅ {count} trades, {win_rate:.1f}% win rate")
            else:
                results['trades_api'] = False
                print(f"   Trades API: ❌ API Error: {data}")
        else:
            results['trades_api'] = False
            print(f"   Trades API: ❌ HTTP {resp.status_code}")
    except Exception as e:
        results['trades_api'] = False
        print(f"   Trades API: ❌ Exception: {e}")
    
    # 3. Test Auto Trading Toggle
    print("\n3️⃣ Testing Auto Trading Toggle...")
    try:
        # Turn OFF first
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": False})
        if resp.status_code == 200:
            print("   ✅ Successfully turned OFF auto trading")
            time.sleep(1)
            
            # Turn ON
            resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
            if resp.status_code == 200:
                data = resp.json()
                results['toggle'] = data.get("status") == "success"
                print(f"   ✅ Successfully turned ON auto trading: {data.get('message', '')}")
            else:
                results['toggle'] = False
                print(f"   ❌ Failed to turn ON: {resp.status_code}")
        else:
            results['toggle'] = False
            print(f"   ❌ Failed to turn OFF: {resp.status_code}")
    except Exception as e:
        results['toggle'] = False
        print(f"   ❌ Toggle Exception: {e}")
    
    # 4. Test Signal Generation
    print("\n4️⃣ Testing Signal Generation...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                signal_type = signal.get("signal", "")
                confidence = signal.get("confidence", 0)
                symbol = signal.get("symbol", "")
                results['signal'] = True
                print(f"   ✅ Signal: {signal_type} for {symbol} ({confidence:.1f}% confidence)")
            else:
                results['signal'] = False
                print(f"   ❌ No signal available or API error: {data}")
        else:
            results['signal'] = False
            print(f"   ❌ Signal API HTTP {resp.status_code}")
    except Exception as e:
        results['signal'] = False
        print(f"   ❌ Signal Exception: {e}")
    
    # 5. Summary
    print("\n📊 TEST SUMMARY")
    print("="*40)
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Auto trading system is fully functional!")
    elif passed_tests >= total_tests * 0.8:
        print("\n✅ Most tests passed. System is mostly functional.")
    else:
        print("\n❌ Several tests failed. Check the system.")
    
    # 6. User Instructions
    print("\n📋 USER TESTING INSTRUCTIONS")
    print("="*40)
    print("1. Open browser: http://127.0.0.1:8050")
    print("2. Go to 'Auto Trading' tab")
    print("3. Check that you can see:")
    print("   - Virtual Balance (dollar amount)")
    print("   - Total P&L (dollar amount)")
    print("   - Win Rate percentage")
    print("   - Total Trades count")
    print("   - W/L ratio")
    print("   - Auto Trading toggle (should be ON)")
    print("4. Try toggling Auto Trading ON/OFF")
    print("5. Watch for real-time updates")
    
    if results.get('dashboard') and results.get('auto_trading_status'):
        print("\n✅ Dashboard and backend are communicating!")
    else:
        print("\n❌ Dashboard or backend communication issue!")
    
    return results

if __name__ == "__main__":
    results = test_all_features()
    
    # Return appropriate exit code
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    if passed_tests == total_tests:
        print(f"\n🎉 SUCCESS: All {total_tests} tests passed!")
        exit(0)
    else:
        print(f"\n⚠️  PARTIAL SUCCESS: {passed_tests}/{total_tests} tests passed!")
        exit(1)
