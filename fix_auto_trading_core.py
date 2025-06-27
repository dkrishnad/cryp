"""
Core Auto Trading Fix - Proper Backend Startup
This script ensures the backend starts with the correct working directory and loads the right data files.
"""

import os
import sys
import subprocess
import time
import requests

def fix_data_files():
    """Consolidate and fix data files"""
    print("=== FIXING DATA FILES ===")
    
    # Ensure main data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Set correct auto trading status
    auto_trading_status = {
        "enabled": True,
        "active_trades": [],
        "total_profit": 0.0,
        "signals_processed": 0
    }
    
    # Set correct virtual balance  
    virtual_balance = {
        "balance": 10000.0,
        "current_pnl": 0.0,
        "total_value": 10000.0,
        "last_updated": "2025-06-24T03:30:00.000000"
    }
    
    # Write to main data directory
    import json
    with open("data/auto_trading_status.json", "w") as f:
        json.dump(auto_trading_status, f)
    print(f"✅ Set auto_trading_status.json: enabled={auto_trading_status['enabled']}")
    
    with open("data/virtual_balance.json", "w") as f:
        json.dump(virtual_balance, f)
    print(f"✅ Set virtual_balance.json: balance=${virtual_balance['balance']:,.2f}")

def kill_processes():
    """Kill existing Python processes"""
    print("=== STOPPING EXISTING PROCESSES ===")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T"], 
                      capture_output=True, check=False)
        print("✅ Stopped existing Python processes")
        time.sleep(3)
    except Exception as e:
        print(f"⚠ Warning stopping processes: {e}")

def start_backend():
    """Start backend from correct directory"""
    print("=== STARTING BACKEND ===")
    
    # Ensure we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Error: backend/main.py not found. Run from project root.")
        return False
        
    # Start backend with correct working directory
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.main:app", 
        "--host", "127.0.0.1", "--port", "8000", "--reload"
    ], cwd=os.getcwd())
    
    print(f"✅ Started backend (PID: {backend_process.pid})")
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    for i in range(10):
        try:
            resp = requests.get("http://127.0.0.1:8000/auto_trading/status", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                enabled = data.get("auto_trading", {}).get("enabled", False)
                print(f"✅ Backend started successfully! Auto trading enabled: {enabled}")
                return True
        except:
            time.sleep(1)
            print(f"   Attempt {i+1}/10...")
    
    print("❌ Backend failed to start properly")
    return False

def start_dashboard():
    """Start dashboard"""
    print("=== STARTING DASHBOARD ===")
    
    dashboard_process = subprocess.Popen([
        sys.executable, "dashboard/app.py"
    ], cwd=os.getcwd())
    
    print(f"✅ Started dashboard (PID: {dashboard_process.pid})")
    time.sleep(2)
    return True

def test_system():
    """Test the complete system"""
    print("=== TESTING SYSTEM ===")
    
    try:
        # Test auto trading status
        resp = requests.get("http://127.0.0.1:8000/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            enabled = data.get("auto_trading", {}).get("enabled", False)
            print(f"✅ Auto trading status: enabled={enabled}")
        else:
            print(f"❌ Auto trading status failed: {resp.status_code}")
            
        # Test virtual balance
        resp = requests.get("http://127.0.0.1:8000/virtual_balance")
        if resp.status_code == 200:
            data = resp.json()
            balance = data.get("balance", 0)
            print(f"✅ Virtual balance: ${balance:,.2f}")
        else:
            print(f"❌ Virtual balance failed: {resp.status_code}")
            
        print("\n🎉 SYSTEM READY!")
        print("📱 Dashboard: http://127.0.0.1:8050")
        print("🔧 Backend API: http://127.0.0.1:8000")
        
    except Exception as e:
        print(f"❌ System test failed: {e}")

if __name__ == "__main__":
    print("🚀 CORE AUTO TRADING FIX")
    print("=" * 50)
    
    fix_data_files()
    kill_processes()
    
    if start_backend():
        start_dashboard()
        test_system()
    else:
        print("❌ Failed to start backend properly")
        
    print("\nPress Ctrl+C to stop all services")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        kill_processes()
