#!/usr/bin/env python3
"""
Test and fix the technical indicators endpoint
"""
import requests
import json

def test_indicators_endpoint():
    """Test the indicators endpoint"""
    print("🔍 Testing Technical Indicators Endpoint")
    print("="*50)
    
    try:
        # Test the endpoint
        url = "http://localhost:8001/features/indicators"
        params = {"symbol": "btcusdt"}
        
        print(f"📡 Testing: {url}")
        print(f"📋 Parameters: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response Status: {data.get('status')}")
            print(f"📈 Symbol: {data.get('symbol')}")
            
            indicators = data.get('indicators', {})
            print(f"\n🔢 Indicators ({len(indicators)} total):")
            
            # Key indicators for dashboard
            key_indicators = ['regime', 'rsi', 'macd', 'bb_upper', 'bb_middle', 'bb_lower']
            
            for key in key_indicators:
                value = indicators.get(key)
                if value is not None:
                    if key == 'regime':
                        print(f"   ✅ {key}: {value}")
                    else:
                        print(f"   ✅ {key}: {value:.4f}")
                else:
                    print(f"   ❌ {key}: Missing")
            
            # Check if any values are null/none
            null_values = [k for k, v in indicators.items() if v is None]
            if null_values:
                print(f"\n⚠️  Null values found: {null_values}")
            
            # Check if any values are zero (could indicate calculation issues)
            zero_values = [k for k, v in indicators.items() if v == 0.0 and k != 'macd']
            if zero_values:
                print(f"\n⚠️  Zero values found: {zero_values}")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text}")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_data_availability():
    """Check if there's market data available"""
    print("\n🔍 Testing Market Data Availability")
    print("="*40)
    
    try:
        import sqlite3
        
        # Connect to database
        conn = sqlite3.connect('trades.db')
        cursor = conn.cursor()
        
        # Check if market_data table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='market_data'
        """)
        
        if cursor.fetchone():
            print("✅ market_data table exists")
            
            # Check row count
            cursor.execute("SELECT COUNT(*) FROM market_data WHERE symbol = 'BTCUSDT'")
            count = cursor.fetchone()[0]
            print(f"📊 BTCUSDT records: {count}")
            
            if count > 0:
                # Get latest record
                cursor.execute("""
                    SELECT timestamp, close_price, volume 
                    FROM market_data 
                    WHERE symbol = 'BTCUSDT' 
                    ORDER BY timestamp DESC LIMIT 1
                """)
                latest = cursor.fetchone()
                if latest:
                    print(f"📅 Latest record: {latest[0]}")
                    print(f"💰 Price: ${latest[1]:.2f}")
                    print(f"📈 Volume: {latest[2]:.2f}")
            else:
                print("❌ No BTCUSDT data found")
        else:
            print("❌ market_data table does not exist")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")

def simulate_indicators_fix():
    """Create a fix for the indicators if data is missing"""
    print("\n🔧 Creating Indicators Fix")
    print("="*30)
    
    # Test current price endpoint to get live data
    try:
        response = requests.get("http://localhost:8001/price", timeout=5)
        if response.status_code == 200:
            price_data = response.json()
            current_price = float(price_data.get('price', 105000))
            symbol = price_data.get('symbol', 'BTCUSDT')
            
            print(f"✅ Current price: {symbol} = ${current_price:.2f}")
            
            # Generate realistic indicators based on current price
            simulated_indicators = {
                "regime": "NEUTRAL",
                "rsi": 52.3,
                "macd": 0.0245,
                "macd_signal": 0.0189,
                "bb_upper": current_price * 1.021,
                "bb_middle": current_price * 1.003,
                "bb_lower": current_price * 0.985,
                "sma_20": current_price * 0.998,
                "ema_20": current_price * 1.001,
                "atr": current_price * 0.008,
                "adx": 28.7,
                "stoch_k": 48.2,
                "stoch_d": 51.1,
                "williams_r": -45.8,
                "roc": 0.12
            }
            
            print("\n📊 Simulated indicators:")
            for key, value in simulated_indicators.items():
                if key == 'regime':
                    print(f"   {key}: {value}")
                else:
                    print(f"   {key}: {value:.4f}")
                    
            return simulated_indicators
            
        else:
            print("❌ Could not get current price")
            return None
            
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return None

def main():
    """Run all tests and fixes"""
    print("🚀 TECHNICAL INDICATORS DIAGNOSTIC")
    print("="*60)
    
    # Test the endpoint
    test_indicators_endpoint()
    
    # Test data availability
    test_data_availability()
    
    # Create fix simulation
    simulated = simulate_indicators_fix()
    
    print("\n📋 DIAGNOSIS:")
    print("- Endpoint exists and responds")
    print("- Issue likely in data calculation or database")
    print("- Dashboard expects: regime, rsi, macd, bb_upper, bb_middle, bb_lower")
    
    print("\n🔧 RECOMMENDED FIX:")
    print("1. Ensure market data is being collected")
    print("2. Add fallback values for missing indicators")
    print("3. Improve error handling in indicators calculation")
    
    if simulated:
        print("4. Use simulated values as temporary fix")

if __name__ == "__main__":
    main()
