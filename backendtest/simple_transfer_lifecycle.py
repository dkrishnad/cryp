#!/usr/bin/env python3
"""
Simplified Transfer Learning Lifecycle Manager
Avoids SQL complexity and provides simple file-based tracking
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class SimpleTransferLearningLifecycle:
    """
    Simplified transfer learning lifecycle manager using JSON files
    """
    
    def __init__(self):
        self.models_dir = "models/crypto_transfer"
        self.config_file = os.path.join(self.models_dir, "lifecycle_config.json")
        self.status_file = os.path.join(self.models_dir, "training_status.json")
        
        # Create directories
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Default source pairs
        self.source_pairs = ["ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
        self.target_pair = "BTCUSDT"
        
        # Initialize config
        self._init_config()
    
    def _init_config(self):
        """Initialize configuration if it doesn't exist"""
        if not os.path.exists(self.config_file):
            config = {
                "source_pairs": self.source_pairs,
                "target_pair": self.target_pair,
                "created_at": datetime.now().isoformat(),
                "retrain_threshold": 0.05,
                "training_interval_hours": 24
            }
            self._save_json(config, self.config_file)
        
        if not os.path.exists(self.status_file):
            status = {
                "source_models": {},
                "target_model": {
                    "trained": False,
                    "last_training": None,
                    "accuracy": 0.0
                },
                "training_history": [],
                "last_updated": datetime.now().isoformat()
            }
            self._save_json(status, self.status_file)
    
    def _load_json(self, file_path: str) -> Dict:
        """Load JSON file safely"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return {}
    
    def _save_json(self, data: Dict, file_path: str):
        """Save JSON file safely"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")
    
    def check_initial_setup_required(self) -> Dict:
        """Check if initial setup is required"""
        status = self._load_json(self.status_file)
        config = self._load_json(self.config_file)
        
        source_models = status.get("source_models", {})
        required_symbols = config.get("source_pairs", self.source_pairs)
        
        trained_symbols = [symbol for symbol, info in source_models.items() 
                          if info.get("trained", False)]
        
        missing_symbols = [symbol for symbol in required_symbols 
                          if symbol not in trained_symbols]
        
        completion_percentage = (len(trained_symbols) / len(required_symbols)) * 100
        
        return {
            "setup_required": len(missing_symbols) > 0,
            "missing_symbols": missing_symbols,
            "existing_symbols": trained_symbols,
            "total_required": len(required_symbols),
            "completion_percentage": completion_percentage
        }
    
    def schedule_initial_training(self) -> Dict:
        """Schedule initial training"""
        setup_status = self.check_initial_setup_required()
        
        if not setup_status["setup_required"]:
            return {
                "status": "already_complete",
                "message": "All source models are already trained"
            }
        
        return {
            "status": "scheduled",
            "scheduled_models": setup_status["missing_symbols"],
            "estimated_time_minutes": len(setup_status["missing_symbols"]) * 3
        }
    
    def record_training_completion(self, model_type: str, symbol: str, accuracy: float, model_path: str) -> bool:
        """Record training completion"""
        try:
            status = self._load_json(self.status_file)
            
            if model_type == "source":
                if "source_models" not in status:
                    status["source_models"] = {}
                
                status["source_models"][symbol] = {
                    "trained": True,
                    "accuracy": accuracy,
                    "model_path": model_path,
                    "training_date": datetime.now().isoformat()
                }
            
            elif model_type == "target":
                status["target_model"] = {
                    "trained": True,
                    "accuracy": accuracy,
                    "model_path": model_path,
                    "last_training": datetime.now().isoformat()
                }
            
            # Add to history
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "model_type": model_type,
                "symbol": symbol,
                "accuracy": accuracy,
                "model_path": model_path
            }
            
            if "training_history" not in status:
                status["training_history"] = []
            
            status["training_history"].append(history_entry)
            status["last_updated"] = datetime.now().isoformat()
            
            self._save_json(status, self.status_file)
            return True
            
        except Exception as e:
            logger.error(f"Error recording training completion: {e}")
            return False
    
    def check_retrain_needed(self) -> Dict:
        """Check if retraining is needed"""
        status = self._load_json(self.status_file)
        config = self._load_json(self.config_file)
        
        retrain_needed = {
            "source_models": False,
            "target_model": False,
            "triggers": []
        }
        
        # Check target model age
        target_info = status.get("target_model", {})
        if target_info.get("trained") and target_info.get("last_training"):
            last_training = datetime.fromisoformat(target_info["last_training"])
            hours_since_training = (datetime.now() - last_training).total_seconds() / 3600
            
            training_interval = config.get("training_interval_hours", 24)
            if hours_since_training > training_interval:
                retrain_needed["target_model"] = True
                retrain_needed["triggers"].append(f"Target model trained {hours_since_training:.1f} hours ago")
        
        # Check if target model needs initial training
        if not target_info.get("trained"):
            retrain_needed["target_model"] = True
            retrain_needed["triggers"].append("Target model not yet trained")
        
        # Check source model freshness (weekly refresh)
        source_models = status.get("source_models", {})
        for symbol, info in source_models.items():
            if info.get("training_date"):
                training_date = datetime.fromisoformat(info["training_date"])
                days_since = (datetime.now() - training_date).days
                if days_since > 7:  # Refresh source models weekly
                    retrain_needed["source_models"] = True
                    retrain_needed["triggers"].append(f"Source model {symbol} trained {days_since} days ago")
        
        return retrain_needed
    
    def get_training_schedule(self) -> Dict:
        """Get current training schedule"""
        status = self._load_json(self.status_file)
        config = self._load_json(self.config_file)
        
        return {
            "source_models": status.get("source_models", {}),
            "target_model": status.get("target_model", {}),
            "training_interval_hours": config.get("training_interval_hours", 24),
            "next_suggested_training": self._get_next_training_time()
        }
    
    def _get_next_training_time(self) -> str:
        """Get next suggested training time"""
        status = self._load_json(self.status_file)
        target_info = status.get("target_model", {})
        
        if target_info.get("last_training"):
            last_training = datetime.fromisoformat(target_info["last_training"])
            next_training = last_training + timedelta(hours=24)
            return next_training.isoformat()
        else:
            return "immediate"
    
    def get_lifecycle_status(self) -> Dict:
        """Get overall lifecycle status"""
        status = self._load_json(self.status_file)
        setup_check = self.check_initial_setup_required()
        retrain_check = self.check_retrain_needed()
        
        return {
            "setup_complete": not setup_check["setup_required"],
            "source_models_trained": len(status.get("source_models", {})),
            "target_model_trained": status.get("target_model", {}).get("trained", False),
            "retrain_needed": retrain_check,
            "health_score": self._calculate_health_score(),
            "last_updated": status.get("last_updated", "never")
        }
    
    def _calculate_health_score(self) -> float:
        """Calculate system health score (0-1)"""
        status = self._load_json(self.status_file)
        
        score = 0.0
        
        # Source models contribution (50%)
        source_models = status.get("source_models", {})
        trained_sources = len([m for m in source_models.values() if m.get("trained")])
        total_sources = len(self.source_pairs)
        source_score = (trained_sources / total_sources) * 0.5
        
        # Target model contribution (30%)
        target_trained = status.get("target_model", {}).get("trained", False)
        target_score = 0.3 if target_trained else 0.0
        
        # Freshness contribution (20%)
        target_info = status.get("target_model", {})
        if target_info.get("last_training"):
            last_training = datetime.fromisoformat(target_info["last_training"])
            hours_since = (datetime.now() - last_training).total_seconds() / 3600
            freshness_score = max(0, 0.2 * (1 - hours_since / 48))  # Fresh if < 48 hours
        else:
            freshness_score = 0.0
        
        return min(1.0, source_score + target_score + freshness_score)
