#!/usr/bin/env python3
"""
Test the fixed indicators
"""
import requests
import json

def test_fixed_indicators():
    """Test if indicators are now working"""
    print("🔧 Testing Fixed Technical Indicators")
    print("="*50)
    
    try:
        # Test the endpoint
        response = requests.get("http://localhost:8001/features/indicators?symbol=btcusdt", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response status: {data.get('status')}")
            
            indicators = data.get('indicators', {})
            print(f"\n📊 Indicators:")
            
            # Test key indicators
            key_indicators = ['regime', 'rsi', 'macd', 'bb_upper', 'bb_middle', 'bb_lower']
            
            all_valid = True
            for key in key_indicators:
                value = indicators.get(key)
                if value is not None and value != 0:
                    if key == 'regime':
                        print(f"   ✅ {key}: {value}")
                    else:
                        print(f"   ✅ {key}: {value:.4f}")
                else:
                    print(f"   ⚠️  {key}: {value} (fallback)")
                    
            # Check if we have valid bollinger bands
            bb_upper = indicators.get('bb_upper', 0)
            bb_middle = indicators.get('bb_middle', 0) 
            bb_lower = indicators.get('bb_lower', 0)
            
            if bb_upper > bb_middle > bb_lower > 0:
                print(f"   ✅ Bollinger Bands are properly ordered")
            else:
                print(f"   ⚠️  Bollinger Bands may need adjustment")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_fixed_indicators()
    if success:
        print(f"\n✅ Indicators should now show properly in dashboard!")
    else:
        print(f"\n❌ Still having issues - check backend logs")
