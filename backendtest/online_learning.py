#!/usr/bin/env python3
"""
Online Learning System for Crypto Trading Bot
Implements incremental learning alongside batch-trained models
"""
import numpy as np
import pandas as pd
import joblib
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import sqlite3
import threading
import time
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OnlineLearningManager:
    """
    Manages online learning models that can update incrementally
    """
    
    def __init__(self, models_dir: str = "models", db_path: str = "trades.db"):
        self.models_dir = os.path.abspath(models_dir)
        self.db_path = db_path
        self.online_models_dir = os.path.join(self.models_dir, "online")
        os.makedirs(self.online_models_dir, exist_ok=True)
        
        # Online learning models
        self.models = {}
        self.scalers = {}
        self.model_configs = {
            'sgd': {
                'class': SGDClassifier,
                'params': {
                    'loss': 'log_loss',
                    'learning_rate': 'adaptive',
                    'eta0': 0.01,
                    'random_state': 42,
                    'max_iter': 1000
                }
            },
            'passive_aggressive': {
                'class': PassiveAggressiveClassifier,
                'params': {
                    'random_state': 42,
                    'max_iter': 1000
                }
            },
            'mlp_online': {
                'class': MLPClassifier,
                'params': {
                    'hidden_layer_sizes': (50, 25),
                    'learning_rate': 'adaptive',
                    'random_state': 42,
                    'max_iter': 1
                }
            }
        }
        
        # Data buffer for batch updates
        self.data_buffer = deque(maxlen=1000)
        self.feature_columns = [
            'open', 'high', 'low', 'close', 'volume', 'rsi', 'stoch_k', 'stoch_d', 
            'williams_r', 'roc', 'ao', 'macd', 'macd_signal', 'macd_diff', 'adx', 
            'cci', 'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
        ]
        
        # Performance tracking
        self.performance_history = {}
        self.last_update_time = {}
          # Load existing models
        self._load_models()

    def _load_models(self):
        """Load existing online learning models"""
        try:
            for model_name in self.model_configs.keys():
                model_path = os.path.join(self.online_models_dir, f"{model_name}.joblib")
                scaler_path = os.path.join(self.online_models_dir, f"{model_name}_scaler.joblib")
                metadata_path = os.path.join(self.online_models_dir, f"{model_name}_metadata.json")
                
                if os.path.exists(model_path) and os.path.exists(scaler_path):
                    self.models[model_name] = joblib.load(model_path)
                    self.scalers[model_name] = joblib.load(scaler_path)
                    
                    # Load metadata if available
                    if os.path.exists(metadata_path):
                        try:
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            
                            # Restore performance history and last update time
                            self.performance_history[model_name] = metadata.get('performance_history', [])
                            
                            if 'last_update' in metadata:
                                self.last_update_time[model_name] = datetime.fromisoformat(metadata['last_update'])
                            else:
                                self.last_update_time[model_name] = datetime.now()
                                
                            logger.info(f"Loaded online model with metadata: {model_name} "
                                      f"(performance history: {len(self.performance_history[model_name])} entries)")
                        except Exception as e:
                            logger.warning(f"Could not load metadata for {model_name}: {e}")
                            self.performance_history[model_name] = []
                            self.last_update_time[model_name] = datetime.now()
                    else:
                        self.performance_history[model_name] = []
                        self.last_update_time[model_name] = datetime.now()
                    
                    logger.info(f"Loaded online model: {model_name}")
                else:
                    # Initialize new model
                    self._initialize_model(model_name)
                    
        except Exception as e:
            logger.error(f"Error loading online models: {e}")
            
    def _initialize_model(self, model_name: str):
        """Initialize a new online learning model"""
        try:
            config = self.model_configs[model_name]
            model = config['class'](**config['params'])
            scaler = StandardScaler()
            
            # Initialize with dummy data to set up the model structure
            dummy_X = np.random.random((10, len(self.feature_columns)))
            dummy_y = np.random.randint(0, 2, 10)
            
            scaled_X = scaler.fit_transform(dummy_X)
            model.fit(scaled_X, dummy_y)
            
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            self.performance_history[model_name] = []
            self.last_update_time[model_name] = datetime.now()
            
            # Save initialized model
            self._save_model(model_name)
            
            logger.info(f"Initialized online model: {model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing model {model_name}: {e}")
            
    def _save_model(self, model_name: str):
        """Save online learning model and scaler"""
        try:
            model_path = os.path.join(self.online_models_dir, f"{model_name}.joblib")
            scaler_path = os.path.join(self.online_models_dir, f"{model_name}_scaler.joblib")
            
            joblib.dump(self.models[model_name], model_path)
            joblib.dump(self.scalers[model_name], scaler_path)
            
            # Save metadata
            metadata = {
                'last_update': self.last_update_time[model_name].isoformat(),
                'performance_history': self.performance_history.get(model_name, []),
                'buffer_size': len(self.data_buffer)
            }
            
            metadata_path = os.path.join(self.online_models_dir, f"{model_name}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {e}")
            
    def add_training_data(self, features: Dict[str, float], target: int, symbol: str = "default"):
        """
        Add new training data to the buffer
        
        Args:
            features: Dictionary of feature values
            target: Binary target (0 or 1)
            symbol: Trading symbol
        """
        try:
            # Convert features to array format
            feature_array = [features.get(col, 0.0) for col in self.feature_columns]
            
            data_point = {
                'features': feature_array,
                'target': target,
                'symbol': symbol,
                'timestamp': datetime.now().isoformat()
            }
            
            self.data_buffer.append(data_point)
            logger.info(f"Added training data for {symbol}, buffer size: {len(self.data_buffer)}")
            
        except Exception as e:
            logger.error(f"Error adding training data: {e}")
            
    def update_models_incremental(self, batch_size: int = 50) -> Dict[str, float]:
        """
        Incrementally update models with buffered data
        
        Args:
            batch_size: Number of samples to use for update
            
        Returns:
            Dictionary of model accuracies
        """
        if len(self.data_buffer) < batch_size:
            logger.info(f"Insufficient data for update. Buffer: {len(self.data_buffer)}, Required: {batch_size}")
            return {}
            
        try:
            # Prepare batch data
            recent_data = list(self.data_buffer)[-batch_size:]
            X = np.array([point['features'] for point in recent_data])
            y = np.array([point['target'] for point in recent_data])
            
            results = {}
            
            for model_name, model in self.models.items():
                try:
                    # Scale features
                    scaler = self.scalers[model_name]
                    X_scaled = scaler.transform(X)
                    
                    # Partial fit for online learning
                    if hasattr(model, 'partial_fit'):
                        model.partial_fit(X_scaled, y)
                    else:
                        # For MLPClassifier, use fit with single iteration
                        model.fit(X_scaled, y)
                    
                    # Calculate accuracy on recent data
                    predictions = model.predict(X_scaled)
                    accuracy = accuracy_score(y, predictions)
                    
                    # Update tracking
                    self.performance_history[model_name].append({
                        'timestamp': datetime.now().isoformat(),
                        'accuracy': accuracy,
                        'sample_count': len(X)
                    })
                    
                    # Keep only recent performance history
                    if len(self.performance_history[model_name]) > 100:
                        self.performance_history[model_name] = self.performance_history[model_name][-50:]
                    
                    self.last_update_time[model_name] = datetime.now()
                    results[model_name] = accuracy
                    
                    logger.info(f"Updated {model_name}: accuracy={accuracy:.4f}")
                    
                except Exception as e:
                    logger.error(f"Error updating model {model_name}: {e}")
                    
            # Save updated models
            for model_name in results.keys():
                self._save_model(model_name)
                
            return results
            
        except Exception as e:
            logger.error(f"Error in incremental update: {e}")
            return {}
            
    def predict_ensemble(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make predictions using ensemble of online models
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        try:
            feature_array = np.array([features.get(col, 0.0) for col in self.feature_columns]).reshape(1, -1)
            
            predictions = {}
            probabilities = {}
            
            for model_name, model in self.models.items():
                try:
                    scaler = self.scalers[model_name]
                    X_scaled = scaler.transform(feature_array)
                    
                    # Get prediction
                    pred = model.predict(X_scaled)[0]
                    predictions[model_name] = int(pred)
                    
                    # Get probability if available
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba(X_scaled)[0]
                        probabilities[model_name] = {
                            'confidence': float(max(proba)),
                            'proba_0': float(proba[0]),
                            'proba_1': float(proba[1])
                        }
                    else:
                        # Use decision function for confidence
                        decision = model.decision_function(X_scaled)[0]
                        confidence = 1 / (1 + np.exp(-abs(decision)))  # Sigmoid of absolute decision
                        probabilities[model_name] = {
                            'confidence': float(confidence),
                            'decision_value': float(decision)
                        }
                        
                except Exception as e:
                    logger.error(f"Error predicting with {model_name}: {e}")
                    
            # Ensemble prediction (majority vote)
            if predictions:
                ensemble_pred = int(np.round(np.mean(list(predictions.values()))))
                ensemble_confidence = np.mean([p.get('confidence', 0.5) for p in probabilities.values()])
            else:
                ensemble_pred = 0
                ensemble_confidence = 0.5
                
            return {
                'ensemble_prediction': ensemble_pred,
                'ensemble_confidence': float(ensemble_confidence),
                'individual_predictions': predictions,
                'probabilities': probabilities,
                'model_count': len(predictions)
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {e}")
            return {
                'ensemble_prediction': 0,
                'ensemble_confidence': 0.5,
                'individual_predictions': {},
                'probabilities': {},
                'model_count': 0,
                'error': str(e)
            }
            
    def get_model_stats(self) -> Dict[str, Any]:
        """Get statistics about online learning models"""
        try:
            stats = {}
            
            for model_name in self.models.keys():
                recent_performance = self.performance_history.get(model_name, [])
                recent_accuracies = [p['accuracy'] for p in recent_performance[-10:]]
                
                stats[model_name] = {
                    'last_update': self.last_update_time.get(model_name, datetime.now()).isoformat(),
                    'recent_accuracy': np.mean(recent_accuracies) if recent_accuracies else 0.0,
                    'performance_history_length': len(recent_performance),
                    'model_type': type(self.models[model_name]).__name__
                }
                
            stats['buffer_size'] = len(self.data_buffer)
            stats['total_models'] = len(self.models)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting model stats: {e}")
            return {'error': str(e)}
            
    def reset_models(self):
        """Reset all online learning models"""
        try:
            for model_name in list(self.models.keys()):
                self._initialize_model(model_name)
                
            self.data_buffer.clear()
            logger.info("Reset all online learning models")
            
        except Exception as e:
            logger.error(f"Error resetting models: {e}")

    def update_models(self) -> Dict:
        """Update models with latest data"""
        try:
            results = self.update_models_incremental()
            return {
                "status": "success",
                "updated_models": list(results.keys()),
                "accuracies": results
            }
        except Exception as e:
            logger.error(f"Error updating models: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        try:
            model_stats = self.get_model_stats()
            return {
                "status": "success",
                "stats": model_stats,
                "data_buffer_size": len(self.data_buffer),
                "active_models": list(self.models.keys())
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def enable_learning(self) -> Dict:
        """Enable online learning system"""
        try:
            self.enabled = True
            logger.info("Online learning system enabled")
            return {
                "status": "success",
                "message": "Online learning enabled",
                "enabled": True,
                "config": {
                    "models": list(self.model_configs.keys()),
                    "data_buffer_size": len(self.data_buffer),
                    "active_models": list(self.models.keys())
                }
            }
        except Exception as e:
            logger.error(f"Error enabling learning: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def disable_learning(self) -> Dict:
        """Disable online learning system"""
        try:
            self.enabled = False
            logger.info("Online learning system disabled")
            return {
                "status": "success",
                "message": "Online learning disabled",
                "enabled": False,
                "final_stats": self.get_stats()
            }
        except Exception as e:
            logger.error(f"Error disabling learning: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_status(self) -> Dict:
        """Get current status of online learning system"""
        try:
            return {
                "enabled": getattr(self, 'enabled', True),
                "models_loaded": len(self.models),
                "data_buffer_size": len(self.data_buffer),
                "last_update": getattr(self, 'last_update', None),
                "total_samples_processed": sum(getattr(self, 'sample_counts', {}).values()),
                "active_symbols": list(set(item['symbol'] for item in self.data_buffer))
            }
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                "enabled": False,
                "error": str(e)
            }

# Global instance
online_learning_manager = OnlineLearningManager()

if __name__ == "__main__":
    # Test the online learning system
    print("Testing Online Learning System...")
    
    # Add some dummy data
    for i in range(100):
        features = {col: np.random.random() for col in online_learning_manager.feature_columns}
        target = np.random.randint(0, 2)
        online_learning_manager.add_training_data(features, target, f"test_symbol_{i%3}")
        
    # Update models
    results = online_learning_manager.update_models_incremental(batch_size=20)
    print(f"Update results: {results}")
    
    # Make prediction
    test_features = {col: np.random.random() for col in online_learning_manager.feature_columns}
    prediction = online_learning_manager.predict_ensemble(test_features)
    print(f"Prediction: {prediction}")
    
    # Get stats
    stats = online_learning_manager.get_model_stats()
    print(f"Stats: {json.dumps(stats, indent=2)}")
