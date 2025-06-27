#!/usr/bin/env python3
"""
Quick Multi-Coin Analysis
$1 per coin (5 coins) win probability calculator
"""

import numpy as np
import json
from datetime import datetime

def quick_multi_coin_analysis():
    """Quick analysis of multi-coin strategy"""
    
    print("🚀 MULTI-COIN WIN PROBABILITY ANALYSIS")
    print("="*50)
    
    # Parameters
    initial_per_coin = 1.0  # $1 per coin
    num_coins = 5
    total_initial = initial_per_coin * num_coins  # $5 total
    leverage = 5
    
    coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'KAIAUSDT']
    
    print(f"💰 Investment Structure:")
    print(f"   Per Coin: ${initial_per_coin}")
    print(f"   Number of Coins: {num_coins}")
    print(f"   Total Investment: ${total_initial}")
    print(f"   Leverage: {leverage}x")
    print(f"   Effective Capital: ${total_initial * leverage}")
    print()
    
    # Simulation parameters
    base_accuracy = 0.68  # 68% win rate per coin
    avg_win_return = 0.0045  # 0.45% per win
    avg_loss_return = -0.0030  # -0.30% per loss
    trades_per_day_per_coin = 1440  # 5 trades/minute
    days = 30
    
    # Quick Monte Carlo (simplified)
    num_simulations = 5000
    results = []
    
    print(f"🔄 Running {num_simulations:,} simulations...")
    
    for sim in range(num_simulations):
        portfolio_value = 0
        
        # Simulate each coin
        for coin in coins:
            coin_value = initial_per_coin
            
            # Market correlation effect
            market_factor = np.random.normal(1.0, 0.1)
            coin_accuracy = base_accuracy * market_factor
            coin_accuracy = max(0.55, min(0.85, coin_accuracy))
            
            # Daily compounding simulation
            for day in range(days):
                daily_return = 0
                
                # Simulate trades for the day
                for trade in range(trades_per_day_per_coin):
                    if np.random.random() < coin_accuracy:
                        # Win
                        trade_return = avg_win_return + np.random.normal(0, 0.001)
                    else:
                        # Loss
                        trade_return = avg_loss_return + np.random.normal(0, 0.0005)
                    
                    # Apply leverage
                    leveraged_return = trade_return * leverage
                    daily_return += leveraged_return
                
                # Apply daily return with compounding
                coin_value *= (1 + daily_return)
                
                # Stop loss protection
                if coin_value < initial_per_coin * 0.1:
                    coin_value = initial_per_coin * 0.1
                    break
            
            portfolio_value += coin_value
        
        results.append(portfolio_value)
        
        if sim % 1000 == 0 and sim > 0:
            print(f"   Completed {sim:,} simulations...")
    
    # Analyze results
    results = np.array(results)
    
    # Calculate probabilities
    prob_profit = np.mean(results > total_initial)
    prob_2x = np.mean(results > total_initial * 2)
    prob_3x = np.mean(results > total_initial * 3)
    prob_5x = np.mean(results > total_initial * 5)
    prob_10x = np.mean(results > total_initial * 10)
    prob_20x = np.mean(results > total_initial * 20)
    prob_loss_50 = np.mean(results < total_initial * 0.5)
    prob_loss_90 = np.mean(results < total_initial * 0.1)
    
    # Statistics
    mean_value = np.mean(results)
    median_value = np.median(results)
    std_value = np.std(results)
    min_value = np.min(results)
    max_value = np.max(results)
    
    mean_return = (mean_value - total_initial) / total_initial
    
    # Print results
    print("\n" + "="*50)
    print("📊 ANALYSIS RESULTS")
    print("="*50)
    
    print(f"\n💰 PORTFOLIO PERFORMANCE:")
    print(f"   Expected Final Value: ${mean_value:.2f}")
    print(f"   Median Final Value: ${median_value:.2f}")
    print(f"   Expected Return: {mean_return*100:.1f}%")
    print(f"   Standard Deviation: ${std_value:.2f}")
    print(f"   Best Case: ${max_value:.2f}")
    print(f"   Worst Case: ${min_value:.2f}")
    
    print(f"\n🎯 WIN PROBABILITIES:")
    print(f"   Any Profit: {prob_profit*100:.1f}%")
    print(f"   2x Return ($10+): {prob_2x*100:.1f}%")
    print(f"   3x Return ($15+): {prob_3x*100:.1f}%")
    print(f"   5x Return ($25+): {prob_5x*100:.1f}%")
    print(f"   10x Return ($50+): {prob_10x*100:.1f}%")
    print(f"   20x Return ($100+): {prob_20x*100:.1f}%")
    
    print(f"\n⚠️  RISK ANALYSIS:")
    print(f"   Loss >50%: {prob_loss_50*100:.1f}%")
    print(f"   Loss >90%: {prob_loss_90*100:.1f}%")
    
    # Percentile analysis
    p5 = np.percentile(results, 5)
    p25 = np.percentile(results, 25)
    p50 = np.percentile(results, 50)
    p75 = np.percentile(results, 75)
    p95 = np.percentile(results, 95)
    
    print(f"\n📈 PERCENTILE ANALYSIS:")
    print(f"   5th Percentile: ${p5:.2f}")
    print(f"   25th Percentile: ${p25:.2f}")
    print(f"   50th Percentile: ${p50:.2f}")
    print(f"   75th Percentile: ${p75:.2f}")
    print(f"   95th Percentile: ${p95:.2f}")
    
    # Scenario analysis
    print(f"\n📋 SCENARIO ANALYSIS:")
    
    conservative = p25
    expected = mean_value
    optimistic = p75
    best_case = p95
    
    print(f"   Conservative (25%): ${conservative:.2f} ({((conservative-total_initial)/total_initial)*100:.0f}% return)")
    print(f"   Expected (Mean): ${expected:.2f} ({((expected-total_initial)/total_initial)*100:.0f}% return)")
    print(f"   Optimistic (75%): ${optimistic:.2f} ({((optimistic-total_initial)/total_initial)*100:.0f}% return)")
    print(f"   Best Case (95%): ${best_case:.2f} ({((best_case-total_initial)/total_initial)*100:.0f}% return)")
    
    # Overall verdict
    print(f"\n🚀 OVERALL VERDICT:")
    print(f"   Win Probability: {prob_profit*100:.1f}%")
    
    if prob_profit > 0.85:
        verdict = "EXCELLENT"
        color = "🟢"
    elif prob_profit > 0.75:
        verdict = "VERY GOOD"
        color = "🟡"
    elif prob_profit > 0.65:
        verdict = "GOOD"
        color = "🟠"
    else:
        verdict = "RISKY"
        color = "🔴"
    
    print(f"   Strategy Rating: {color} {verdict}")
    print(f"   Expected Profit: ${mean_value - total_initial:.2f}")
    print(f"   Risk Level: {'LOW' if prob_loss_50 < 0.1 else 'MODERATE' if prob_loss_50 < 0.2 else 'HIGH'}")
    
    print("\n" + "="*50)
    print("✅ Analysis Complete!")
    print("="*50)
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'investment_structure': {
            'per_coin': initial_per_coin,
            'num_coins': num_coins,
            'total_initial': total_initial,
            'leverage': leverage
        },
        'results': {
            'win_probability': prob_profit,
            'expected_value': mean_value,
            'expected_return_pct': mean_return * 100,
            'prob_2x': prob_2x,
            'prob_5x': prob_5x,
            'prob_10x': prob_10x,
            'risk_significant_loss': prob_loss_50
        },
        'verdict': {
            'rating': verdict,
            'win_probability_pct': prob_profit * 100,
            'expected_profit': mean_value - total_initial
        }
    }
    
    with open('multi_coin_analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"💾 Summary saved to: multi_coin_analysis_summary.json")
    
    return summary

if __name__ == "__main__":
    result = quick_multi_coin_analysis()
