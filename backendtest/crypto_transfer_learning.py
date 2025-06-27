#!/usr/bin/env python3
"""
Crypto Transfer Learning Implementation
Advanced transfer learning system for crypto trading
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional, Tuple
import asyncio
import requests

logger = logging.getLogger(__name__)

class CryptoTransferLearner:
    """
    Advanced Transfer Learning for Crypto Trading
    Uses knowledge from major crypto pairs to enhance target pair predictions
    """
    
    def __init__(self, source_pairs: List[str] = None, target_pair: str = "BTCUSDT"):
        """
        Initialize transfer learning system
        
        Args:
            source_pairs: Major crypto pairs to learn from
            target_pair: Target pair to enhance
        """
        if source_pairs is None:
            source_pairs = ["ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
        
        self.source_pairs = source_pairs
        self.target_pair = target_pair
        
        # Model storage
        self.source_models = {}
        self.target_model = None
        self.transfer_adapter = None
        
        # Feature engineering
        self.scaler = StandardScaler()
        self.feature_columns = []
        
        # Model directory
        self.model_dir = "models/crypto_transfer"
        os.makedirs(self.model_dir, exist_ok=True)
        
        logger.info(f"Initialized CryptoTransferLearner for {target_pair} using {len(source_pairs)} source pairs")
    
    def _get_crypto_data(self, symbol: str, limit: int = 1000) -> pd.DataFrame:
        """
        Fetch crypto data for a symbol
        
        Args:
            symbol: Trading pair symbol
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Simulate fetching crypto data (in real implementation, use Binance API)
            # For demo, create synthetic but realistic data
            dates = pd.date_range(end=datetime.now(), periods=limit, freq='1H')
            
            # Create realistic crypto price movements
            np.random.seed(hash(symbol) % 2**32)  # Consistent data per symbol
            base_price = {"BTCUSDT": 45000, "ETHUSDT": 3200, "BNBUSDT": 380, 
                         "ADAUSDT": 1.2, "SOLUSDT": 105}.get(symbol, 100)
            
            # Generate price series with volatility
            price_changes = np.random.normal(0, 0.02, limit)  # 2% volatility
            prices = [base_price]
            
            for change in price_changes[1:]:
                new_price = prices[-1] * (1 + change)
                prices.append(max(new_price, base_price * 0.5))  # Prevent extreme drops
            
            # Create OHLCV data
            df = pd.DataFrame({
                'timestamp': dates,
                'open': prices,
                'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'close': prices,
                'volume': np.random.uniform(1000000, 5000000, limit)
            })
            
            logger.info(f"Generated {len(df)} data points for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            raise
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for transfer learning
        
        Args:
            df: Raw OHLCV data
            
        Returns:
            DataFrame with engineered features
        """
        features_df = df.copy()
        
        # Price-based features
        features_df['price_change'] = df['close'].pct_change()
        features_df['volatility'] = df['close'].rolling(20).std()
        features_df['rsi'] = self._calculate_rsi(df['close'])
        
        # Moving averages
        features_df['ma_7'] = df['close'].rolling(7).mean()
        features_df['ma_25'] = df['close'].rolling(25).mean()
        features_df['ma_ratio'] = features_df['ma_7'] / features_df['ma_25']
        
        # Volume features
        features_df['volume_ma'] = df['volume'].rolling(20).mean()
        features_df['volume_ratio'] = df['volume'] / features_df['volume_ma']
        
        # Momentum indicators
        features_df['momentum'] = df['close'] / df['close'].shift(10)
        features_df['bollinger_pos'] = self._bollinger_position(df['close'])
        
        # Market structure
        features_df['higher_high'] = (df['high'] > df['high'].shift(1)).astype(int)
        features_df['lower_low'] = (df['low'] < df['low'].shift(1)).astype(int)
        
        # Target variable (next period return)
        features_df['target'] = df['close'].shift(-1) / df['close'] - 1
        
        # Remove NaN values
        features_df = features_df.dropna()
        
        # Store feature columns for later use
        if not self.feature_columns:
            self.feature_columns = [col for col in features_df.columns 
                                  if col not in ['timestamp', 'target', 'open', 'high', 'low', 'close', 'volume']]
        
        logger.info(f"Engineered {len(self.feature_columns)} features")
        return features_df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _bollinger_position(self, prices: pd.Series, period: int = 20, std: float = 2) -> pd.Series:
        """Calculate position within Bollinger Bands"""
        ma = prices.rolling(period).mean()
        std_dev = prices.rolling(period).std()
        upper_band = ma + (std_dev * std)
        lower_band = ma - (std_dev * std)
        return (prices - lower_band) / (upper_band - lower_band)
    
    def train_source_models(self) -> Dict[str, Any]:
        """
        Train source models on major crypto pairs
        
        Returns:
            Training results for each source pair
        """
        results = {}
        
        for symbol in self.source_pairs:
            try:
                logger.info(f"Training source model for {symbol}")
                
                # Get data and engineer features
                data = self._get_crypto_data(symbol, limit=2000)
                features_df = self._engineer_features(data)
                
                # Prepare training data
                X = features_df[self.feature_columns]
                y = features_df['target']
                
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Train ensemble of models for robustness
                models = {
                    'rf': RandomForestRegressor(n_estimators=100, random_state=42),
                    'gb': GradientBoostingRegressor(n_estimators=100, random_state=42)
                }
                
                trained_models = {}
                for model_name, model in models.items():
                    model.fit(X_scaled, y)
                    score = model.score(X_scaled, y)
                    trained_models[model_name] = {
                        'model': model,
                        'score': score
                    }
                    logger.info(f"{symbol} {model_name} R² score: {score:.4f}")
                
                # Store best performing model
                best_model_name = max(trained_models.keys(), 
                                    key=lambda k: trained_models[k]['score'])
                best_model = trained_models[best_model_name]['model']
                
                self.source_models[symbol] = best_model
                
                # Save model
                model_path = os.path.join(self.model_dir, f"source_{symbol}.joblib")
                joblib.dump(best_model, model_path)
                
                results[symbol] = {
                    'trained': True,
                    'score': trained_models[best_model_name]['score'],
                    'best_model': best_model_name,
                    'model_path': model_path
                }
                
            except Exception as e:
                logger.error(f"Error training source model for {symbol}: {e}")
                results[symbol] = {
                    'trained': False,
                    'error': str(e)
                }
        
        logger.info(f"Source model training completed. Success: {len([r for r in results.values() if r.get('trained')])}/{len(self.source_pairs)}")
        return results
    
    def train_target_model_with_transfer(self) -> Dict[str, Any]:
        """
        Train target model using transfer learning from source models
        
        Returns:
            Training results for target model
        """
        try:
            logger.info(f"Training target model for {self.target_pair} with transfer learning")
            
            # Get target data
            target_data = self._get_crypto_data(self.target_pair, limit=1500)
            target_features = self._engineer_features(target_data)
            
            X_target = target_features[self.feature_columns]
            y_target = target_features['target']
            
            # Scale features
            X_target_scaled = self.scaler.transform(X_target)
            
            # Get knowledge from source models
            source_predictions = self._get_source_predictions(X_target_scaled)
            
            # Combine target features with source knowledge
            enhanced_features = np.column_stack([X_target_scaled, source_predictions])
            
            # Train target model with enhanced features
            self.target_model = RandomForestRegressor(
                n_estimators=150,  # More trees for transfer learning
                max_depth=10,
                random_state=42
            )
            
            self.target_model.fit(enhanced_features, y_target)
            
            # Evaluate performance
            train_score = self.target_model.score(enhanced_features, y_target)
            predictions = self.target_model.predict(enhanced_features)
            mse = mean_squared_error(y_target, predictions)
            
            # Compare with baseline (without transfer learning)
            baseline_model = RandomForestRegressor(n_estimators=100, random_state=42)
            baseline_model.fit(X_target_scaled, y_target)
            baseline_score = baseline_model.score(X_target_scaled, y_target)
            
            improvement = train_score - baseline_score
            
            # Save target model
            model_path = os.path.join(self.model_dir, f"target_{self.target_pair}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.joblib")
            joblib.dump(self.target_model, model_path)
            
            # Save scaler
            scaler_path = os.path.join(self.model_dir, "scaler.joblib")
            joblib.dump(self.scaler, scaler_path)
            
            results = {
                'trained': True,
                'target_pair': self.target_pair,
                'score': train_score,
                'baseline_score': baseline_score,
                'improvement': improvement,
                'mse': mse,
                'model_path': model_path,
                'scaler_path': scaler_path,
                'source_models_used': len(self.source_models),
                'transfer_effective': improvement > 0.01  # 1% improvement threshold
            }
            
            logger.info(f"Target model training completed. R² score: {train_score:.4f}, Improvement: {improvement:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error training target model: {e}")
            return {
                'trained': False,
                'error': str(e)
            }
    
    def _get_source_predictions(self, X: np.ndarray) -> np.ndarray:
        """
        Get predictions from all source models
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of source model predictions
        """
        source_preds = []
        
        for symbol, model in self.source_models.items():
            try:
                preds = model.predict(X)
                source_preds.append(preds)
            except Exception as e:
                logger.warning(f"Error getting predictions from {symbol} model: {e}")
                # Use zeros if model fails
                source_preds.append(np.zeros(len(X)))
        
        return np.column_stack(source_preds) if source_preds else np.zeros((len(X), 1))
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Make predictions using transfer learning
        
        Args:
            features: Input features
            
        Returns:
            Prediction results with confidence and transfer learning info
        """
        try:
            if self.target_model is None:
                raise ValueError("Target model not trained")
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Get source predictions
            source_predictions = self._get_source_predictions(features_scaled)
            
            # Combine with source knowledge
            enhanced_features = np.column_stack([features_scaled, source_predictions])
            
            # Make prediction
            prediction = self.target_model.predict(enhanced_features)
            
            # Calculate confidence based on source agreement
            source_agreement = self._calculate_source_agreement(source_predictions)
            base_confidence = 0.6
            confidence = min(0.95, base_confidence + (0.3 * source_agreement))
            
            return {
                'prediction': prediction.tolist(),
                'confidence': confidence,
                'source_agreement': source_agreement,
                'source_models_active': len(self.source_models),
                'transfer_learning_active': True
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def _calculate_source_agreement(self, source_predictions: np.ndarray) -> float:
        """
        Calculate agreement between source model predictions
        
        Args:
            source_predictions: Array of source predictions
            
        Returns:
            Agreement score (0-1)
        """
        if source_predictions.shape[1] < 2:
            return 0.5
        
        # Calculate standard deviation across source predictions
        std_across_sources = np.std(source_predictions, axis=1)
        mean_std = np.mean(std_across_sources)
        
        # Convert to agreement score (lower std = higher agreement)
        agreement = max(0, 1 - (mean_std * 10))  # Scale factor of 10
        return min(1, agreement)
    
    def load_models(self) -> bool:
        """
        Load pre-trained models from disk
        
        Returns:
            True if models loaded successfully
        """
        try:
            # Load source models
            for symbol in self.source_pairs:
                model_path = os.path.join(self.model_dir, f"source_{symbol}.joblib")
                if os.path.exists(model_path):
                    self.source_models[symbol] = joblib.load(model_path)
                    logger.info(f"Loaded source model for {symbol}")
            
            # Load target model (latest)
            target_files = [f for f in os.listdir(self.model_dir) 
                          if f.startswith(f"target_{self.target_pair}") and f.endswith('.joblib')]
            
            if target_files:
                latest_target = sorted(target_files)[-1]
                target_path = os.path.join(self.model_dir, latest_target)
                self.target_model = joblib.load(target_path)
                logger.info(f"Loaded target model: {latest_target}")
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, "scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info("Loaded feature scaler")
            
            success = len(self.source_models) > 0 and self.target_model is not None
            logger.info(f"Model loading {'successful' if success else 'failed'}")
            return success
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models
        
        Returns:
            Model information dictionary
        """
        return {
            'source_models': list(self.source_models.keys()),
            'target_pair': self.target_pair,
            'target_model_loaded': self.target_model is not None,
            'scaler_loaded': hasattr(self.scaler, 'scale_'),
            'feature_count': len(self.feature_columns),
            'model_directory': self.model_dir
        }
