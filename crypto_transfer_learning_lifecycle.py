#!/usr/bin/env python3
"""
Crypto Transfer Learning Training Lifecycle
Manages the complete training lifecycle for crypto transfer learning
"""
import sqlite3
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TransferLearningLifecycle:
    """
    Manages the complete lifecycle of crypto transfer learning training
    """
    
    def __init__(self, db_path="trades.db"):
        self.db_path = db_path
        self.init_lifecycle_tracking()
        
        # Training configuration
        self.source_pairs = ["ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT", "DOGEUSDT"]
        self.target_pair = "BTCUSDT"
        
        # Training thresholds
        self.retrain_accuracy_threshold = 0.05  # Retrain if accuracy drops 5%
        self.source_refresh_days = 21  # Refresh source models every 3 weeks
        self.min_trades_for_retrain = 20  # Minimum trades before retraining
        
    def init_lifecycle_tracking(self):
        """Initialize database tables for lifecycle tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Transfer learning models tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfer_models (
                id INTEGER PRIMARY KEY,
                model_type TEXT,  -- 'source' or 'target'
                symbol TEXT,
                training_date DATETIME,
                accuracy REAL,
                model_path TEXT,
                is_active BOOLEAN DEFAULT 1,
                performance_data TEXT,  -- JSON
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Training schedule tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_schedule (
                id INTEGER PRIMARY KEY,
                model_type TEXT,
                symbol TEXT,
                last_training DATETIME,
                next_training DATETIME,
                retrain_trigger TEXT,  -- 'performance', 'schedule', 'manual'
                status TEXT DEFAULT 'pending',  -- 'pending', 'training', 'completed', 'failed'
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance monitoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfer_performance (
                id INTEGER PRIMARY KEY,
                model_id INTEGER,
                date DATE,
                accuracy REAL,
                precision_score REAL,
                recall REAL,
                profit_factor REAL,
                trades_count INTEGER,
                FOREIGN KEY (model_id) REFERENCES transfer_models (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def check_initial_setup_required(self) -> Dict:
        """Check if initial source model training is required"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if we have trained source models for all pairs
        cursor.execute('''
            SELECT symbol FROM transfer_models 
            WHERE model_type = 'source' AND is_active = 1
        ''')
        
        existing_symbols = [row[0] for row in cursor.fetchall()]
        missing_symbols = [symbol for symbol in self.source_pairs if symbol not in existing_symbols]
        
        conn.close()
        
        return {
            "setup_required": len(missing_symbols) > 0,
            "missing_symbols": missing_symbols,
            "existing_symbols": existing_symbols,
            "total_required": len(self.source_pairs),
            "completion_percentage": (len(existing_symbols) / len(self.source_pairs)) * 100
        }
    
    def schedule_initial_training(self) -> Dict:
        """Schedule initial source model training"""
        setup_status = self.check_initial_setup_required()
        
        if not setup_status["setup_required"]:
            return {"status": "already_complete", "message": "All source models already trained"}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        scheduled_count = 0
        for symbol in setup_status["missing_symbols"]:
            cursor.execute('''
                INSERT INTO training_schedule 
                (model_type, symbol, last_training, next_training, retrain_trigger, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                'source',
                symbol,
                None,
                datetime.now(),
                'initial_setup',
                'pending'
            ))
            scheduled_count += 1
        
        conn.commit()
        conn.close()
        
        return {
            "status": "scheduled",
            "scheduled_models": scheduled_count,
            "estimated_time_minutes": scheduled_count * 3,  # ~3 minutes per source model
            "symbols": setup_status["missing_symbols"]
        }
    
    def check_retrain_needed(self) -> Dict:
        """Check if any models need retraining"""
        retrain_needed = {
            "source_models": [],
            "target_model": False,
            "triggers": [],
            "estimated_time_minutes": 0
        }
        
        # Check target model performance
        target_performance = self._check_target_performance()
        if target_performance["needs_retrain"]:
            retrain_needed["target_model"] = True
            retrain_needed["triggers"].append(f"Target accuracy dropped to {target_performance['current_accuracy']:.3f}")
            retrain_needed["estimated_time_minutes"] += 5
        
        # Check source model freshness
        stale_sources = self._check_source_model_freshness()
        if stale_sources:
            retrain_needed["source_models"] = stale_sources
            retrain_needed["triggers"].append(f"{len(stale_sources)} source models are stale")
            retrain_needed["estimated_time_minutes"] += len(stale_sources) * 3
        
        # Check minimum trades threshold
        trade_count = self._get_recent_trade_count()
        if trade_count >= self.min_trades_for_retrain:
            if not retrain_needed["target_model"]:  # Only if not already scheduled
                retrain_needed["target_model"] = True
                retrain_needed["triggers"].append(f"Sufficient new trades ({trade_count}) for adaptation")
                retrain_needed["estimated_time_minutes"] += 3
        
        return retrain_needed
    
    def _check_target_performance(self) -> Dict:
        """Check target model performance degradation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent performance data
        cursor.execute('''
            SELECT accuracy FROM transfer_performance tp
            JOIN transfer_models tm ON tp.model_id = tm.id
            WHERE tm.model_type = 'target' AND tm.symbol = ? AND tm.is_active = 1
            ORDER BY tp.date DESC
            LIMIT 10
        ''', (self.target_pair,))
        
        recent_accuracies = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if len(recent_accuracies) < 3:
            return {"needs_retrain": False, "current_accuracy": 0.0, "reason": "insufficient_data"}
        
        # Compare recent vs historical performance
        current_avg = np.mean(recent_accuracies[:3])  # Last 3 periods
        historical_avg = np.mean(recent_accuracies[3:]) if len(recent_accuracies) > 3 else current_avg
        
        performance_drop = historical_avg - current_avg
        needs_retrain = performance_drop > self.retrain_accuracy_threshold
        
        return {
            "needs_retrain": needs_retrain,
            "current_accuracy": current_avg,
            "historical_accuracy": historical_avg,
            "performance_drop": performance_drop,
            "threshold": self.retrain_accuracy_threshold
        }
    
    def _check_source_model_freshness(self) -> List[str]:
        """Check which source models need refreshing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=self.source_refresh_days)
        
        cursor.execute('''
            SELECT symbol FROM transfer_models
            WHERE model_type = 'source' 
            AND is_active = 1
            AND training_date < ?
        ''', (cutoff_date,))
        
        stale_symbols = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return stale_symbols
    
    def _get_recent_trade_count(self) -> int:
        """Get count of recent trades for adaptation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count trades from last training
        cursor.execute('''
            SELECT COUNT(*) FROM trades t
            WHERE t.created_at > (
                SELECT COALESCE(MAX(training_date), datetime('now', '-7 days'))
                FROM transfer_models 
                WHERE model_type = 'target' AND is_active = 1
            )
        ''')
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def schedule_retraining(self, force_all: bool = False) -> Dict:
        """Schedule retraining based on current needs"""
        if not force_all:
            retrain_check = self.check_retrain_needed()
        else:
            retrain_check = {
                "source_models": self.source_pairs,
                "target_model": True,
                "triggers": ["manual_force_retrain"],
                "estimated_time_minutes": len(self.source_pairs) * 3 + 5
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        scheduled_tasks = []
        
        # Schedule source model retraining
        for symbol in retrain_check["source_models"]:
            cursor.execute('''
                INSERT INTO training_schedule
                (model_type, symbol, next_training, retrain_trigger, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                'source',
                symbol,
                datetime.now(),
                'performance_degradation',
                'pending'
            ))
            scheduled_tasks.append(f"source_{symbol}")
        
        # Schedule target model retraining
        if retrain_check["target_model"]:
            cursor.execute('''
                INSERT INTO training_schedule
                (model_type, symbol, next_training, retrain_trigger, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                'target',
                self.target_pair,
                datetime.now(),
                'adaptation_needed',
                'pending'
            ))
            scheduled_tasks.append(f"target_{self.target_pair}")
        
        conn.commit()
        conn.close()
        
        return {
            "scheduled_tasks": scheduled_tasks,
            "estimated_time_minutes": retrain_check["estimated_time_minutes"],
            "triggers": retrain_check["triggers"],
            "total_tasks": len(scheduled_tasks)
        }
    
    def get_training_schedule(self) -> Dict:
        """Get current training schedule"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT model_type, symbol, next_training, retrain_trigger, status
            FROM training_schedule
            WHERE status IN ('pending', 'training')
            ORDER BY next_training ASC
        ''')
        
        schedule = []
        for row in cursor.fetchall():
            schedule.append({
                "model_type": row[0],
                "symbol": row[1],
                "next_training": row[2],
                "trigger": row[3],
                "status": row[4]
            })
        
        conn.close()
        
        return {
            "scheduled_trainings": schedule,
            "pending_count": len([s for s in schedule if s["status"] == "pending"]),
            "training_count": len([s for s in schedule if s["status"] == "training"]),
            "next_training": schedule[0]["next_training"] if schedule else None
        }
    
    def record_training_completion(self, 
                                 model_type: str, 
                                 symbol: str, 
                                 accuracy: float,
                                 model_path: str) -> bool:
        """Record completion of a training session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Deactivate old models
            cursor.execute('''
                UPDATE transfer_models 
                SET is_active = 0 
                WHERE model_type = ? AND symbol = ?
            ''', (model_type, symbol))
            
            # Insert new model record
            cursor.execute('''
                INSERT INTO transfer_models
                (model_type, symbol, training_date, accuracy, model_path, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (model_type, symbol, datetime.now(), accuracy, model_path))
            
            # Update training schedule
            cursor.execute('''
                UPDATE training_schedule
                SET status = 'completed', last_training = ?
                WHERE model_type = ? AND symbol = ? AND status = 'training'
            ''', (datetime.now(), model_type, symbol))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error recording training completion: {e}")
            conn.rollback()
            return False
            
        finally:
            conn.close()
    
    def get_lifecycle_status(self) -> Dict:
        """Get comprehensive lifecycle status"""
        return {
            "initial_setup": self.check_initial_setup_required(),
            "retrain_needed": self.check_retrain_needed(),
            "training_schedule": self.get_training_schedule(),
            "lifecycle_health": self._calculate_lifecycle_health()
        }
    
    def _calculate_lifecycle_health(self) -> Dict:
        """Calculate overall health of the transfer learning system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count active models
        cursor.execute('''
            SELECT model_type, COUNT(*) FROM transfer_models
            WHERE is_active = 1
            GROUP BY model_type
        ''')
        
        model_counts = dict(cursor.fetchall())
        
        # Check recent performance
        cursor.execute('''
            SELECT AVG(accuracy) FROM transfer_performance
            WHERE date > date('now', '-7 days')
        ''')
        
        recent_accuracy = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        health_score = 0
        health_factors = []
        
        # Source model coverage
        source_coverage = model_counts.get('source', 0) / len(self.source_pairs)
        health_score += source_coverage * 40
        health_factors.append(f"Source coverage: {source_coverage:.1%}")
        
        # Target model presence
        if model_counts.get('target', 0) > 0:
            health_score += 30
            health_factors.append("Target model: Active")
        else:
            health_factors.append("Target model: Missing")
        
        # Recent performance
        if recent_accuracy > 0.7:
            health_score += 30
            health_factors.append(f"Performance: Good ({recent_accuracy:.1%})")
        elif recent_accuracy > 0.6:
            health_score += 20
            health_factors.append(f"Performance: Fair ({recent_accuracy:.1%})")
        else:
            health_factors.append(f"Performance: Poor ({recent_accuracy:.1%})")
        
        return {
            "health_score": min(100, health_score),
            "health_factors": health_factors,
            "status": "healthy" if health_score >= 80 else "needs_attention" if health_score >= 60 else "critical"
        }


# Usage example for integration
def integrate_lifecycle_management():
    """Integration example for existing bot"""
    
    lifecycle = TransferLearningLifecycle()
    
    # Check initial setup
    setup_status = lifecycle.check_initial_setup_required()
    if setup_status["setup_required"]:
        print(f"⚠️  Initial setup needed for {len(setup_status['missing_symbols'])} models")
        schedule_result = lifecycle.schedule_initial_training()
        print(f"📅 Scheduled training: {schedule_result}")
    
    # Check ongoing maintenance needs
    retrain_check = lifecycle.check_retrain_needed()
    if retrain_check["target_model"] or retrain_check["source_models"]:
        print(f"🔄 Retraining needed: {retrain_check}")
        schedule_result = lifecycle.schedule_retraining()
        print(f"📅 Scheduled retraining: {schedule_result}")
    
    # Get overall status
    status = lifecycle.get_lifecycle_status()
    print(f"🎯 System health: {status['lifecycle_health']}")
    
    return lifecycle


if __name__ == "__main__":
    lifecycle = integrate_lifecycle_management()
