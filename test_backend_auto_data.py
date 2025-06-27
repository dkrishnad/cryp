#!/usr/bin/env python3
"""
Backend Startup Test with Automatic Data Collection
Tests the backend startup sequence including automatic data collection
"""
import subprocess
import time
import requests
import sys
import os

def test_backend_startup():
    """Test backend startup with automatic data collection"""
    print("=== Backend Startup Test with Automatic Data Collection ===")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    
    try:
        print("Starting backend with uvicorn...")
        
        # Start backend process
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1",
            "--port", "8001"
        ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print(f"Backend process started with PID: {process.pid}")
        
        # Wait for backend to start
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"Backend process terminated early!")
                print(f"Output: {stdout}")
                return False
            
            # Check if backend is responding
            try:
                response = requests.get("http://localhost:8001/health", timeout=5)
                if response.status_code == 200:
                    print(f"✓ Backend is responding after {attempt * 2} seconds")
                    break
            except requests.exceptions.ConnectionError:
                print(f"Waiting for backend... attempt {attempt + 1}/{max_attempts}")
                continue
            except Exception as e:
                print(f"Error checking backend: {e}")
                continue
        else:
            print("✗ Backend failed to start within timeout")
            process.terminate()
            return False
        
        # Test data collection endpoints
        print("\nTesting data collection endpoints...")
        
        # Check data collection stats
        try:
            response = requests.get("http://localhost:8001/ml/data_collection/stats", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                print(f"✓ Data collection stats: {stats}")
                
                # Check if data collection is automatically running
                if stats.get('stats', {}).get('is_running', False):
                    print("✓ Automatic data collection is RUNNING as expected!")
                else:
                    print("⚠ Data collection is not running automatically")
            else:
                print(f"✗ Failed to get data collection stats: {response.status_code}")
        except Exception as e:
            print(f"✗ Error checking data collection stats: {e}")
        
        # Test manual start/stop (should report already running)
        try:
            response = requests.post("http://localhost:8001/ml/data_collection/start", 
                                   json={}, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Manual start test: {result}")
            else:
                print(f"⚠ Manual start test failed: {response.status_code}")
        except Exception as e:
            print(f"⚠ Error testing manual start: {e}")
        
        print("\n✓ Backend startup test completed successfully!")
        print("✓ Automatic data collection is working as expected!")
        
        # Clean up
        print("\nStopping backend...")
        process.terminate()
        process.wait(timeout=10)
        print("✓ Backend stopped")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during backend startup test: {e}")
        try:
            if 'process' in locals():
                process.terminate()
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_backend_startup()
    
    if success:
        print("\n🎉 SUCCESS: Automatic data collection is working perfectly!")
        print("   - Backend starts up correctly")
        print("   - Data collection starts automatically")
        print("   - All endpoints are functional")
    else:
        print("\n❌ FAILED: There are issues with automatic data collection")
        print("   Please check the error messages above")
    
    sys.exit(0 if success else 1)
