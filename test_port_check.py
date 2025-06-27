#!/usr/bin/env python3
"""
Test port checking logic
"""
import requests
import time

def test_port_check():
    """Test the improved port checking"""
    print("Testing port checking logic...")
    
    def check_port(port):
        """Check if port is responding"""
        try:
            # Try multiple addresses for better compatibility
            addresses = ["http://127.0.0.1", "http://localhost"]
            
            for addr in addresses:
                try:
                    url = f"{addr}:{port}/health" if port == 8001 else f"{addr}:{port}"
                    print(f"Trying: {url}")
                    response = requests.get(url, timeout=2)
                    print(f"Response: {response.status_code}")
                    if response.status_code == 200:
                        return True
                except Exception as e:
                    print(f"Failed: {e}")
                    continue
            return False
        except:
            return False
    
    # Test backend port
    print("\n--- Testing Backend (8001) ---")
    backend_ok = check_port(8001)
    print(f"Backend status: {backend_ok}")
    
    # Test dashboard port  
    print("\n--- Testing Dashboard (8050) ---")
    dashboard_ok = check_port(8050)
    print(f"Dashboard status: {dashboard_ok}")
    
    return backend_ok, dashboard_ok

if __name__ == "__main__":
    backend, dashboard = test_port_check()
    print(f"\nResults: Backend={backend}, Dashboard={dashboard}")
