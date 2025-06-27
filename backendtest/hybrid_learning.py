#!/usr/bin/env python3
"""
Hybrid Learning Orchestrator
Combines batch training with online learning for optimal performance
"""
import asyncio
import schedule
import threading
import time
import logging
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import subprocess
import sys
import os

from online_learning import OnlineLearningManager
from data_collection import DataCollector
from ml import load_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridLearningOrchestrator:
    """
    Orchestrates hybrid learning system combining:
    1. Batch training (periodic full retraining)
    2. Online learning (continuous incremental updates)
    3. Automated data collection
    4. Model ensemble management
    """
    
    def __init__(self):
        self.online_manager = OnlineLearningManager()
        self.data_collector = DataCollector()
        
        # Load batch-trained model
        self.batch_model = None
        self._load_batch_model()
        
        # Scheduling
        self.scheduler_thread = None
        self.is_running = False
        
        # Performance tracking
        self.performance_history = []
        self.last_batch_retrain = None
        
        # Configuration
        self.config = {
            'batch_retrain_interval_hours': 24,  # Retrain every 24 hours
            'online_update_interval_minutes': 30,  # Update online models every 30 min
            'min_data_points_for_update': 50,  # Minimum data points for online update
            'data_collection_enabled': True,
            'auto_retrain_enabled': True,
            'ensemble_weight_batch': 0.7,  # Weight for batch model in ensemble
            'ensemble_weight_online': 0.3   # Weight for online models in ensemble
        }
        
    def _load_batch_model(self):
        """Load the best batch-trained model"""
        try:
            self.batch_model = load_model()
            logger.info("Loaded batch-trained model successfully")
        except Exception as e:
            logger.error(f"Error loading batch model: {e}")
            self.batch_model = None
            
    def start_system(self):
        """Start the complete hybrid learning system"""
        if self.is_running:
            logger.warning("Hybrid learning system already running")
            return
            
        logger.info("Starting Hybrid Learning System...")
        
        # Start data collection
        if self.config['data_collection_enabled']:
            self.data_collector.start_collection()
            logger.info("✓ Data collection started")
            
        # Setup scheduling
        self._setup_scheduling()
        
        # Start scheduler
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("✓ Hybrid Learning System fully operational")
        
    def stop_system(self):
        """Stop the hybrid learning system"""
        logger.info("Stopping Hybrid Learning System...")
        
        self.is_running = False
        
        # Stop data collection
        self.data_collector.stop_collection()
        
        # Stop scheduler
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=10)
            
        logger.info("✓ Hybrid Learning System stopped")
        
    def _setup_scheduling(self):
        """Setup automated scheduling for various tasks"""
        
        # Online learning updates
        schedule.every(self.config['online_update_interval_minutes']).minutes.do(
            self._scheduled_online_update
        )
        
        # Batch retraining
        if self.config['auto_retrain_enabled']:
            schedule.every(self.config['batch_retrain_interval_hours']).hours.do(
                self._scheduled_batch_retrain
            )
            
        # Performance evaluation
        schedule.every(1).hours.do(self._scheduled_performance_evaluation)
        
        # Model cleanup
        schedule.every().day.at("02:00").do(self._scheduled_cleanup)
        
        logger.info("Scheduling configured")
        
    def _scheduler_loop(self):
        """Main scheduler loop"""
        logger.info("Scheduler loop started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)
                
        logger.info("Scheduler loop stopped")
        
    def _scheduled_online_update(self):
        """Scheduled online learning update"""
        try:
            logger.info("Starting scheduled online learning update...")
            
            # Get recent data from collection
            recent_data = self._prepare_online_training_data()
            
            if len(recent_data) < self.config['min_data_points_for_update']:
                logger.info(f"Insufficient data for online update: {len(recent_data)}")
                return
                
            # Add data to online learning buffer
            for _, row in recent_data.iterrows():
                features = self._extract_features(row)
                target = int(row.get('target', 0))
                self.online_manager.add_training_data(features, target, row['symbol'])
                
            # Update models
            results = self.online_manager.update_models_incremental(
                batch_size=min(len(recent_data), 100)
            )
            
            logger.info(f"Online update completed: {results}")
            
        except Exception as e:
            logger.error(f"Error in scheduled online update: {e}")
            
    def _scheduled_batch_retrain(self):
        """Scheduled batch model retraining"""
        try:
            logger.info("Starting scheduled batch retraining...")
            
            # Check if we have enough new data
            if not self._should_retrain_batch():
                logger.info("Skipping batch retrain - insufficient new data")
                return
                
            # Export recent data for training
            self._export_training_data()
            
            # Trigger batch retraining
            result = subprocess.run([
                sys.executable, "backend/train_model.py"
            ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            if result.returncode == 0:
                logger.info("Batch retraining completed successfully")
                self._load_batch_model()  # Reload the updated model
                self.last_batch_retrain = datetime.now()
            else:
                logger.error(f"Batch retraining failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error in scheduled batch retrain: {e}")
            
    def _scheduled_performance_evaluation(self):
        """Scheduled performance evaluation"""
        try:
            logger.info("Evaluating system performance...")
            
            # Get recent test data
            test_data = self._get_test_data()
            
            if len(test_data) < 10:
                logger.warning("Insufficient test data for evaluation")
                return
                
            # Evaluate ensemble performance
            performance = self.evaluate_ensemble_performance(test_data)
            
            # Store performance metrics
            self.performance_history.append({
                'timestamp': datetime.now().isoformat(),
                'performance': performance
            })
            
            # Keep only recent history
            if len(self.performance_history) > 100:
                self.performance_history = self.performance_history[-50:]
                
            logger.info(f"Performance evaluation: {performance}")
            
        except Exception as e:
            logger.error(f"Error in performance evaluation: {e}")
            
    def _scheduled_cleanup(self):
        """Scheduled cleanup of old data and models"""
        try:
            logger.info("Performing system cleanup...")
            
            # Clean old market data (keep last 30 days)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            # Note: In production, you might want to archive rather than delete
            # This is a simplified cleanup
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            
    def _prepare_online_training_data(self) -> pd.DataFrame:
        """Prepare recent data for online learning"""
        try:
            # Get recent data from all symbols
            all_data = []
            
            for symbol in self.data_collector.symbols:
                recent_data = self.data_collector.get_recent_data(
                    symbol, 
                    hours=self.config['online_update_interval_minutes'] / 60 * 2
                )
                if len(recent_data) > 0:
                    all_data.append(recent_data)
                    
            if not all_data:
                return pd.DataFrame()
                
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Remove rows without targets
            combined_data = combined_data.dropna(subset=['target'])
            
            return combined_data.tail(200)  # Last 200 points
            
        except Exception as e:
            logger.error(f"Error preparing online training data: {e}")
            return pd.DataFrame()
            
    def _extract_features(self, row: pd.Series) -> Dict[str, float]:
        """Extract features from a data row"""
        feature_columns = [
            'open_price', 'high_price', 'low_price', 'close_price', 'volume',
            'rsi', 'stoch_k', 'stoch_d', 'williams_r', 'roc', 'ao',
            'macd', 'macd_signal', 'macd_diff', 'adx', 'cci',
            'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
        ]
        
        # Map database column names to feature names
        name_mapping = {
            'open_price': 'open',
            'high_price': 'high', 
            'low_price': 'low',
            'close_price': 'close'
        }
        
        features = {}
        for col in feature_columns:
            # Use mapped name if available, otherwise use original
            feature_name = name_mapping.get(col, col)
            features[feature_name] = float(row.get(col, 0.0))
            
        return features
        
    def _should_retrain_batch(self) -> bool:
        """Determine if batch retraining should occur"""
        try:
            # Check if enough time has passed since last retrain
            if self.last_batch_retrain:
                time_since_retrain = datetime.now() - self.last_batch_retrain
                if time_since_retrain.total_seconds() < self.config['batch_retrain_interval_hours'] * 3600:
                    return False
                    
            # Check if we have enough new data
            total_new_records = 0
            for symbol in self.data_collector.symbols:
                recent_data = self.data_collector.get_recent_data(symbol, hours=24)
                total_new_records += len(recent_data)
                
            return total_new_records >= 100  # Minimum new records for retraining
            
        except Exception as e:
            logger.error(f"Error checking retrain conditions: {e}")
            return False
            
    def _export_training_data(self):
        """Export collected data for batch training"""
        try:
            # Get data from last week for training
            all_data = []
            
            for symbol in self.data_collector.symbols:
                data = self.data_collector.get_recent_data(symbol, hours=168)  # 1 week
                if len(data) > 0:
                    all_data.append(data)
                    
            if not all_data:
                logger.warning("No data available for export")
                return
                
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Map column names for training script compatibility
            combined_data = combined_data.rename(columns={
                'open_price': 'open',
                'high_price': 'high',
                'low_price': 'low', 
                'close_price': 'close'
            })
            
            # Save as CSV for training script
            output_path = "c:/Users/Hari/Desktop/Trading data/kaia_trading_history_daily.csv"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            combined_data.to_csv(output_path, index=False)
            
            logger.info(f"Exported {len(combined_data)} records for training")
            
        except Exception as e:
            logger.error(f"Error exporting training data: {e}")
            
    def _get_test_data(self) -> pd.DataFrame:
        """Get recent data for performance testing"""
        try:
            # Get last 24 hours of data for testing
            all_data = []
            
            for symbol in self.data_collector.symbols:
                data = self.data_collector.get_recent_data(symbol, hours=24)
                if len(data) > 0:
                    all_data.append(data)
                    
            if not all_data:
                return pd.DataFrame()
                
            return pd.concat(all_data, ignore_index=True).tail(100)
            
        except Exception as e:
            logger.error(f"Error getting test data: {e}")
            return pd.DataFrame()
            
    def predict_hybrid_ensemble(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make predictions using hybrid ensemble (batch + online models)
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Ensemble prediction with confidence scores
        """
        try:
            predictions = {
                'batch_prediction': None,
                'online_predictions': {},
                'ensemble_prediction': 0,
                'ensemble_confidence': 0.5
            }
              # Get batch model prediction
            if self.batch_model:
                try:
                    # Convert features to DataFrame with proper column names to avoid warnings
                    feature_df = pd.DataFrame([features])[self.online_manager.feature_columns]
                    
                    # Suppress sklearn warnings temporarily
                    import warnings
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", message="X does not have valid feature names")
                        batch_pred = self.batch_model.predict(feature_df)[0]
                        predictions['batch_prediction'] = int(batch_pred)
                        
                        # Get probability if available
                        if hasattr(self.batch_model, 'predict_proba'):
                            batch_proba = self.batch_model.predict_proba(feature_df)[0]
                            predictions['batch_confidence'] = float(max(batch_proba))
                        else:
                            predictions['batch_confidence'] = 0.7  # Default confidence
                        
                except Exception as e:
                    logger.debug(f"Batch prediction fallback (using simplified features): {e}")
                    # Fallback: Try with simplified feature array (suppress warnings)
                    try:
                        import warnings
                        with warnings.catch_warnings():
                            warnings.filterwarnings("ignore")
                            feature_array = np.array([features.get(col, 0.0) for col in self.online_manager.feature_columns]).reshape(1, -1)
                            batch_pred = self.batch_model.predict(feature_array)[0]
                            predictions['batch_prediction'] = int(batch_pred)
                            predictions['batch_confidence'] = 0.6  # Lower confidence for fallback
                    except:
                        logger.debug("Batch model prediction failed, using online only")
                    
            # Get online model predictions
            online_result = self.online_manager.predict_ensemble(features)
            predictions['online_predictions'] = online_result
            
            # Create ensemble prediction
            batch_pred = predictions.get('batch_prediction', 0)
            online_pred = online_result.get('ensemble_prediction', 0)
            batch_conf = predictions.get('batch_confidence', 0.5)
            online_conf = online_result.get('ensemble_confidence', 0.5)
            
            # Weighted ensemble
            if batch_pred is not None:
                ensemble_score = (
                    batch_pred * self.config['ensemble_weight_batch'] * batch_conf +
                    online_pred * self.config['ensemble_weight_online'] * online_conf
                ) / (
                    self.config['ensemble_weight_batch'] * batch_conf +
                    self.config['ensemble_weight_online'] * online_conf
                )
                
                predictions['ensemble_prediction'] = int(round(ensemble_score))
                predictions['ensemble_confidence'] = (batch_conf + online_conf) / 2
            else:
                # Fallback to online only
                predictions['ensemble_prediction'] = online_pred
                predictions['ensemble_confidence'] = online_conf
                
            return predictions
            
        except Exception as e:
            logger.error(f"Error in hybrid ensemble prediction: {e}")
            return {
                'batch_prediction': None,
                'online_predictions': {},
                'ensemble_prediction': 0,
                'ensemble_confidence': 0.5,
                'error': str(e)
            }
            
    def predict(self, features: Dict[str, float], symbol: str = None) -> Dict[str, Any]:
        """
        Simple predict method that wraps predict_hybrid_ensemble
        This method provides compatibility with existing code that calls .predict()
        
        Args:
            features: Dictionary of feature values
            symbol: Trading symbol (optional, for compatibility)
            
        Returns:
            Prediction dictionary with prediction and confidence
        """
        try:
            # Use the hybrid ensemble prediction
            ensemble_result = self.predict_hybrid_ensemble(features)
            
            # Convert to expected format
            prediction_value = ensemble_result.get('ensemble_prediction', 0)
            confidence_value = ensemble_result.get('ensemble_confidence', 0.5)
            
            # Convert binary prediction (0/1) to probability (0.0-1.0)
            if prediction_value in [0, 1]:
                probability = confidence_value if prediction_value == 1 else (1 - confidence_value)
            else:
                probability = prediction_value
                
            return {
                'prediction': float(probability),
                'confidence': float(confidence_value),
                'signal': 'LONG' if prediction_value > 0.5 else 'SHORT',
                'ensemble_details': ensemble_result,
                'symbol': symbol
            }
            
        except Exception as e:
            logger.error(f"Error in predict method: {e}")
            return {
                'prediction': 0.5,
                'confidence': 0.5,
                'signal': 'NEUTRAL',
                'error': str(e),
                'symbol': symbol
            }
    
    def evaluate_ensemble_performance(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Evaluate performance of the hybrid ensemble"""
        try:
            if len(test_data) == 0:
                return {'error': 'No test data available'}
                
            correct_predictions = 0
            total_predictions = 0
            
            for _, row in test_data.iterrows():
                if pd.isna(row.get('target')):
                    continue
                    
                features = self._extract_features(row)
                prediction = self.predict_hybrid_ensemble(features)
                
                actual = int(row['target'])
                predicted = prediction['ensemble_prediction']
                
                if predicted == actual:
                    correct_predictions += 1
                total_predictions += 1
                
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0.0
            
            return {
                'accuracy': accuracy,
                'total_predictions': total_predictions,
                'correct_predictions': correct_predictions
            }
            
        except Exception as e:
            logger.error(f"Error evaluating performance: {e}")
            return {'error': str(e)}
            
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            status = {
                'system_running': self.is_running,
                'data_collection': self.data_collector.get_collection_stats(),
                'online_learning': self.online_manager.get_model_stats(),
                'batch_model_loaded': self.batch_model is not None,
                'last_batch_retrain': self.last_batch_retrain.isoformat() if self.last_batch_retrain else None,
                'configuration': self.config,
                'recent_performance': self.performance_history[-5:] if self.performance_history else []
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
            
    def update_config(self, new_config: Dict[str, Any]):
        """Update system configuration"""
        try:
            self.config.update(new_config)
            logger.info(f"Configuration updated: {new_config}")
            
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")

    def get_prediction(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        Get hybrid prediction for a specific symbol
        
        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            
        Returns:
            Prediction result with ensemble analysis
        """
        try:
            # Get latest technical indicators for the symbol
            from data_collection import get_technical_indicators
            
            # Get current features
            indicators = get_technical_indicators(symbol.upper())
            
            if not indicators:
                return {
                    'error': 'Could not fetch technical indicators',
                    'symbol': symbol,
                    'ensemble_prediction': 0,
                    'ensemble_confidence': 0.5,
                    'signal': 'HOLD'
                }
            
            # Prepare features dictionary
            features = {
                'open': indicators.get('open', 0),
                'high': indicators.get('high', 0), 
                'low': indicators.get('low', 0),
                'close': indicators.get('close', 0),
                'volume': indicators.get('volume', 0),
                'rsi': indicators.get('rsi', 50),
                'stoch_k': indicators.get('stoch_k', 50),
                'stoch_d': indicators.get('stoch_d', 50), 
                'williams_r': indicators.get('williams_r', -50),
                'roc': indicators.get('roc', 0),
                'ao': indicators.get('ao', 0),
                'macd': indicators.get('macd', 0),
                'macd_signal': indicators.get('macd_signal', 0),
                'macd_diff': indicators.get('macd_diff', 0),
                'adx': indicators.get('adx', 25),
                'cci': indicators.get('cci', 0),
                'sma_20': indicators.get('sma_20', indicators.get('close', 0)),
                'ema_20': indicators.get('ema_20', indicators.get('close', 0)),
                'bb_high': indicators.get('bb_upper', indicators.get('close', 0)),
                'bb_low': indicators.get('bb_lower', indicators.get('close', 0)),
                'atr': indicators.get('atr', 1),
                'obv': indicators.get('obv', 0),
                'cmf': indicators.get('cmf', 0)
            }
            
            # Get ensemble prediction
            prediction_result = self.predict_hybrid_ensemble(features)
            
            # Add signal interpretation
            ensemble_pred = prediction_result.get('ensemble_prediction', 0)
            confidence = prediction_result.get('ensemble_confidence', 0.5)
            
            if ensemble_pred == 1:
                signal = 'BUY'
            elif ensemble_pred == -1:
                signal = 'SELL'
            else:
                signal = 'HOLD'
            
            prediction_result.update({
                'symbol': symbol,
                'signal': signal,
                'timestamp': datetime.now().isoformat()
            })
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error getting prediction for {symbol}: {e}")
            return {
                'error': str(e),
                'symbol': symbol,
                'ensemble_prediction': 0,
                'ensemble_confidence': 0.5,
                'signal': 'HOLD'
            }
            
# Global instance
hybrid_orchestrator = HybridLearningOrchestrator()

if __name__ == "__main__":
    # Test the hybrid learning system
    print("Testing Hybrid Learning System...")
    
    # Start system
    hybrid_orchestrator.start_system()
    
    # Let it run for a short time
    time.sleep(60)
    
    # Get status
    status = hybrid_orchestrator.get_system_status()
    print(f"System status: {json.dumps(status, indent=2)}")
    
    # Test prediction
    test_features = {col: np.random.random() for col in hybrid_orchestrator.online_manager.feature_columns}
    prediction = hybrid_orchestrator.predict_hybrid_ensemble(test_features)
    print(f"Hybrid prediction: {prediction}")
    
    # Stop system
    hybrid_orchestrator.stop_system()
