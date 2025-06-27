#!/usr/bin/env python3
"""
Detailed API response analysis for hybrid predictions
"""
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8001"

def analyze_api_response():
    """Analyze the full API response structure"""
    print("🔍 Detailed API Response Analysis")
    print("=" * 50)
    
    symbol = "kaiausdt"
    
    try:
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
        print(f"📡 API Call: GET /ml/hybrid/predict?symbol={symbol}")
        print(f"📊 Status Code: {resp.status_code}")
        print(f"📝 Response Headers: {dict(resp.headers)}")
        print()
        
        if resp.status_code == 200:
            # Get raw text first
            raw_text = resp.text
            print("📄 Raw Response Text:")
            print("-" * 30)
            print(raw_text[:500] + ("..." if len(raw_text) > 500 else ""))
            print()
            
            # Parse JSON
            try:
                data = resp.json()
                print("🗂️  Parsed JSON Structure:")
                print("-" * 30)
                print(json.dumps(data, indent=2))
                print()
                
                # Analyze specific fields
                print("🔍 Field Analysis:")
                print("-" * 30)
                print(f"• Status: {data.get('status')}")
                print(f"• Symbol: {data.get('symbol')}")
                
                # Check prediction structure
                prediction = data.get('prediction', {})
                print(f"• Prediction exists: {prediction is not None}")
                print(f"• Prediction type: {type(prediction)}")
                
                if isinstance(prediction, dict):
                    print(f"• Prediction keys: {list(prediction.keys())}")
                    print(f"• Ensemble prediction: {prediction.get('ensemble_prediction')}")
                    print(f"• Ensemble confidence: {prediction.get('ensemble_confidence')}")
                    print(f"• Timestamp in prediction: {prediction.get('timestamp')}")
                
                # Check root-level timestamp
                print(f"• Root timestamp: {data.get('timestamp')}")
                
                # Check if there are any timestamp-like fields
                def find_timestamp_fields(obj, path=""):
                    """Recursively find all timestamp-like fields"""
                    timestamps = []
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            current_path = f"{path}.{key}" if path else key
                            if 'timestamp' in key.lower() or 'time' in key.lower() or 'date' in key.lower():
                                timestamps.append((current_path, value))
                            if isinstance(value, (dict, list)):
                                timestamps.extend(find_timestamp_fields(value, current_path))
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            current_path = f"{path}[{i}]"
                            if isinstance(item, (dict, list)):
                                timestamps.extend(find_timestamp_fields(item, current_path))
                    return timestamps
                
                all_timestamps = find_timestamp_fields(data)
                print(f"• All timestamp-like fields: {all_timestamps}")
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {e}")
                
        else:
            print(f"❌ API Error: {resp.status_code}")
            print(f"📝 Error Response: {resp.text}")
            
    except Exception as e:
        print(f"❌ Request Exception: {str(e)}")

def test_multiple_calls():
    """Test multiple calls to see if anything changes"""
    print("\n🔄 Multiple API Calls Test")
    print("=" * 50)
    
    symbol = "kaiausdt"
    
    for i in range(3):
        print(f"\n📞 Call #{i+1}:")
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                prediction = data.get('prediction', {})
                
                print(f"  Ensemble pred: {prediction.get('ensemble_prediction')}")
                print(f"  Confidence: {prediction.get('ensemble_confidence', 0):.4f}")
                print(f"  Timestamp: {prediction.get('timestamp')}")
                print(f"  Root timestamp: {data.get('timestamp')}")
                
                # Check if any field has changed
                if i == 0:
                    first_response = data
                else:
                    changes = []
                    if data != first_response:
                        changes.append("response differs")
                    if prediction.get('ensemble_confidence') != first_response.get('prediction', {}).get('ensemble_confidence'):
                        changes.append("confidence changed")
                    if prediction.get('timestamp') != first_response.get('prediction', {}).get('timestamp'):
                        changes.append("timestamp changed")
                    
                    if changes:
                        print(f"  Changes: {', '.join(changes)}")
                    else:
                        print("  No changes detected")
                        
            else:
                print(f"  ❌ Error: {resp.status_code}")
                
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")

if __name__ == "__main__":
    analyze_api_response()
    test_multiple_calls()
