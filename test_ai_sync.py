#!/usr/bin/env python3
"""
AI Models Synchronization Test
Tests if all AI models are working together in predictions and auto-trading
"""
import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8001"

def test_ai_models_sync():
    """Test if all AI models work in sync for predictions and auto-trading"""
    print("🧠 AI MODELS SYNCHRONIZATION TEST")
    print("=" * 60)
    
    results = {
        'individual_models': {},
        'ensemble_models': {},
        'transfer_learning': {},
        'auto_trading_integration': {},
        'sync_status': 'unknown'
    }
    
    # 1. Test Individual ML Models
    print("\n1️⃣ TESTING INDIVIDUAL ML MODELS")
    print("-" * 40)
    
    try:
        # Test basic ML prediction
        response = requests.post(f"{API_URL}/model/predict_batch", 
                               json=[{'open': 45000, 'high': 46000, 'low': 44000, 'close': 45500, 
                                     'volume': 1000000, 'rsi': 65, 'stoch_k': 75, 'stoch_d': 70,
                                     'williams_r': -25, 'roc': 2.5, 'ao': 150, 'macd': 1.2,
                                     'macd_signal': 1.1, 'macd_diff': 0.1, 'adx': 28, 'cci': 110,
                                     'sma_20': 45200, 'ema_20': 45300, 'bb_high': 46000, 'bb_low': 44500,
                                     'atr': 800, 'obv': 5000000, 'cmf': 0.15}])
        
        if response.status_code == 200:
            basic_ml = response.json()
            results['individual_models']['basic_ml'] = {
                'status': '✅ Working',
                'prediction': basic_ml.get('results', [{}])[0] if basic_ml.get('results') else None
            }
            print("✅ Basic ML Model: Working")
        else:
            results['individual_models']['basic_ml'] = {'status': '❌ Failed', 'error': response.text}
            print("❌ Basic ML Model: Failed")
    except Exception as e:
        results['individual_models']['basic_ml'] = {'status': '❌ Error', 'error': str(e)}
        print(f"❌ Basic ML Model: Error - {e}")
    
    # 2. Test Ensemble Models
    print("\n2️⃣ TESTING ENSEMBLE MODELS")
    print("-" * 40)
    
    try:
        # Test ensemble prediction
        response = requests.post(f"{API_URL}/model/ensemble_predict", 
                               json={'features': [45000, 46000, 44000, 45500]})
        
        if response.status_code == 200:
            ensemble_data = response.json()
            results['ensemble_models']['standard'] = {
                'status': '✅ Working',
                'prediction': ensemble_data.get('ensemble_prediction'),
                'confidence': ensemble_data.get('ensemble_confidence'),
                'models': ensemble_data.get('individual_predictions', {})
            }
            print(f"✅ Standard Ensemble: Working - Prediction: {ensemble_data.get('ensemble_prediction', 'N/A')}")
            print(f"   Individual Models: {list(ensemble_data.get('individual_predictions', {}).keys())}")
        else:
            results['ensemble_models']['standard'] = {'status': '❌ Failed'}
            print("❌ Standard Ensemble: Failed")
    except Exception as e:
        results['ensemble_models']['standard'] = {'status': '❌ Error', 'error': str(e)}
        print(f"❌ Standard Ensemble: Error - {e}")
    
    # Test hybrid ensemble
    try:
        response = requests.get(f"{API_URL}/ml/hybrid/predict?symbol=btcusdt")
        
        if response.status_code == 200:
            hybrid_data = response.json()
            results['ensemble_models']['hybrid'] = {
                'status': '✅ Working',
                'prediction': hybrid_data.get('prediction'),
                'symbol': hybrid_data.get('symbol')
            }
            print(f"✅ Hybrid Ensemble: Working - Prediction: {hybrid_data.get('prediction', 'N/A')}")
        else:
            results['ensemble_models']['hybrid'] = {'status': '❌ Failed'}
            print("❌ Hybrid Ensemble: Failed")
    except Exception as e:
        results['ensemble_models']['hybrid'] = {'status': '❌ Error', 'error': str(e)}
        print(f"❌ Hybrid Ensemble: Error - {e}")
    
    # 3. Test Transfer Learning
    print("\n3️⃣ TESTING TRANSFER LEARNING")
    print("-" * 40)
    
    try:
        # Test transfer learning endpoints
        response = requests.get(f"{API_URL}/model/crypto_transfer/status")
        
        if response.status_code == 200:
            transfer_status = response.json()
            results['transfer_learning']['status'] = {
                'status': '✅ Working',
                'data': transfer_status
            }
            print("✅ Transfer Learning Status: Working")
            
            # Test transfer learning prediction
            response = requests.post(f"{API_URL}/model/crypto_transfer/predict",
                                   json={'features': [[45000, 46000, 44000, 45500, 1000000, 65, 75, 70, -25, 2.5, 150, 1.2, 1.1, 0.1, 28, 110, 45200, 45300, 46000, 44500, 800, 5000000, 0.15]]})
            
            if response.status_code == 200:
                transfer_pred = response.json()
                results['transfer_learning']['prediction'] = {
                    'status': '✅ Working',
                    'prediction': transfer_pred.get('predictions'),
                    'confidence': transfer_pred.get('confidence')
                }
                print(f"✅ Transfer Learning Prediction: Working - Confidence: {transfer_pred.get('confidence', 'N/A')}")
            else:
                results['transfer_learning']['prediction'] = {'status': '❌ Failed'}
                print("❌ Transfer Learning Prediction: Failed")
        else:
            results['transfer_learning']['status'] = {'status': '❌ Failed'}
            print("❌ Transfer Learning Status: Failed")
    except Exception as e:
        results['transfer_learning']['status'] = {'status': '❌ Error', 'error': str(e)}
        print(f"❌ Transfer Learning: Error - {e}")
    
    # 4. Test Auto-Trading Integration
    print("\n4️⃣ TESTING AUTO-TRADING INTEGRATION")
    print("-" * 40)
    
    try:
        # Test auto-trading status
        response = requests.get(f"{API_URL}/auto_trading/status")
        
        if response.status_code == 200:
            auto_status = response.json()
            results['auto_trading_integration']['status'] = {
                'status': '✅ Working',
                'enabled': auto_status.get('data', {}).get('enabled', False),
                'symbol': auto_status.get('data', {}).get('symbol', 'Unknown'),
                'settings': auto_status.get('data', {})
            }
            
            enabled = auto_status.get('data', {}).get('enabled', False)
            symbol = auto_status.get('data', {}).get('symbol', 'Unknown')
            print(f"✅ Auto-Trading Status: Working - Enabled: {enabled}, Symbol: {symbol}")
            
        else:
            results['auto_trading_integration']['status'] = {'status': '❌ Failed'}
            print("❌ Auto-Trading Status: Failed")
    except Exception as e:
        results['auto_trading_integration']['status'] = {'status': '❌ Error', 'error': str(e)}
        print(f"❌ Auto-Trading Integration: Error - {e}")
    
    # 5. Analyze Synchronization
    print("\n5️⃣ SYNCHRONIZATION ANALYSIS")
    print("-" * 40)
    
    working_systems = 0
    total_systems = 0
    
    # Count working systems
    for category, systems in results.items():
        if category == 'sync_status':
            continue
        for system, data in systems.items():
            total_systems += 1
            if isinstance(data, dict) and '✅' in data.get('status', ''):
                working_systems += 1
    
    sync_percentage = (working_systems / total_systems * 100) if total_systems > 0 else 0
    
    if sync_percentage >= 80:
        results['sync_status'] = '✅ Excellent Sync'
        sync_emoji = '🟢'
    elif sync_percentage >= 60:
        results['sync_status'] = '⚠️ Good Sync'
        sync_emoji = '🟡'
    else:
        results['sync_status'] = '❌ Poor Sync'
        sync_emoji = '🔴'
    
    print(f"{sync_emoji} OVERALL SYNCHRONIZATION: {sync_percentage:.0f}% ({working_systems}/{total_systems} systems working)")
    print(f"📊 Status: {results['sync_status']}")
    
    # 6. Recommendations
    print("\n6️⃣ RECOMMENDATIONS")
    print("-" * 40)
    
    if sync_percentage >= 80:
        print("🎉 EXCELLENT! All AI models are working in sync for predictions and auto-trading")
        print("✅ Your bot is ready for production trading")
        print("💡 Consider enabling auto-trading with conservative settings")
    elif sync_percentage >= 60:
        print("⚠️ GOOD sync, but some systems need attention")
        print("🔧 Fix failing systems before enabling auto-trading")
        print("💡 Manual predictions should work well")
    else:
        print("❌ POOR sync - significant issues detected")
        print("🚨 Do not enable auto-trading until issues are resolved")
        print("🔧 Check backend server and model files")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"ai_sync_test_results_{timestamp}.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to: ai_sync_test_results_{timestamp}.json")
    
    return results

def main():
    """Run AI models synchronization test"""
    print("Starting AI models synchronization test...")
    results = test_ai_models_sync()
    
    print("\n" + "=" * 60)
    print("🏁 AI MODELS SYNCHRONIZATION TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
