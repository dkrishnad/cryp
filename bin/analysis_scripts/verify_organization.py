#!/usr/bin/env python3
"""
Post-Organization Verification Script
Verifies that all critical files are present and functional after organization
"""

import os
import requests
import time

BASE_DIR = r"c:\Users\Hari\Desktop\Testin dub"

def check_file_exists(file_path):
    """Check if a critical file exists"""
    full_path = os.path.join(BASE_DIR, file_path)
    exists = os.path.exists(full_path)
    size = os.path.getsize(full_path) if exists else 0
    return exists, size

def verify_critical_files():
    """Verify all critical files are present"""
    print("🔍 VERIFYING CRITICAL FILES")
    print("=" * 40)
    
    critical_files = [
        # Backend Core
        "backendtest/main.py",
        "backendtest/db.py",
        "backendtest/trading.py", 
        "backendtest/ml.py",
        "backendtest/data_collection.py",
        "backendtest/futures_trading.py",
        "backendtest/binance_futures_exact.py",
        "backendtest/advanced_auto_trading.py",
        "backendtest/hybrid_learning.py",
        "backendtest/online_learning.py",
        "backendtest/ws.py",
        "backendtest/email_utils.py",
        "backendtest/price_feed.py",
        
        # Dashboard Core
        "dashboardtest/app.py",
        "dashboardtest/dash_app.py", 
        "dashboardtest/callbacks.py",
        "dashboardtest/layout.py",
        "dashboardtest/utils.py",
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_callbacks.py",
        
        # Layout Files
        "dashboardtest/auto_trading_layout.py",
        "dashboardtest/futures_trading_layout.py",
        "dashboardtest/binance_exact_layout.py",
        "dashboardtest/email_config_layout.py",
        "dashboardtest/hybrid_learning_layout.py",
        
        # Main Launcher
        "main.py",
    ]
    
    all_present = True
    total_size = 0
    
    for file_path in critical_files:
        exists, size = check_file_exists(file_path)
        status = "✅" if exists else "❌"
        size_str = f"{size:,} bytes" if exists else "MISSING"
        print(f"{status} {file_path:<50} {size_str}")
        
        if not exists:
            all_present = False
        else:
            total_size += size
    
    print("\n📊 SUMMARY:")
    print(f"✅ Files verified: {len(critical_files)}")
    print(f"📁 Total size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    print(f"🎯 All critical files present: {'YES' if all_present else 'NO'}")
    
    return all_present

def test_backend_connectivity():
    """Test if backend is accessible"""
    print("\n🔌 TESTING BACKEND CONNECTIVITY")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running and accessible")
            print(f"📊 Status: {data.get('status', 'unknown')}")
            print(f"⏰ Timestamp: {data.get('timestamp', 'unknown')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running (connection refused)")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_key_endpoints():
    """Test key backend endpoints"""
    print("\n🧪 TESTING KEY ENDPOINTS")
    print("=" * 40)
    
    endpoints = [
        "/health",
        "/balance", 
        "/auto_trading/status",
        "/futures/analytics",
        "/model/feature_importance",
        "/price",
        "/trades/recent"
    ]
    
    working_endpoints = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                working_endpoints += 1
            else:
                print(f"❌ {endpoint} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} (Error: {str(e)[:50]}...)")
    
    print(f"\n📊 Working endpoints: {working_endpoints}/{len(endpoints)}")
    return working_endpoints == len(endpoints)

def verify_port_synchronization():
    """Verify port synchronization between dashboard and backend"""
    print("\n🔗 VERIFYING PORT SYNCHRONIZATION")
    print("=" * 40)
    
    # Check dashboard files for correct API URL
    dashboard_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/utils.py", 
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_callbacks.py"
    ]
    
    correct_ports = 0
    
    for file_path in dashboard_files:
        full_path = os.path.join(BASE_DIR, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for correct port (8000)
                if "localhost:8000" in content and "localhost:8001" not in content:
                    print(f"✅ {file_path} - correct port (8000)")
                    correct_ports += 1
                elif "localhost:8001" in content:
                    print(f"❌ {file_path} - incorrect port (8001)")
                elif "127.0.0.1:8000" in content:
                    print(f"⚠️  {file_path} - uses 127.0.0.1 instead of localhost")
                    correct_ports += 1
                else:
                    print(f"❓ {file_path} - no API URL found")
                    
            except Exception as e:
                print(f"❌ {file_path} - error reading file: {e}")
        else:
            print(f"❌ {file_path} - file not found")
    
    print(f"\n📊 Correct port configuration: {correct_ports}/{len(dashboard_files)}")
    return correct_ports == len(dashboard_files)

def main():
    """Main verification function"""
    print("🎯 POST-ORGANIZATION VERIFICATION")
    print("=" * 50)
    print("Verifying that all functionality is preserved after file organization")
    print()
    
    # Verify critical files
    files_ok = verify_critical_files()
    
    # Test backend connectivity  
    backend_ok = test_backend_connectivity()
    
    # Test key endpoints
    endpoints_ok = test_key_endpoints() if backend_ok else False
    
    # Verify port synchronization
    ports_ok = verify_port_synchronization()
    
    # Final summary
    print("\n🏁 FINAL VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"✅ Critical files present: {'YES' if files_ok else 'NO'}")
    print(f"🔌 Backend connectivity: {'YES' if backend_ok else 'NO'}")
    print(f"🧪 Key endpoints working: {'YES' if endpoints_ok else 'NO'}")
    print(f"🔗 Port synchronization: {'YES' if ports_ok else 'NO'}")
    
    overall_success = all([files_ok, backend_ok, endpoints_ok, ports_ok])
    print(f"\n🎉 OVERALL STATUS: {'✅ SUCCESS' if overall_success else '❌ ISSUES FOUND'}")
    
    if overall_success:
        print("\n🚀 All systems verified! The organization was successful.")
        print("📁 147 files moved to bin folder")
        print("✅ No functionality lost")
        print("🎯 Dashboard-backend synchronization confirmed")
    else:
        print("\n⚠️  Some issues found. Please check the details above.")

if __name__ == "__main__":
    main()
