#!/usr/bin/env python3
"""
Complete Transfer Learning Backtesting Suite with Visualizations
Comprehensive testing and validation of the crypto trading bot's transfer learning capabilities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advanced_backtest_transfer_learning import TransferLearningBacktester
from backtest_visualizer import create_visualizations
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def run_complete_backtest():
    """Run complete backtesting suite with visualizations"""
    print("🚀 COMPLETE TRANSFER LEARNING BACKTESTING SUITE")
    print("="*70)
    print("📊 Testing crypto trading bot's transfer learning improvements")
    print("🎯 Validating enhanced accuracy on historical KAIA data")
    print()
    
    try:
        # Initialize backtester
        print("🔧 Initializing backtesting system...")
        backtester = TransferLearningBacktester()
        
        # Load and prepare data
        print("📁 Loading historical data...")
        if not backtester.load_data():
            print("❌ Failed to load data. Please check the data path.")
            return False
        
        # Run baseline tests
        print("🧪 Running baseline model tests...")
        backtester.test_baseline_performance()
        
        # Run transfer learning tests
        print("🚀 Running transfer learning tests...")
        backtester.test_transfer_learning_performance()
        
        # Calculate trading performance
        print("💰 Calculating trading performance...")
        backtester.calculate_trading_performance()
        
        # Generate comprehensive report
        print("📋 Generating comprehensive report...")
        report = backtester.generate_comprehensive_report()
        
        # Save results
        print("💾 Saving results...")
        backtester.save_results()
        
        # Create visualizations
        print("📊 Creating visualizations...")
        try:
            create_visualizations(backtester)
        except Exception as e:
            print(f"⚠️  Visualization error: {e}")
            print("   Results are still available in text format")
        
        # Final summary
        print("\n" + "="*70)
        print("🎉 BACKTESTING COMPLETE!")
        print("="*70)
        
        # Quick summary
        accuracy_improvement = (backtester.transfer_results['test_accuracy'] - 
                              backtester.baseline_results['test_accuracy']) * 100
        return_improvement = (backtester.trading_performance['transfer']['total_return'] - 
                            backtester.trading_performance['baseline']['total_return']) * 100
        
        print(f"📈 Key Results:")
        print(f"   • Accuracy improvement: +{accuracy_improvement:.1f} percentage points")
        print(f"   • Trading return improvement: +{return_improvement:.1f}%")
        print(f"   • Transfer learning confidence: {backtester.transfer_results.get('avg_confidence', 0.5)*100:.0f}%")
        print()
        print("📁 Files generated:")
        print("   • Detailed JSON results file")
        print("   • Performance comparison charts")
        print("   • Prediction analysis visualizations")
        print("   • Improvement summary graphics")
        print()
        print("✅ Transfer learning validation complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during backtesting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_complete_backtest()
    if success:
        print("\n🏆 Backtesting suite executed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Backtesting suite failed!")
        sys.exit(1)
