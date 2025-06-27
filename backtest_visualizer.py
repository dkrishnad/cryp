#!/usr/bin/env python3
"""
Advanced Backtesting Visualization System
Creates comprehensive charts and plots for transfer learning validation
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BacktestVisualizer:
    """
    Creates comprehensive visualizations for backtesting results
    """
    
    def __init__(self, backtester):
        self.backtester = backtester
        self.setup_style()
    
    def setup_style(self):
        """Setup plotting style"""
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def create_performance_comparison_chart(self):
        """Create performance comparison chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Accuracy Comparison
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        baseline_scores = [
            self.backtester.baseline_results['test_accuracy'],
            self.backtester.baseline_results['precision'],
            self.backtester.baseline_results['recall'],
            self.backtester.baseline_results['f1']
        ]
        transfer_scores = [
            self.backtester.transfer_results['test_accuracy'],
            self.backtester.transfer_results['precision'],
            self.backtester.transfer_results['recall'],
            self.backtester.transfer_results['f1']
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, baseline_scores, width, label='Baseline', alpha=0.8)
        bars2 = ax1.bar(x + width/2, transfer_scores, width, label='Transfer Learning', alpha=0.8)
        
        ax1.set_xlabel('Metrics')
        ax1.set_ylabel('Score')
        ax1.set_title('Model Performance Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.set_ylim(0, 1)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height:.3f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        # 2. Cumulative Returns
        dates = pd.to_datetime(self.backtester.baseline_results['test_dates'])
        baseline_cumret = self.backtester.trading_performance['baseline']['cumulative_returns']
        transfer_cumret = self.backtester.trading_performance['transfer']['cumulative_returns']
        
        ax2.plot(dates, baseline_cumret, label='Baseline', linewidth=2, alpha=0.8)
        ax2.plot(dates, transfer_cumret, label='Transfer Learning', linewidth=2, alpha=0.8)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Cumulative Return')
        ax2.set_title('Cumulative Trading Returns')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Daily Returns Distribution
        baseline_daily = self.backtester.trading_performance['baseline']['daily_returns']
        transfer_daily = self.backtester.trading_performance['transfer']['daily_returns']
        
        ax3.hist(baseline_daily, bins=30, alpha=0.6, label='Baseline', density=True)
        ax3.hist(transfer_daily, bins=30, alpha=0.6, label='Transfer Learning', density=True)
        ax3.set_xlabel('Daily Return')
        ax3.set_ylabel('Density')
        ax3.set_title('Daily Returns Distribution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Trading Performance Metrics
        trading_metrics = ['Total Return', 'Sharpe Ratio', 'Win Rate']
        baseline_trading = [
            self.backtester.trading_performance['baseline']['total_return'],
            self.backtester.trading_performance['baseline']['sharpe_ratio'],
            self.backtester.trading_performance['baseline']['win_rate']
        ]
        transfer_trading = [
            self.backtester.trading_performance['transfer']['total_return'],
            self.backtester.trading_performance['transfer']['sharpe_ratio'],
            self.backtester.trading_performance['transfer']['win_rate']
        ]
        
        x = np.arange(len(trading_metrics))
        bars1 = ax4.bar(x - width/2, baseline_trading, width, label='Baseline', alpha=0.8)
        bars2 = ax4.bar(x + width/2, transfer_trading, width, label='Transfer Learning', alpha=0.8)
        
        ax4.set_xlabel('Metrics')
        ax4.set_ylabel('Value')
        ax4.set_title('Trading Performance Metrics')
        ax4.set_xticks(x)
        ax4.set_xticklabels(trading_metrics)
        ax4.legend()
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if 'Ratio' in trading_metrics[bars.index(bar) if hasattr(bars, 'index') else 0]:
                    label = f'{height:.3f}'
                else:
                    label = f'{height:.2%}' if abs(height) < 1 else f'{height:.3f}'
                ax4.annotate(label,
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'backtest_performance_comparison_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_prediction_analysis_chart(self):
        """Create prediction analysis chart"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        dates = pd.to_datetime(self.backtester.baseline_results['test_dates'])
        actual = self.backtester.baseline_results['actual']
        baseline_pred = self.backtester.baseline_results['predictions']
        transfer_pred = self.backtester.transfer_results['predictions']
        
        # 1. Prediction Timeline
        ax1.plot(dates, actual, 'o-', label='Actual', alpha=0.7, markersize=3)
        ax1.plot(dates, baseline_pred, 's-', label='Baseline Pred', alpha=0.7, markersize=3)
        ax1.plot(dates, transfer_pred, '^-', label='Transfer Pred', alpha=0.7, markersize=3)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Prediction (0=Down, 1=Up)')
        ax1.set_title('Prediction Timeline Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Confusion Matrix - Baseline
        from sklearn.metrics import confusion_matrix
        cm_baseline = confusion_matrix(actual, baseline_pred)
        sns.heatmap(cm_baseline, annot=True, fmt='d', cmap='Blues', ax=ax2)
        ax2.set_title('Baseline Confusion Matrix')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Actual')
        
        # 3. Confusion Matrix - Transfer Learning
        cm_transfer = confusion_matrix(actual, transfer_pred)
        sns.heatmap(cm_transfer, annot=True, fmt='d', cmap='Greens', ax=ax3)
        ax3.set_title('Transfer Learning Confusion Matrix')
        ax3.set_xlabel('Predicted')
        ax3.set_ylabel('Actual')
        
        # 4. Confidence Distribution (if available)
        if 'confidences' in self.backtester.transfer_results:
            confidences = self.backtester.transfer_results['confidences']
            ax4.hist(confidences, bins=20, alpha=0.7, color='green', density=True)
            ax4.axvline(np.mean(confidences), color='red', linestyle='--', 
                       label=f'Mean: {np.mean(confidences):.3f}')
            ax4.set_xlabel('Prediction Confidence')
            ax4.set_ylabel('Density')
            ax4.set_title('Transfer Learning Confidence Distribution')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Confidence data\nnot available', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Confidence Analysis')
        
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'backtest_prediction_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_improvement_summary_chart(self):
        """Create improvement summary chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Improvement Metrics
        improvements = {
            'Accuracy': (self.backtester.transfer_results['test_accuracy'] - 
                        self.backtester.baseline_results['test_accuracy']) * 100,
            'Precision': (self.backtester.transfer_results['precision'] - 
                         self.backtester.baseline_results['precision']) * 100,
            'Recall': (self.backtester.transfer_results['recall'] - 
                      self.backtester.baseline_results['recall']) * 100,
            'F1 Score': (self.backtester.transfer_results['f1'] - 
                        self.backtester.baseline_results['f1']) * 100,
            'Total Return': (self.backtester.trading_performance['transfer']['total_return'] - 
                           self.backtester.trading_performance['baseline']['total_return']) * 100,
            'Sharpe Ratio': (self.backtester.trading_performance['transfer']['sharpe_ratio'] - 
                           self.backtester.trading_performance['baseline']['sharpe_ratio']) * 100,
            'Win Rate': (self.backtester.trading_performance['transfer']['win_rate'] - 
                        self.backtester.trading_performance['baseline']['win_rate']) * 100
        }
        
        metrics = list(improvements.keys())
        values = list(improvements.values())
        colors = ['green' if v > 0 else 'red' for v in values]
        
        bars = ax1.barh(metrics, values, color=colors, alpha=0.7)
        ax1.set_xlabel('Improvement (%)')
        ax1.set_title('Transfer Learning Improvements')
        ax1.axvline(0, color='black', linestyle='-', alpha=0.3)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax1.text(value + (0.1 if value > 0 else -0.1), i, f'{value:.1f}%', 
                    va='center', ha='left' if value > 0 else 'right')
        
        # 2. Summary Scorecard
        ax2.axis('off')
        
        # Calculate overall score
        pos_improvements = sum(1 for v in values if v > 0)
        overall_score = (pos_improvements / len(values)) * 100
        
        summary_text = f"""
TRANSFER LEARNING SCORECARD
{'='*30}

📊 METRICS IMPROVED: {pos_improvements}/{len(values)}
🎯 SUCCESS RATE: {overall_score:.0f}%

🏆 BEST IMPROVEMENTS:
"""
        
        # Find top 3 improvements
        sorted_improvements = sorted(improvements.items(), key=lambda x: x[1], reverse=True)
        for i, (metric, improvement) in enumerate(sorted_improvements[:3]):
            summary_text += f"{i+1}. {metric}: +{improvement:.1f}%\n"
        
        summary_text += f"""
📈 ACCURACY BOOST: +{improvements['Accuracy']:.1f}pp
💰 RETURN BOOST: +{improvements['Total Return']:.1f}%
🎪 CONFIDENCE: {self.backtester.transfer_results.get('avg_confidence', 0.5)*100:.0f}%

🌟 CONCLUSION:
Transfer learning shows {'EXCELLENT' if overall_score >= 80 else 'GOOD' if overall_score >= 60 else 'MIXED'} results
across all evaluation metrics.
"""
        
        ax2.text(0.05, 0.95, summary_text, transform=ax2.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'backtest_improvement_summary_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_all_visualizations(self):
        """Create all visualization charts"""
        print("📊 Creating comprehensive visualizations...")
        
        try:
            # Performance comparison
            print("   📈 Creating performance comparison chart...")
            self.create_performance_comparison_chart()
            
            # Prediction analysis
            print("   🎯 Creating prediction analysis chart...")
            self.create_prediction_analysis_chart()
            
            # Improvement summary
            print("   🌟 Creating improvement summary chart...")
            self.create_improvement_summary_chart()
            
            print("✅ All visualizations created successfully!")
            
        except Exception as e:
            print(f"⚠️  Error creating visualizations: {e}")
            print("   Visualizations may require manual execution")

def create_visualizations(backtester):
    """Standalone function to create visualizations"""
    visualizer = BacktestVisualizer(backtester)
    visualizer.create_all_visualizations()
    return visualizer
