#!/usr/bin/env python3
"""
Quick test of transfer learning endpoints
"""
import requests
import json

def test_transfer_endpoints():
    """Test the specific transfer learning endpoints that were failing"""
    base_url = "http://localhost:8001"
    
    print("🧪 Testing Transfer Learning Endpoints")
    print("=" * 50)
    
    # Test 1: Train target model
    print("🔄 Testing train_target...")
    try:
        response = requests.post(f"{base_url}/model/crypto_transfer/train_target", 
                               json={"use_recent_data": True, "adaptation_mode": "incremental"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SUCCESS")
        else:
            print(f"   ❌ ERROR: {response.text}")
    except Exception as e:
        print(f"   ❌ CONNECTION ERROR: {e}")
    
    # Test 2: Check retrain needed
    print("🔄 Testing check_retrain_needed...")
    try:
        response = requests.get(f"{base_url}/model/crypto_transfer/check_retrain_needed")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SUCCESS")
        else:
            print(f"   ❌ ERROR: {response.text}")
    except Exception as e:
        print(f"   ❌ CONNECTION ERROR: {e}")
    
    # Test 3: Training schedule
    print("🔄 Testing training_schedule...")
    try:
        response = requests.get(f"{base_url}/model/crypto_transfer/training_schedule")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SUCCESS")
        else:
            print(f"   ❌ ERROR: {response.text}")
    except Exception as e:
        print(f"   ❌ CONNECTION ERROR: {e}")
    
    print("\n🎯 Transfer Learning Test Complete!")

if __name__ == "__main__":
    test_transfer_endpoints()
