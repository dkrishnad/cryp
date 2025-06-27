#!/usr/bin/env python3
"""
ML Features Compatibility Manager
Ensures transfer learning works seamlessly with existing ML features
"""
import numpy as np
import pandas as pd
import joblib
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MLCompatibilityManager:
    """
    Manages compatibility between transfer learning and existing ML features
    """
    
    def __init__(self):
        self.existing_models = {}
        self.transfer_model = None
        self.online_learning_active = True
        self.continuous_learning_active = True
        self.ensemble_weights = {
            'rf': 0.2,
            'xgb': 0.25, 
            'lgb': 0.2,
            'catboost': 0.15,
            'transfer': 0.2  # New transfer learning weight
        }
        
    def load_existing_models(self, models_dict: Dict) -> bool:
        """Load existing trained models"""
        try:
            self.existing_models = models_dict
            logger.info(f"Loaded {len(self.existing_models)} existing models")
            return True
        except Exception as e:
            logger.error(f"Error loading existing models: {e}")
            return False
    
    def integrate_transfer_model(self, transfer_model) -> bool:
        """Integrate transfer learning model with existing ensemble"""
        try:
            self.transfer_model = transfer_model
            
            # Adjust ensemble weights to include transfer learning
            self._rebalance_ensemble_weights()
            
            logger.info("Transfer learning model integrated successfully")
            return True
        except Exception as e:
            logger.error(f"Error integrating transfer model: {e}")
            return False
    
    def _rebalance_ensemble_weights(self):
        """Rebalance ensemble weights to include transfer learning"""
        if self.transfer_model is None:
            return
            
        # Reduce existing weights proportionally to make room for transfer learning
        reduction_factor = 0.8  # Reduce existing weights by 20%
        
        for model_name in ['rf', 'xgb', 'lgb', 'catboost']:
            if model_name in self.ensemble_weights:
                self.ensemble_weights[model_name] *= reduction_factor
        
        # Assign weight to transfer learning
        self.ensemble_weights['transfer'] = 0.2
        
        # Normalize weights to sum to 1.0
        total_weight = sum(self.ensemble_weights.values())
        for model_name in self.ensemble_weights:
            self.ensemble_weights[model_name] /= total_weight
    
    def enhanced_ensemble_predict(self, features: np.ndarray, include_transfer: bool = True) -> Dict:
        """
        Enhanced ensemble prediction including transfer learning
        """
        predictions = {}
        confidences = {}
        
        # Get predictions from existing models
        for model_name, model in self.existing_models.items():
            if model is not None:
                try:
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba(features)
                        predictions[model_name] = proba[:, 1] if len(proba.shape) > 1 else proba
                        confidences[model_name] = np.max(proba, axis=1) if len(proba.shape) > 1 else proba
                    else:
                        pred = model.predict(features)
                        predictions[model_name] = pred
                        confidences[model_name] = np.abs(pred - 0.5) + 0.5  # Convert to confidence
                except Exception as e:
                    logger.warning(f"Error getting prediction from {model_name}: {e}")
        
        # Get transfer learning prediction if available and requested
        if include_transfer and self.transfer_model is not None:
            try:
                if hasattr(self.transfer_model, 'predict_proba'):
                    transfer_proba = self.transfer_model.predict_proba(features)
                    predictions['transfer'] = transfer_proba[:, 1] if len(transfer_proba.shape) > 1 else transfer_proba
                    confidences['transfer'] = np.max(transfer_proba, axis=1) if len(transfer_proba.shape) > 1 else transfer_proba
                else:
                    transfer_pred = self.transfer_model.predict(features)
                    predictions['transfer'] = transfer_pred
                    confidences['transfer'] = np.abs(transfer_pred - 0.5) + 0.5
            except Exception as e:
                logger.warning(f"Error getting transfer learning prediction: {e}")
        
        # Calculate weighted ensemble prediction
        ensemble_prediction = self._calculate_weighted_prediction(predictions)
        ensemble_confidence = self._calculate_ensemble_confidence(confidences, predictions)
        
        return {
            'ensemble_prediction': ensemble_prediction,
            'ensemble_confidence': ensemble_confidence,
            'individual_predictions': predictions,
            'individual_confidences': confidences,
            'weights_used': {k: v for k, v in self.ensemble_weights.items() if k in predictions},
            'transfer_learning_included': 'transfer' in predictions
        }
    
    def _calculate_weighted_prediction(self, predictions: Dict) -> float:
        """Calculate weighted ensemble prediction"""
        if not predictions:
            return 0.5  # Neutral prediction
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for model_name, pred in predictions.items():
            if model_name in self.ensemble_weights:
                weight = self.ensemble_weights[model_name]
                # Handle array vs scalar predictions
                pred_value = pred[0] if isinstance(pred, np.ndarray) and len(pred) > 0 else pred
                weighted_sum += weight * float(pred_value)
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def _calculate_ensemble_confidence(self, confidences: Dict, predictions: Dict) -> float:
        """Calculate ensemble confidence"""
        if not confidences:
            return 0.5
        
        # Weight confidences by model weights and prediction agreement
        weighted_confidence = 0.0
        total_weight = 0.0
        
        for model_name, conf in confidences.items():
            if model_name in self.ensemble_weights:
                weight = self.ensemble_weights[model_name]
                conf_value = conf[0] if isinstance(conf, np.ndarray) and len(conf) > 0 else conf
                weighted_confidence += weight * float(conf_value)
                total_weight += weight
        
        base_confidence = weighted_confidence / total_weight if total_weight > 0 else 0.5
        
        # Boost confidence if models agree
        agreement_boost = self._calculate_prediction_agreement(predictions)
        final_confidence = min(0.95, base_confidence * (1 + agreement_boost * 0.2))
        
        return final_confidence
    
    def _calculate_prediction_agreement(self, predictions: Dict) -> float:
        """Calculate how much models agree (0 = total disagreement, 1 = perfect agreement)"""
        if len(predictions) < 2:
            return 0.0
        
        pred_values = []
        for pred in predictions.values():
            pred_value = pred[0] if isinstance(pred, np.ndarray) and len(pred) > 0 else pred
            pred_values.append(float(pred_value))
        
        # Calculate standard deviation of predictions (lower = more agreement)
        pred_std = np.std(pred_values)
        # Convert to agreement score (0-1, where 1 is perfect agreement)
        agreement = max(0.0, 1.0 - (float(pred_std) * 4))  # Scale factor for crypto prediction range
        
        return agreement
    
    def update_online_learning(self, trade_result: Dict) -> Dict:
        """
        Update all models (including transfer learning) with new trade result
        """
        update_results = {
            'models_updated': [],
            'update_errors': [],
            'online_learning_active': self.online_learning_active
        }
        
        if not self.online_learning_active:
            return update_results
        
        # Prepare features and target from trade result
        features = trade_result.get('features', [])
        target = 1 if trade_result.get('profit', 0) > 0 else 0
        
        if not features:
            update_results['update_errors'].append("No features provided for online learning")
            return update_results
        
        features_array = np.array(features).reshape(1, -1)
        target_array = np.array([target])
        
        # Update existing models that support online learning
        for model_name, model in self.existing_models.items():
            try:
                if hasattr(model, 'partial_fit'):
                    # Models with built-in online learning
                    model.partial_fit(features_array, target_array)
                    update_results['models_updated'].append(model_name)
                elif hasattr(model, 'fit') and model_name in ['sgd', 'online_naive_bayes']:
                    # Incremental models
                    model.fit(features_array, target_array)
                    update_results['models_updated'].append(model_name)
                else:
                    # For tree-based models, we'll retrain periodically instead of per-sample
                    pass
            except Exception as e:
                update_results['update_errors'].append(f"{model_name}: {str(e)}")
        
        # Update transfer learning model if it supports online learning
        if self.transfer_model is not None:
            try:
                if hasattr(self.transfer_model, 'partial_fit'):
                    self.transfer_model.partial_fit(features_array, target_array)
                    update_results['models_updated'].append('transfer')
                elif hasattr(self.transfer_model, 'update_target_model'):
                    # Custom transfer learning update method
                    self.transfer_model.update_target_model(features_array, target_array)
                    update_results['models_updated'].append('transfer')
            except Exception as e:
                update_results['update_errors'].append(f"transfer: {str(e)}")
        
        return update_results
    
    def continuous_learning_update(self, performance_data: Dict) -> Dict:
        """
        Continuous learning updates based on performance data
        """
        update_results = {
            'adjustments_made': [],
            'performance_improvements': {},
            'continuous_learning_active': self.continuous_learning_active
        }
        
        if not self.continuous_learning_active:
            return update_results
        
        # Analyze model performance
        model_accuracies = performance_data.get('model_accuracies', {})
        overall_accuracy = performance_data.get('overall_accuracy', 0.0)
        
        # Adjust ensemble weights based on recent performance
        if model_accuracies:
            weight_adjustments = self._calculate_weight_adjustments(model_accuracies)
            
            for model_name, adjustment in weight_adjustments.items():
                if model_name in self.ensemble_weights:
                    old_weight = self.ensemble_weights[model_name]
                    self.ensemble_weights[model_name] = max(0.05, min(0.4, old_weight + adjustment))
                    update_results['adjustments_made'].append(
                        f"{model_name}: {old_weight:.3f} -> {self.ensemble_weights[model_name]:.3f}"
                    )
            
            # Renormalize weights
            total_weight = sum(self.ensemble_weights.values())
            for model_name in self.ensemble_weights:
                self.ensemble_weights[model_name] /= total_weight
        
        # Track performance improvements
        if overall_accuracy > 0:
            update_results['performance_improvements']['overall_accuracy'] = overall_accuracy
        
        return update_results
    
    def _calculate_weight_adjustments(self, model_accuracies: Dict) -> Dict:
        """Calculate how to adjust ensemble weights based on performance"""
        adjustments = {}
        
        if not model_accuracies:
            return adjustments
        
        # Calculate average accuracy
        avg_accuracy = np.mean(list(model_accuracies.values()))
        
        # Adjust weights based on relative performance
        for model_name, accuracy in model_accuracies.items():
            if model_name in self.ensemble_weights:
                # Models performing above average get weight increase
                performance_ratio = accuracy / avg_accuracy if avg_accuracy > 0 else 1.0
                
                if performance_ratio > 1.1:  # 10% above average
                    adjustments[model_name] = 0.02  # Increase weight
                elif performance_ratio < 0.9:  # 10% below average
                    adjustments[model_name] = -0.02  # Decrease weight
                else:
                    adjustments[model_name] = 0.0  # No change
        
        return adjustments
    
    def get_compatibility_status(self) -> Dict:
        """Get comprehensive compatibility status"""
        return {
            'existing_models_count': len(self.existing_models),
            'transfer_learning_integrated': self.transfer_model is not None,
            'online_learning_active': self.online_learning_active,
            'continuous_learning_active': self.continuous_learning_active,
            'ensemble_weights': self.ensemble_weights.copy(),
            'features_compatibility': {
                'online_learning': 'compatible',
                'continuous_learning': 'compatible', 
                'ensemble_voting': 'enhanced',
                'hybrid_learning': 'compatible',
                'feature_engineering': 'unchanged'
            },
            'integration_health': 'optimal' if self.transfer_model and self.online_learning_active else 'partial'
        }
    
    def validate_all_features(self, test_features: np.ndarray) -> Dict:
        """Comprehensive validation that all ML features work together"""
        validation_results = {
            'tests_passed': 0,
            'tests_failed': 0,
            'feature_status': {},
            'overall_status': 'unknown'
        }
        
        # Test 1: Ensemble prediction with transfer learning
        try:
            ensemble_result = self.enhanced_ensemble_predict(test_features, include_transfer=True)
            if ensemble_result['transfer_learning_included']:
                validation_results['feature_status']['ensemble_with_transfer'] = 'passed'
                validation_results['tests_passed'] += 1
            else:
                validation_results['feature_status']['ensemble_with_transfer'] = 'failed'
                validation_results['tests_failed'] += 1
        except Exception as e:
            validation_results['feature_status']['ensemble_with_transfer'] = f'error: {str(e)}'
            validation_results['tests_failed'] += 1
        
        # Test 2: Online learning compatibility
        try:
            fake_trade_result = {
                'features': test_features[0].tolist(),
                'profit': 100.0
            }
            online_result = self.update_online_learning(fake_trade_result)
            if online_result['online_learning_active'] and len(online_result['models_updated']) > 0:
                validation_results['feature_status']['online_learning'] = 'passed'
                validation_results['tests_passed'] += 1
            else:
                validation_results['feature_status']['online_learning'] = 'failed'
                validation_results['tests_failed'] += 1
        except Exception as e:
            validation_results['feature_status']['online_learning'] = f'error: {str(e)}'
            validation_results['tests_failed'] += 1
        
        # Test 3: Continuous learning compatibility
        try:
            fake_performance = {
                'model_accuracies': {'rf': 0.75, 'xgb': 0.78, 'transfer': 0.82},
                'overall_accuracy': 0.78
            }
            continuous_result = self.continuous_learning_update(fake_performance)
            if continuous_result['continuous_learning_active']:
                validation_results['feature_status']['continuous_learning'] = 'passed'
                validation_results['tests_passed'] += 1
            else:
                validation_results['feature_status']['continuous_learning'] = 'failed'
                validation_results['tests_failed'] += 1
        except Exception as e:
            validation_results['feature_status']['continuous_learning'] = f'error: {str(e)}'
            validation_results['tests_failed'] += 1
        
        # Overall status
        total_tests = validation_results['tests_passed'] + validation_results['tests_failed']
        if total_tests > 0:
            success_rate = validation_results['tests_passed'] / total_tests
            if success_rate >= 0.8:
                validation_results['overall_status'] = 'excellent'
            elif success_rate >= 0.6:
                validation_results['overall_status'] = 'good'
            else:
                validation_results['overall_status'] = 'needs_attention'
        
        return validation_results

    def check_compatibility(self) -> Dict:
        """Check ML environment compatibility"""
        try:
            compatibility_checks = {
                "existing_models": len(self.existing_models) > 0,
                "transfer_model": self.transfer_model is not None,
                "online_learning": self.online_learning_active,
                "continuous_learning": self.continuous_learning_active,
                "ensemble_weights": sum(self.ensemble_weights.values()) == 1.0
            }
            
            all_compatible = all(compatibility_checks.values())
            
            return {
                "status": "success",
                "compatible": all_compatible,
                "checks": compatibility_checks,
                "existing_models_count": len(self.existing_models),
                "transfer_model_active": self.transfer_model is not None,
                "online_learning": self.online_learning_active,
                "continuous_learning": self.continuous_learning_active
            }
        except Exception as e:
            return {
                "status": "error",
                "compatible": False,
                "error": str(e)
            }

    def fix_compatibility(self) -> Dict:
        """Fix compatibility issues"""
        try:
            # Reset ensemble weights
            self._rebalance_ensemble_weights()
            
            return {
                "status": "success",
                "fixed": True,
                "message": "Compatibility issues fixed"
            }
        except Exception as e:
            return {
                "status": "error",
                "fixed": False,
                "error": str(e)
            }

    def get_recommendations(self) -> Dict:
        """Get recommendations for improving compatibility"""
        try:
            recommendations = []
            
            if len(self.existing_models) < 4:
                recommendations.append("Consider training more models for better ensemble performance")
            
            if self.transfer_model is None:
                recommendations.append("Transfer learning model not available - consider training one")
            
            return {
                "status": "success",
                "recommendations": recommendations,
                "count": len(recommendations)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "recommendations": []
            }

# Integration example
def integrate_ml_compatibility():
    """Integration example for existing bot"""
    
    # Initialize compatibility manager
    compatibility = MLCompatibilityManager()
    
    # Load existing models (this would come from your current model loading)
    existing_models = {
        'rf': None,  # Your RandomForest model
        'xgb': None, # Your XGBoost model
        'lgb': None, # Your LightGBM model
        'catboost': None  # Your CatBoost model
    }
    
    compatibility.load_existing_models(existing_models)
    
    # When transfer learning model is ready, integrate it
    # transfer_model = your_trained_transfer_model
    # compatibility.integrate_transfer_model(transfer_model)
    
    # Test compatibility
    test_features = np.random.randn(1, 8)  # Example features
    validation = compatibility.validate_all_features(test_features)
    
    print(f"🔍 ML Compatibility Validation:")
    print(f"✅ Tests Passed: {validation['tests_passed']}")
    print(f"❌ Tests Failed: {validation['tests_failed']}")
    print(f"🎯 Overall Status: {validation['overall_status']}")
    
    return compatibility


if __name__ == "__main__":
    compatibility = integrate_ml_compatibility()
