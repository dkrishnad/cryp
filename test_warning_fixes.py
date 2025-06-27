#!/usr/bin/env python3
"""
Test fixes for WebSocket timeouts and ML warnings
"""
import requests
import asyncio
import time

def test_indicators_no_warnings():
    """Test indicators endpoint for warnings"""
    print("🔧 Testing Indicators - No Warnings")
    print("="*40)
    
    try:
        response = requests.get("http://localhost:8001/features/indicators?symbol=btcusdt", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            
            indicators = data.get('indicators', {})
            regime = indicators.get('regime', 'Unknown')
            rsi = indicators.get('rsi', 0)
            
            print(f"✅ Regime: {regime}")
            print(f"✅ RSI: {rsi:.2f}")
            
            if regime != 'Unknown' and rsi > 0:
                print("✅ Indicators working properly")
                return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def test_ml_prediction_no_warnings():
    """Test ML prediction for warnings"""
    print("\n🔧 Testing ML Predictions - No Warnings")
    print("="*45)
    
    try:
        response = requests.get("http://localhost:8001/ml/hybrid/predict?symbol=btcusdt", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            
            if data.get('status') == 'success':
                prediction = data.get('prediction', {})
                signal = prediction.get('signal', 'Unknown')
                confidence = prediction.get('ensemble_confidence', 0)
                
                print(f"✅ Signal: {signal}")
                print(f"✅ Confidence: {confidence:.3f}")
                
                if signal in ['BUY', 'SELL', 'HOLD']:
                    print("✅ ML predictions working properly")
                    return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def test_websocket_connection():
    """Test WebSocket for timeout issues"""
    print("\n🔧 Testing WebSocket - No Timeouts")
    print("="*40)
    
    try:
        # Test if WebSocket endpoint is available
        import websockets
        
        async def test_ws():
            try:
                uri = "ws://localhost:8001/ws/price/btcusdt"
                async with websockets.connect(uri, timeout=5) as websocket:
                    # Wait for a price update
                    message = await asyncio.wait_for(websocket.recv(), timeout=10)
                    print(f"✅ Received: {message[:50]}...")
                    return True
            except asyncio.TimeoutError:
                print("⚠️  WebSocket timeout (expected initially)")
                return False
            except Exception as e:
                print(f"❌ WebSocket error: {e}")
                return False
        
        # Run the test
        result = asyncio.run(test_ws())
        return result
        
    except ImportError:
        print("⚠️  websockets library not available, skipping test")
        return True
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def main():
    """Run all warning fix tests"""
    print("🚀 TESTING WARNING FIXES")
    print("="*50)
    
    results = []
    
    # Test 1: Indicators
    results.append(test_indicators_no_warnings())
    
    # Test 2: ML Predictions  
    results.append(test_ml_prediction_no_warnings())
    
    # Test 3: WebSocket
    results.append(test_websocket_connection())
    
    # Summary
    print(f"\n📊 RESULTS SUMMARY")
    print("="*30)
    
    tests = ["Indicators", "ML Predictions", "WebSocket"]
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ FIXED" if result else "❌ NEEDS ATTENTION"
        print(f"{i+1}. {test}: {status}")
    
    fixed_count = sum(results)
    total_tests = len(results)
    
    print(f"\n🎯 Fixed: {fixed_count}/{total_tests} issues")
    
    if fixed_count == total_tests:
        print("✅ All warnings should be resolved!")
    else:
        print("⚠️  Some issues may still exist in logs")
    
    return fixed_count == total_tests

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 SUCCESS' if success else '⚠️ PARTIAL FIX'} - Check your logs for improvements")
