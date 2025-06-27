#!/usr/bin/env python3
"""
Test Enhanced Batch Upload Endpoint
"""
import requests
import csv
import tempfile
import os
import json
from datetime import datetime

API_URL = "http://localhost:8000"

def test_enhanced_batch_upload():
    """Test the enhanced batch upload endpoint with validation and error handling"""
    
    print("🧪 Testing Enhanced Batch Upload Endpoint")
    print("=" * 50)
    
    # Test 1: Valid CSV upload
    print("\n1. Testing valid CSV upload...")
    valid_data = [
        ["timestamp", "symbol", "open", "high", "low", "close", "volume"],
        ["2024-01-01 00:00:00", "BTCUSDT", "42000", "42500", "41800", "42200", "1000"],
        ["2024-01-01 01:00:00", "BTCUSDT", "42200", "42800", "42000", "42600", "1200"],
        ["2024-01-01 02:00:00", "BTCUSDT", "42600", "43000", "42400", "42800", "900"]
    ]
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerows(valid_data)
        valid_csv_path = f.name
    
    try:
        # Test valid upload
        with open(valid_csv_path, 'rb') as f:
            files = {"file": ("test_data.csv", f, "text/csv")}
            response = requests.post(f"{API_URL}/upload_csv", files=files)
            
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful: {result['message']}")
            print(f"   Processed rows: {result.get('processed_rows', 'N/A')}")
            upload_id = result.get('upload_id')
            if upload_id:
                print(f"   Upload ID: {upload_id}")
        else:
            print(f"❌ Upload failed: {response.text}")
            
    finally:
        os.unlink(valid_csv_path)
    
    # Test 2: Invalid file type
    print("\n2. Testing invalid file type...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is not a CSV file")
        invalid_file_path = f.name
    
    try:
        with open(invalid_file_path, 'rb') as f:
            files = {"file": ("test_data.txt", f, "text/plain")}
            response = requests.post(f"{API_URL}/upload_csv", files=files)
            
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            result = response.json()
            print(f"✅ Correctly rejected: {result['detail']}")
        else:
            print(f"❌ Should have been rejected: {response.text}")
            
    finally:
        os.unlink(invalid_file_path)
    
    # Test 3: Invalid CSV structure
    print("\n3. Testing invalid CSV structure...")
    invalid_data = [
        ["wrong", "headers", "in", "csv"],
        ["data1", "data2", "data3", "data4"]
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerows(invalid_data)
        invalid_csv_path = f.name
    
    try:
        with open(invalid_csv_path, 'rb') as f:
            files = {"file": ("invalid_data.csv", f, "text/csv")}
            response = requests.post(f"{API_URL}/upload_csv", files=files)
            
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            result = response.json()
            print(f"✅ Correctly rejected: {result['detail']}")
        else:
            print(f"❌ Should have been rejected: {response.text}")
            
    finally:
        os.unlink(invalid_csv_path)
    
    # Test 4: Test upload status endpoint
    print("\n4. Testing upload status endpoint...")
    if 'upload_id' in locals():
        response = requests.get(f"{API_URL}/upload_status/{upload_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload status retrieved:")
            print(f"   Status: {result['status']}")
            print(f"   Processed: {result.get('processed_rows', 'N/A')}")
            print(f"   Errors: {result.get('error_count', 0)}")
        else:
            print(f"❌ Failed to get status: {response.text}")
    else:
        print("⚠ No upload ID available from previous test")
    
    # Test 5: Large file simulation (size limit)
    print("\n5. Testing file size limit...")
    large_data = [["timestamp", "symbol", "open", "high", "low", "close", "volume"]]
    # Add many rows to exceed 10MB limit
    for i in range(100000):  # This should create a file > 10MB
        large_data.append([
            f"2024-01-01 {i%24:02d}:00:00", "BTCUSDT", 
            "42000", "42500", "41800", "42200", "1000"
        ])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerows(large_data)
        large_csv_path = f.name
    
    try:
        file_size = os.path.getsize(large_csv_path) / (1024*1024)  # Size in MB
        print(f"Generated file size: {file_size:.2f} MB")
        
        with open(large_csv_path, 'rb') as f:
            files = {"file": ("large_data.csv", f, "text/csv")}
            response = requests.post(f"{API_URL}/upload_csv", files=files)
            
        print(f"Status Code: {response.status_code}")
        if response.status_code == 413 or (response.status_code == 400 and "size" in response.text.lower()):
            print(f"✅ Correctly rejected large file")
        elif response.status_code == 200:
            print(f"⚠ Large file was accepted (may be within limit)")
        else:
            print(f"❌ Unexpected response: {response.text}")
            
    finally:
        os.unlink(large_csv_path)
    
    print("\n" + "=" * 50)
    print("✅ Enhanced batch upload testing completed!")

def test_email_endpoints():
    """Test the email configuration endpoints"""
    
    print("\n🧪 Testing Email Configuration Endpoints")
    print("=" * 50)
    
    # Test 1: Get current email config
    print("\n1. Testing get email config...")
    response = requests.get(f"{API_URL}/email/config")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Config retrieved: {result.get('status', 'N/A')}")
        current_config = result.get('config', {})
        print(f"   Enabled: {current_config.get('enabled', False)}")
    else:
        print(f"❌ Failed to get config: {response.text}")
    
    # Test 2: Set email config
    print("\n2. Testing set email config...")
    test_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "test@example.com",
        "smtp_pass": "test_password",
        "from_email": "test@example.com",
        "to_email": "notifications@example.com",
        "enabled": False  # Don't enable for testing
    }
    
    response = requests.post(f"{API_URL}/email/config", json=test_config)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Config saved: {result.get('message', 'N/A')}")
    else:
        print(f"❌ Failed to save config: {response.text}")
    
    # Test 3: Test email connection (should fail with fake credentials)
    print("\n3. Testing email connection...")
    response = requests.post(f"{API_URL}/email/test")
    print(f"Status Code: {response.status_code}")
    result = response.json()
    if result.get('status') == 'error':
        print(f"✅ Connection test correctly failed: {result.get('result', {}).get('message', 'N/A')}")
    else:
        print(f"⚠ Unexpected result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ Email endpoint testing completed!")

if __name__ == "__main__":
    try:
        print("🚀 Starting Enhanced Features Testing")
        test_enhanced_batch_upload()
        test_email_endpoints()
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Please ensure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
