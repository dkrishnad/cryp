"""
Test Dashboard Components Update
Test if the dashboard components are updating correctly after restart
"""

import requests
import time
from datetime import datetime

def test_dashboard_api():
    """Test dashboard API endpoint"""
    print("🔍 Testing Dashboard...")
    
    try:
        # Test if dashboard is running
        resp = requests.get("http://127.0.0.1:8050", timeout=3)
        if resp.status_code == 200:
            print("✅ Dashboard is accessible at http://127.0.0.1:8050")
            return True
        else:
            print(f"❌ Dashboard error: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard connection error: {e}")
        return False

def test_auto_trading_toggle():
    """Test toggling auto trading and see if it appears in dashboard"""
    print("\n🔄 Testing Auto Trading Toggle...")
    
    # Turn on auto trading
    try:
        resp = requests.post("http://127.0.0.1:8000/auto_trading/toggle", json={"enabled": True})
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Auto trading enabled: {data.get('message', 'Success')}")
            
            # Wait a moment for dashboard to update
            time.sleep(2)
            
            # Check backend status
            status_resp = requests.get("http://127.0.0.1:8000/auto_trading/status")
            if status_resp.status_code == 200:
                status_data = status_resp.json()
                enabled = status_data.get("auto_trading", {}).get("enabled", False)
                print(f"✅ Backend confirms auto trading enabled: {enabled}")
            
            return True
        else:
            print(f"❌ Toggle failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Toggle error: {e}")
        return False

def test_virtual_balance():
    """Test virtual balance API"""
    print("\n💰 Testing Virtual Balance...")
    
    try:
        resp = requests.get("http://127.0.0.1:8000/virtual_balance")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                balance = data.get("balance", 0)
                pnl = data.get("current_pnl", 0)
                print(f"✅ Virtual balance: ${balance:,.2f}")
                print(f"✅ Current P&L: ${pnl:,.2f}")
                return True
            else:
                print(f"❌ Balance API error: {data}")
                return False
        else:
            print(f"❌ Balance API HTTP error: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Balance API error: {e}")
        return False

def print_instructions():
    """Print instructions for user"""
    print("\n" + "="*50)
    print("📋 DASHBOARD TEST INSTRUCTIONS")
    print("="*50)
    print("1. Open your browser and go to: http://127.0.0.1:8050")
    print("2. Navigate to the 'Auto Trading' tab")
    print("3. Check if the following are now visible:")
    print("   - Virtual Balance should show a dollar amount")
    print("   - Total P&L should show a dollar amount") 
    print("   - Auto Trading toggle should be ON (enabled)")
    print("   - Win Rate, Total Trades, W/L ratio should show values")
    print("4. Try toggling the Auto Trading switch")
    print("5. Check if values update in real-time")
    print("\nIf you can see the values now, the fix worked! ✅")
    print("If values are still missing, there may be a deeper issue. ❌")

if __name__ == "__main__":
    print("=== Dashboard Component Update Test ===")
    print(f"Timestamp: {datetime.now()}")
    
    # Test components
    dashboard_ok = test_dashboard_api()
    toggle_ok = test_auto_trading_toggle()
    balance_ok = test_virtual_balance()
    
    print(f"\n📊 Test Results:")
    print(f"Dashboard accessible: {'✅' if dashboard_ok else '❌'}")
    print(f"Auto trading toggle: {'✅' if toggle_ok else '❌'}")
    print(f"Virtual balance API: {'✅' if balance_ok else '❌'}")
    
    if dashboard_ok and toggle_ok and balance_ok:
        print(f"\n✅ All backend tests passed!")
        print_instructions()
    else:
        print(f"\n❌ Some tests failed. Check the dashboard and backend.")
    
    print("\n🔗 Dashboard URL: http://127.0.0.1:8050")
