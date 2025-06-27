#!/usr/bin/env python3
"""
Test script to simulate dashboard interactions and check if callbacks work.
"""

import requests
import json
import time

def test_dashboard_response():
    """Test if dashboard is responding"""
    try:
        response = requests.get("http://localhost:8050", timeout=5)
        print(f"✓ Dashboard responds with status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Dashboard not responding: {e}")
        return False

def test_callback_endpoint():
    """Test if callback endpoint is available"""
    try:
        # This should return a 400 error with proper callback format but shows endpoint works
        response = requests.post("http://localhost:8050/_dash-update-component", 
                                json={}, timeout=5)
        print(f"✓ Callback endpoint responds with status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Callback endpoint not responding: {e}")
        return False

def test_symbol_dropdown_callback():
    """Test the symbol dropdown callback"""
    try:
        # Simulate a symbol dropdown change
        callback_data = {
            "output": "open-positions-table.data",
            "outputs": [{"id": "open-positions-table", "property": "data"}],
            "inputs": [{"id": "symbol-dropdown", "property": "value", "value": "BTCUSDT"}],
            "changedPropIds": ["symbol-dropdown.value"],
            "state": []
        }
        
        response = requests.post("http://localhost:8050/_dash-update-component",
                               json=callback_data,
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        print(f"Symbol dropdown callback status: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✓ Symbol dropdown callback successful")
                print(f"Response type: {type(result)}")
                return True
            except json.JSONDecodeError as e:
                print(f"✗ JSON decode error: {e}")
                print(f"Response text: {response.text[:500]}...")
                return False
        else:
            print(f"✗ Symbol dropdown callback failed: {response.text[:500]}...")
            return False
            
    except Exception as e:
        print(f"✗ Symbol dropdown callback error: {e}")
        return False

def main():
    print("=== Dashboard Interaction Test ===")
    print()
    
    # Test basic dashboard response
    if not test_dashboard_response():
        print("Dashboard is not running. Please start it first.")
        return
    
    time.sleep(1)
    
    # Test callback endpoint
    if not test_callback_endpoint():
        print("Callback endpoint is not working.")
        return
    
    time.sleep(1)
    
    # Test symbol dropdown callback
    test_symbol_dropdown_callback()
    
    print()
    print("=== Test Complete ===")

if __name__ == "__main__":
    main()
