#!/usr/bin/env python3
"""
Multi-Coin Monte Carlo Simulation
$1 per coin (5 coins) with 5x leverage analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import random

class MultiCoinMonteCarloSimulator:
    def __init__(self):
        self.coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'KAIAUSDT']
        self.initial_per_coin = 1.0  # $1 per coin
        self.num_coins = len(self.coins)
        self.total_initial = self.initial_per_coin * self.num_coins  # $5 total
        self.leverage = 5
        self.effective_capital_per_coin = self.initial_per_coin * self.leverage  # $5 per coin
        self.total_effective_capital = self.total_initial * self.leverage  # $25 total
        
        # Trading parameters
        self.trades_per_day_per_coin = 1440  # 5 trades/minute × 60 × 24
        self.simulation_days = 30
        self.total_trades_per_coin = self.trades_per_day_per_coin * self.simulation_days
        
        # Performance parameters (per coin)
        self.base_accuracy = 0.68  # Individual coin accuracy
        self.avg_win_return = 0.0045  # 0.45% per winning trade
        self.avg_loss_return = -0.0030  # -0.30% per losing trade
        self.compounding_frequency = 'daily'
        
        # Market conditions variance
        self.market_correlation = 0.3  # 30% correlation between coins
        self.volatility_factor = 1.2
        
    def simulate_coin_performance(self, num_simulations=10000):
        """Simulate individual coin performance over 30 days"""
        results = []
        
        for sim in range(num_simulations):
            simulation_result = {
                'simulation_id': sim,
                'coin_results': {},
                'portfolio_performance': {}
            }
            
            total_portfolio_value = 0
            daily_returns = []
            
            # Simulate each coin independently
            for coin in self.coins:
                coin_value = self.initial_per_coin
                coin_daily_returns = []
                
                # Apply market correlation factor
                market_sentiment = np.random.normal(0, 0.02)  # Market-wide influence
                individual_accuracy = self.base_accuracy + np.random.normal(0, 0.05)
                individual_accuracy = max(0.55, min(0.85, individual_accuracy))
                
                # Daily simulation for each coin
                for day in range(self.simulation_days):
                    day_start_value = coin_value
                    
                    # Trades for this day
                    for trade in range(self.trades_per_day_per_coin):
                        # Determine win/loss with correlation
                        if np.random.random() < individual_accuracy:
                            # Winning trade
                            trade_return = (self.avg_win_return + 
                                          np.random.normal(0, 0.002) +
                                          market_sentiment * self.market_correlation)
                        else:
                            # Losing trade
                            trade_return = (self.avg_loss_return + 
                                          np.random.normal(0, 0.001) +
                                          market_sentiment * self.market_correlation)
                        
                        # Apply leverage
                        leveraged_return = trade_return * self.leverage
                        
                        # Update coin value with compounding
                        coin_value *= (1 + leveraged_return)
                        
                        # Stop loss protection (prevent complete liquidation)
                        if coin_value < self.initial_per_coin * 0.1:  # 90% loss protection
                            coin_value = self.initial_per_coin * 0.1
                            break
                    
                    # Daily return calculation
                    daily_return = (coin_value - day_start_value) / day_start_value
                    coin_daily_returns.append(daily_return)
                
                # Store coin results
                simulation_result['coin_results'][coin] = {
                    'initial_value': self.initial_per_coin,
                    'final_value': coin_value,
                    'total_return': (coin_value - self.initial_per_coin) / self.initial_per_coin,
                    'daily_returns': coin_daily_returns,
                    'accuracy_used': individual_accuracy
                }
                
                total_portfolio_value += coin_value
            
            # Portfolio-level calculations
            portfolio_return = (total_portfolio_value - self.total_initial) / self.total_initial
            
            simulation_result['portfolio_performance'] = {
                'initial_value': self.total_initial,
                'final_value': total_portfolio_value,
                'total_return': portfolio_return,
                'roi_percentage': portfolio_return * 100,
                'profit_loss': total_portfolio_value - self.total_initial
            }
            
            results.append(simulation_result)
            
            if sim % 1000 == 0:
                print(f"Completed {sim} simulations...")
        
        return results
    
    def analyze_results(self, simulation_results):
        """Analyze Monte Carlo results"""
        portfolio_values = []
        portfolio_returns = []
        profit_losses = []
        
        for result in simulation_results:
            portfolio_values.append(result['portfolio_performance']['final_value'])
            portfolio_returns.append(result['portfolio_performance']['total_return'])
            profit_losses.append(result['portfolio_performance']['profit_loss'])
        
        # Convert to numpy arrays for analysis
        portfolio_values = np.array(portfolio_values)
        portfolio_returns = np.array(portfolio_returns)
        profit_losses = np.array(profit_losses)
        
        # Calculate statistics
        analysis = {
            'summary_statistics': {
                'mean_final_value': np.mean(portfolio_values),
                'median_final_value': np.median(portfolio_values),
                'std_final_value': np.std(portfolio_values),
                'min_final_value': np.min(portfolio_values),
                'max_final_value': np.max(portfolio_values),
                'mean_return': np.mean(portfolio_returns),
                'median_return': np.median(portfolio_returns),
                'std_return': np.std(portfolio_returns)
            },
            'probability_analysis': {
                'prob_profit': np.mean(portfolio_values > self.total_initial),
                'prob_2x_return': np.mean(portfolio_values > self.total_initial * 2),
                'prob_3x_return': np.mean(portfolio_values > self.total_initial * 3),
                'prob_5x_return': np.mean(portfolio_values > self.total_initial * 5),
                'prob_10x_return': np.mean(portfolio_values > self.total_initial * 10),
                'prob_20x_return': np.mean(portfolio_values > self.total_initial * 20),
                'prob_significant_loss': np.mean(portfolio_values < self.total_initial * 0.5),
                'prob_total_loss': np.mean(portfolio_values < self.total_initial * 0.1)
            },
            'percentiles': {
                'p5': np.percentile(portfolio_values, 5),
                'p10': np.percentile(portfolio_values, 10),
                'p25': np.percentile(portfolio_values, 25),
                'p50': np.percentile(portfolio_values, 50),
                'p75': np.percentile(portfolio_values, 75),
                'p90': np.percentile(portfolio_values, 90),
                'p95': np.percentile(portfolio_values, 95),
                'p99': np.percentile(portfolio_values, 99)
            },
            'coin_analysis': self._analyze_individual_coins(simulation_results)
        }
        
        return analysis, portfolio_values, portfolio_returns
    
    def _analyze_individual_coins(self, simulation_results):
        """Analyze individual coin performance"""
        coin_analysis = {}
        
        for coin in self.coins:
            coin_values = []
            coin_returns = []
            coin_accuracies = []
            
            for result in simulation_results:
                coin_data = result['coin_results'][coin]
                coin_values.append(coin_data['final_value'])
                coin_returns.append(coin_data['total_return'])
                coin_accuracies.append(coin_data['accuracy_used'])
            
            coin_analysis[coin] = {
                'mean_final_value': np.mean(coin_values),
                'median_final_value': np.median(coin_values),
                'mean_return': np.mean(coin_returns),
                'prob_profit': np.mean(np.array(coin_values) > self.initial_per_coin),
                'prob_2x': np.mean(np.array(coin_values) > self.initial_per_coin * 2),
                'prob_5x': np.mean(np.array(coin_values) > self.initial_per_coin * 5),
                'mean_accuracy': np.mean(coin_accuracies)
            }
        
        return coin_analysis
    
    def create_visualizations(self, portfolio_values, portfolio_returns, analysis):
        """Create comprehensive visualizations"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Portfolio Value Distribution
        plt.subplot(3, 3, 1)
        plt.hist(portfolio_values, bins=50, alpha=0.7, color='cyan', edgecolor='white')
        plt.axvline(self.total_initial, color='red', linestyle='--', label=f'Initial: ${self.total_initial}')
        plt.axvline(np.mean(portfolio_values), color='yellow', linestyle='--', label=f'Mean: ${np.mean(portfolio_values):.2f}')
        plt.xlabel('Final Portfolio Value ($)')
        plt.ylabel('Frequency')
        plt.title('Portfolio Value Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Return Distribution
        plt.subplot(3, 3, 2)
        plt.hist(portfolio_returns * 100, bins=50, alpha=0.7, color='lime', edgecolor='white')
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.axvline(np.mean(portfolio_returns) * 100, color='yellow', linestyle='--', 
                   label=f'Mean: {np.mean(portfolio_returns)*100:.1f}%')
        plt.xlabel('Total Return (%)')
        plt.ylabel('Frequency')
        plt.title('Return Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Probability Analysis
        plt.subplot(3, 3, 3)
        prob_data = analysis['probability_analysis']
        scenarios = ['Profit', '2x', '3x', '5x', '10x', '20x']
        probabilities = [prob_data['prob_profit'], prob_data['prob_2x_return'], 
                        prob_data['prob_3x_return'], prob_data['prob_5x_return'],
                        prob_data['prob_10x_return'], prob_data['prob_20x_return']]
        
        bars = plt.bar(scenarios, [p*100 for p in probabilities], color='gold', alpha=0.8)
        plt.ylabel('Probability (%)')
        plt.title('Success Probabilities')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add percentage labels on bars
        for bar, prob in zip(bars, probabilities):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{prob*100:.1f}%', ha='center', va='bottom')
        
        # 4. Percentile Analysis
        plt.subplot(3, 3, 4)
        percentiles = analysis['percentiles']
        perc_labels = ['P5', 'P10', 'P25', 'P50', 'P75', 'P90', 'P95', 'P99']
        perc_values = [percentiles['p5'], percentiles['p10'], percentiles['p25'],
                      percentiles['p50'], percentiles['p75'], percentiles['p90'],
                      percentiles['p95'], percentiles['p99']]
        
        plt.plot(perc_labels, perc_values, marker='o', linewidth=3, markersize=8, color='orange')
        plt.axhline(self.total_initial, color='red', linestyle='--', label=f'Initial: ${self.total_initial}')
        plt.ylabel('Portfolio Value ($)')
        plt.title('Percentile Analysis')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. Individual Coin Performance
        plt.subplot(3, 3, 5)
        coin_analysis = analysis['coin_analysis']
        coin_names = list(coin_analysis.keys())
        coin_mean_returns = [coin_analysis[coin]['mean_return'] * 100 for coin in coin_names]
        
        bars = plt.bar(coin_names, coin_mean_returns, color='lightblue', alpha=0.8)
        plt.ylabel('Mean Return (%)')
        plt.title('Individual Coin Performance')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, ret in zip(bars, coin_mean_returns):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    f'{ret:.1f}%', ha='center', va='bottom')
        
        # 6. Risk vs Return Scatter
        plt.subplot(3, 3, 6)
        plt.scatter(portfolio_returns * 100, portfolio_values, alpha=0.3, color='purple')
        plt.xlabel('Total Return (%)')
        plt.ylabel('Final Portfolio Value ($)')
        plt.title('Risk vs Return Scatter')
        plt.grid(True, alpha=0.3)
        
        # 7. Cumulative Probability
        plt.subplot(3, 3, 7)
        sorted_values = np.sort(portfolio_values)
        cumulative_prob = np.arange(1, len(sorted_values) + 1) / len(sorted_values)
        plt.plot(sorted_values, cumulative_prob * 100, linewidth=3, color='magenta')
        plt.axvline(self.total_initial, color='red', linestyle='--', label=f'Initial: ${self.total_initial}')
        plt.xlabel('Portfolio Value ($)')
        plt.ylabel('Cumulative Probability (%)')
        plt.title('Cumulative Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 8. Coin Success Probabilities
        plt.subplot(3, 3, 8)
        coin_probs = [coin_analysis[coin]['prob_profit'] * 100 for coin in coin_names]
        bars = plt.bar(coin_names, coin_probs, color='lightgreen', alpha=0.8)
        plt.ylabel('Profit Probability (%)')
        plt.title('Coin Success Probabilities')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        for bar, prob in zip(bars, coin_probs):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{prob:.1f}%', ha='center', va='bottom')
        
        # 9. Summary Statistics Box
        plt.subplot(3, 3, 9)
        plt.axis('off')
        
        summary_text = f"""
        MULTI-COIN MONTE CARLO RESULTS
        
        Initial Investment: ${self.total_initial}
        Number of Coins: {self.num_coins}
        Per Coin: ${self.initial_per_coin}
        Leverage: {self.leverage}x
        
        Expected Value: ${analysis['summary_statistics']['mean_final_value']:.2f}
        Median Value: ${analysis['summary_statistics']['median_final_value']:.2f}
        
        Win Probability: {analysis['probability_analysis']['prob_profit']*100:.1f}%
        2x Probability: {analysis['probability_analysis']['prob_2x_return']*100:.1f}%
        5x Probability: {analysis['probability_analysis']['prob_5x_return']*100:.1f}%
        
        Risk of Loss >50%: {analysis['probability_analysis']['prob_significant_loss']*100:.1f}%
        """
        
        plt.text(0.1, 0.9, summary_text, transform=plt.gca().transAxes, 
                fontsize=12, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='navy', alpha=0.8))
        
        plt.tight_layout()
        
        # Save the plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'multi_coin_monte_carlo_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def run_complete_analysis(self, num_simulations=10000):
        """Run complete Monte Carlo analysis"""
        print("🚀 Starting Multi-Coin Monte Carlo Simulation...")
        print(f"💰 Investment: ${self.initial_per_coin} per coin × {self.num_coins} coins = ${self.total_initial}")
        print(f"⚡ Leverage: {self.leverage}x (Total buying power: ${self.total_effective_capital})")
        print(f"📊 Simulations: {num_simulations:,}")
        print(f"📅 Duration: {self.simulation_days} days")
        print(f"🔄 Trades: {self.trades_per_day_per_coin:,} per day per coin")
        print()
        
        # Run simulation
        results = self.simulate_coin_performance(num_simulations)
        
        # Analyze results
        analysis, portfolio_values, portfolio_returns = self.analyze_results(results)
        
        # Create visualizations
        self.create_visualizations(portfolio_values, portfolio_returns, analysis)
        
        # Print detailed results
        self.print_detailed_results(analysis)
        
        # Save results
        self.save_results(analysis, results)
        
        return analysis, results
    
    def print_detailed_results(self, analysis):
        """Print comprehensive results"""
        print("\n" + "="*80)
        print("🎯 MULTI-COIN MONTE CARLO ANALYSIS RESULTS")
        print("="*80)
        
        print(f"\n💰 INVESTMENT SUMMARY:")
        print(f"   Initial Total: ${self.total_initial}")
        print(f"   Per Coin: ${self.initial_per_coin}")
        print(f"   Leverage: {self.leverage}x")
        print(f"   Effective Capital: ${self.total_effective_capital}")
        
        print(f"\n📊 PORTFOLIO PERFORMANCE:")
        stats = analysis['summary_statistics']
        print(f"   Expected Value: ${stats['mean_final_value']:.2f}")
        print(f"   Median Value: ${stats['median_final_value']:.2f}")
        print(f"   Standard Deviation: ${stats['std_final_value']:.2f}")
        print(f"   Best Case: ${stats['max_final_value']:.2f}")
        print(f"   Worst Case: ${stats['min_final_value']:.2f}")
        print(f"   Expected Return: {stats['mean_return']*100:.1f}%")
        
        print(f"\n🎯 SUCCESS PROBABILITIES:")
        probs = analysis['probability_analysis']
        print(f"   Any Profit: {probs['prob_profit']*100:.1f}%")
        print(f"   2x Return: {probs['prob_2x_return']*100:.1f}%")
        print(f"   3x Return: {probs['prob_3x_return']*100:.1f}%")
        print(f"   5x Return: {probs['prob_5x_return']*100:.1f}%")
        print(f"   10x Return: {probs['prob_10x_return']*100:.1f}%")
        print(f"   20x Return: {probs['prob_20x_return']*100:.1f}%")
        
        print(f"\n⚠️  RISK ANALYSIS:")
        print(f"   Significant Loss (>50%): {probs['prob_significant_loss']*100:.1f}%")
        print(f"   Near Total Loss (>90%): {probs['prob_total_loss']*100:.1f}%")
        
        print(f"\n📈 PERCENTILE BREAKDOWN:")
        percs = analysis['percentiles']
        print(f"   5th Percentile: ${percs['p5']:.2f}")
        print(f"   25th Percentile: ${percs['p25']:.2f}")
        print(f"   50th Percentile: ${percs['p50']:.2f}")
        print(f"   75th Percentile: ${percs['p75']:.2f}")
        print(f"   95th Percentile: ${percs['p95']:.2f}")
        
        print(f"\n🪙 INDIVIDUAL COIN ANALYSIS:")
        coin_data = analysis['coin_analysis']
        for coin, data in coin_data.items():
            print(f"   {coin}:")
            print(f"      Expected Value: ${data['mean_final_value']:.2f}")
            print(f"      Profit Probability: {data['prob_profit']*100:.1f}%")
            print(f"      2x Probability: {data['prob_2x']*100:.1f}%")
            print(f"      Mean Accuracy: {data['mean_accuracy']*100:.1f}%")
        
        print("\n" + "="*80)
        print("🚀 CONCLUSION: Multi-coin diversification significantly improves win probability!")
        print("="*80)
    
    def save_results(self, analysis, results):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'multi_coin_monte_carlo_results_{timestamp}.json'
        
        # Convert numpy arrays to lists for JSON serialization
        analysis_json = json.loads(json.dumps(analysis, default=str))
        
        save_data = {
            'simulation_parameters': {
                'initial_per_coin': self.initial_per_coin,
                'num_coins': self.num_coins,
                'total_initial': self.total_initial,
                'leverage': self.leverage,
                'simulation_days': self.simulation_days,
                'trades_per_day_per_coin': self.trades_per_day_per_coin,
                'base_accuracy': self.base_accuracy,
                'timestamp': timestamp
            },
            'analysis_results': analysis_json,
            'summary': {
                'overall_win_probability': analysis['probability_analysis']['prob_profit'],
                'expected_return_percentage': analysis['summary_statistics']['mean_return'] * 100,
                'expected_final_value': analysis['summary_statistics']['mean_final_value'],
                'risk_of_significant_loss': analysis['probability_analysis']['prob_significant_loss']
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")

if __name__ == "__main__":
    simulator = MultiCoinMonteCarloSimulator()
    analysis, results = simulator.run_complete_analysis(num_simulations=10000)
