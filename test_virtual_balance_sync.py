#!/usr/bin/env python3
"""
Test virtual balance synchronization across all tabs
"""

import requests
import time
import json

API_URL = "http://localhost:8001"

def test_virtual_balance_endpoints():
    """Test all virtual balance related endpoints"""
    print("=== Testing Virtual Balance Endpoints ===\n")
    
    # Test GET virtual_balance
    print("1. Testing GET /virtual_balance...")
    try:
        response = requests.get(f"{API_URL}/virtual_balance", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ GET virtual_balance working")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test POST virtual_balance (reset to 10000)
    print("2. Testing POST /virtual_balance (reset)...")
    try:
        response = requests.post(f"{API_URL}/virtual_balance", 
                               json={"balance": 10000.0}, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ POST virtual_balance working")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test update to different amount
    print("3. Testing POST /virtual_balance (custom amount)...")
    try:
        response = requests.post(f"{API_URL}/virtual_balance", 
                               json={"balance": 15000.0}, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ Custom balance update working")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Verify the change
    print("4. Verifying balance change...")
    try:
        response = requests.get(f"{API_URL}/virtual_balance", timeout=5)
        if response.status_code == 200:
            data = response.json()
            balance = data.get('balance', 0)
            if balance == 15000.0:
                print(f"✓ Balance correctly updated to ${balance:,.2f}")
            else:
                print(f"✗ Balance mismatch: expected $15,000.00, got ${balance:,.2f}")
        else:
            print(f"✗ Failed to verify: status {response.status_code}")
    except Exception as e:
        print(f"✗ Error verifying: {e}")

def test_balance_endpoint():
    """Test the /balance endpoint used by some callbacks"""
    print("\n=== Testing Balance Endpoint ===\n")
    
    try:
        response = requests.get(f"{API_URL}/balance", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print("✓ GET /balance working")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_synchronization_scenario():
    """Test a realistic synchronization scenario"""
    print("\n=== Testing Synchronization Scenario ===\n")
    
    # Set initial balance
    print("Setting initial balance to $12,500...")
    try:
        response = requests.post(f"{API_URL}/virtual_balance", 
                               json={"balance": 12500.0}, timeout=5)
        if response.status_code == 200:
            print("✓ Initial balance set")
        else:
            print("✗ Failed to set initial balance")
            return
    except Exception as e:
        print(f"✗ Error setting balance: {e}")
        return
    
    # Simulate checking from different tabs
    print("\nSimulating balance checks from different tabs...")
    
    for i in range(3):
        try:
            response = requests.get(f"{API_URL}/virtual_balance", timeout=3)
            if response.status_code == 200:
                data = response.json()
                balance = data.get('balance', 0)
                pnl = data.get('current_pnl', 0)
                print(f"Check {i+1}: Balance=${balance:,.2f}, P&L=${pnl:,.2f}")
            time.sleep(1)
        except Exception as e:
            print(f"Check {i+1} failed: {e}")
    
    print("✓ Synchronization test completed")

def main():
    """Run all virtual balance tests"""
    print("🧪 VIRTUAL BALANCE SYNCHRONIZATION TEST\n")
    
    # Check if backend is running
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not accessible. Please start the backend first.")
            return
    except Exception:
        print("❌ Backend not running. Please start with: cd backend && uvicorn main:app --reload")
        return
    
    print("✅ Backend is running\n")
    
    # Run tests
    test_virtual_balance_endpoints()
    test_balance_endpoint()
    test_synchronization_scenario()
    
    print("\n🎉 Virtual balance testing completed!")
    print("\nThe virtual balance should now synchronize across:")
    print("• Main dashboard sidebar")
    print("• Auto trading tab")
    print("• Futures trading tab")
    print("• All other tabs that display balance")

if __name__ == "__main__":
    main()
