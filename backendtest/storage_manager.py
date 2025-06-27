#!/usr/bin/env python3
"""
Storage Management for Crypto Transfer Learning
Manages storage optimization and cleanup for 6-month operation
"""
import os
import shutil
import gzip
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class StorageManager:
    """
    Manages storage for crypto transfer learning system
    """
    
    def __init__(self, base_path="c:/Users/Hari/Desktop/Crypto bot"):
        self.base_path = Path(base_path)
        self.models_dir = self.base_path / "models"
        self.db_path = self.base_path / "trades.db"
        
        # Storage limits (in GB)
        self.max_storage_gb = 30  # Conservative limit for 6-month operation
        self.warning_threshold_gb = 25
        
        # Retention policies
        self.keep_recent_models = 5  # Keep last 5 versions
        self.compress_after_days = 30
        self.delete_after_days = 180  # 6 months
        
    def get_current_storage_usage(self) -> dict:
        """Get current storage usage breakdown"""
        storage_breakdown = {
            "base_models": self._get_directory_size(self.models_dir / "base"),
            "transfer_models": self._get_directory_size(self.models_dir / "crypto_transfer"),
            "database": self._get_file_size(self.db_path),
            "logs": self._get_directory_size(self.base_path / "logs"),
            "archives": self._get_directory_size(self.models_dir / "archive")
        }
        
        total_mb = sum(storage_breakdown.values())
        
        return {
            "breakdown_mb": storage_breakdown,
            "total_mb": total_mb,
            "total_gb": total_mb / 1024,
            "usage_percentage": (total_mb / 1024) / self.max_storage_gb * 100 if self.max_storage_gb > 0 else 0,
            "warning_threshold_reached": (total_mb / 1024) > self.warning_threshold_gb
        }
    
    def _get_directory_size(self, directory: Path) -> float:
        """Get directory size in MB"""
        if not directory.exists():
            return 0.0
            
        total_size = 0
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    def _get_file_size(self, file_path: Path) -> float:
        """Get file size in MB"""
        if not file_path.exists():
            return 0.0
        return file_path.stat().st_size / (1024 * 1024)
    
    def project_6_month_storage(self) -> dict:
        """Project storage needs for 6 months"""
        current_usage = self.get_current_storage_usage()
        current_gb = current_usage["total_gb"]
        
        # Projection based on training frequency
        monthly_growth = {
            "transfer_models": 1.66,  # 52 target updates / 12 months * 6 months
            "source_models": 0.53,   # 8 refreshes / 12 months * 6 months  
            "database": 0.08,        # 165MB / 12 months * 6 months
            "base_models": 4.55,     # Existing model growth
            "logs_archives": 0.87    # Log and archive growth
        }
        
        projected_6month_gb = current_gb + sum(monthly_growth.values())
        
        return {
            "current_gb": current_gb,
            "projected_6month_gb": projected_6month_gb,
            "monthly_growth_breakdown": monthly_growth,
            "storage_health": "healthy" if projected_6month_gb < self.warning_threshold_gb else "warning" if projected_6month_gb < self.max_storage_gb else "critical",
            "optimization_needed": projected_6month_gb > self.warning_threshold_gb,
            "cleanup_recommendation": self._get_cleanup_recommendations(projected_6month_gb)
        }
    
    def _get_cleanup_recommendations(self, projected_gb: float) -> list:
        """Get cleanup recommendations based on projection"""
        recommendations = []
        
        if projected_gb > self.warning_threshold_gb:
            recommendations.append("Enable automatic model compression")
            recommendations.append("Implement rolling deletion of old models")
            
        if projected_gb > self.max_storage_gb:
            recommendations.append("Reduce model retention period to 3 months")
            recommendations.append("Compress all models older than 2 weeks")
            recommendations.append("Archive training logs externally")
            
        return recommendations
    
    def cleanup_old_models(self, keep_versions: int = 5, compress_old: bool = True) -> dict:
        """Clean up old model versions"""
        cleanup_stats = {
            "deleted_files": 0,
            "compressed_files": 0,
            "space_freed_mb": 0,
            "errors": []
        }
        
        try:
            # Clean base models
            cleanup_stats = self._cleanup_model_directory(
                self.models_dir / "base", 
                keep_versions, 
                compress_old, 
                cleanup_stats
            )
            
            # Clean transfer learning models
            transfer_dir = self.models_dir / "crypto_transfer"
            if transfer_dir.exists():
                for model_type_dir in transfer_dir.iterdir():
                    if model_type_dir.is_dir():
                        cleanup_stats = self._cleanup_model_directory(
                            model_type_dir,
                            keep_versions,
                            compress_old,
                            cleanup_stats
                        )
                        
        except Exception as e:
            cleanup_stats["errors"].append(f"Cleanup error: {str(e)}")
            logger.error(f"Cleanup error: {e}")
        
        return cleanup_stats
    
    def _cleanup_model_directory(self, directory: Path, keep_versions: int, compress_old: bool, stats: dict) -> dict:
        """Clean up a specific model directory"""
        if not directory.exists():
            return stats
            
        # Get all model files sorted by modification time
        model_files = []
        for file_path in directory.glob("*.joblib"):
            if file_path.is_file():
                model_files.append((file_path, file_path.stat().st_mtime))
        
        # Sort by modification time (newest first)
        model_files.sort(key=lambda x: x[1], reverse=True)
        
        # Keep recent models, process older ones
        for i, (file_path, mtime) in enumerate(model_files):
            file_age_days = (datetime.now().timestamp() - mtime) / (24 * 3600)
            
            if i >= keep_versions:  # Beyond keep limit
                if file_age_days > self.delete_after_days:
                    # Delete very old files
                    try:
                        file_size_mb = file_path.stat().st_size / (1024 * 1024)
                        file_path.unlink()
                        stats["deleted_files"] += 1
                        stats["space_freed_mb"] += file_size_mb
                    except Exception as e:
                        stats["errors"].append(f"Delete error {file_path}: {str(e)}")
                        
                elif file_age_days > self.compress_after_days and compress_old:
                    # Compress old files
                    try:
                        compressed_path = file_path.with_suffix(file_path.suffix + '.gz')
                        if not compressed_path.exists():
                            with open(file_path, 'rb') as f_in:
                                with gzip.open(compressed_path, 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            
                            original_size = file_path.stat().st_size
                            compressed_size = compressed_path.stat().st_size
                            space_saved = (original_size - compressed_size) / (1024 * 1024)
                            
                            file_path.unlink()  # Remove original
                            stats["compressed_files"] += 1
                            stats["space_freed_mb"] += space_saved
                            
                    except Exception as e:
                        stats["errors"].append(f"Compress error {file_path}: {str(e)}")
        
        return stats
    
    def optimize_storage(self) -> dict:
        """Comprehensive storage optimization"""
        optimization_results = {
            "actions_taken": [],
            "space_freed_mb": 0,
            "storage_before_gb": 0,
            "storage_after_gb": 0,
            "optimization_success": False
        }
        
        try:
            # Get current usage
            before_usage = self.get_current_storage_usage()
            optimization_results["storage_before_gb"] = before_usage["total_gb"]
            
            # Action 1: Cleanup old models
            cleanup_result = self.cleanup_old_models(keep_versions=3, compress_old=True)
            if cleanup_result["space_freed_mb"] > 0:
                optimization_results["actions_taken"].append(f"Cleaned up models: {cleanup_result['space_freed_mb']:.1f} MB freed")
                optimization_results["space_freed_mb"] += cleanup_result["space_freed_mb"]
            
            # Action 2: Compress training logs
            log_compression = self._compress_old_logs()
            if log_compression["space_freed_mb"] > 0:
                optimization_results["actions_taken"].append(f"Compressed logs: {log_compression['space_freed_mb']:.1f} MB freed")
                optimization_results["space_freed_mb"] += log_compression["space_freed_mb"]
            
            # Action 3: Database optimization
            db_optimization = self._optimize_database()
            if db_optimization["space_freed_mb"] > 0:
                optimization_results["actions_taken"].append(f"Optimized database: {db_optimization['space_freed_mb']:.1f} MB freed")
                optimization_results["space_freed_mb"] += db_optimization["space_freed_mb"]
            
            # Get final usage
            after_usage = self.get_current_storage_usage()
            optimization_results["storage_after_gb"] = after_usage["total_gb"]
            optimization_results["optimization_success"] = True
            
        except Exception as e:
            optimization_results["actions_taken"].append(f"Optimization error: {str(e)}")
            logger.error(f"Storage optimization error: {e}")
        
        return optimization_results
    
    def _compress_old_logs(self) -> dict:
        """Compress old log files"""
        result = {"space_freed_mb": 0, "files_compressed": 0}
        
        logs_dir = self.base_path / "logs"
        if not logs_dir.exists():
            return result
        
        cutoff_date = datetime.now() - timedelta(days=7)  # Compress logs older than 1 week
        
        for log_file in logs_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                try:
                    compressed_path = log_file.with_suffix(log_file.suffix + '.gz')
                    if not compressed_path.exists():
                        with open(log_file, 'rb') as f_in:
                            with gzip.open(compressed_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        original_size = log_file.stat().st_size
                        compressed_size = compressed_path.stat().st_size
                        space_saved = (original_size - compressed_size) / (1024 * 1024)
                        
                        log_file.unlink()
                        result["space_freed_mb"] += space_saved
                        result["files_compressed"] += 1
                        
                except Exception as e:
                    logger.error(f"Error compressing {log_file}: {e}")
        
        return result
    
    def _optimize_database(self) -> dict:
        """Optimize database storage"""
        result = {"space_freed_mb": 0, "optimization_applied": False}
        
        if not self.db_path.exists():
            return result
        
        try:
            original_size = self.db_path.stat().st_size
            
            # Database optimization
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Remove old performance data (keep 3 months)
            cutoff_date = datetime.now() - timedelta(days=90)
            cursor.execute('''
                DELETE FROM transfer_performance 
                WHERE date < ?
            ''', (cutoff_date.strftime('%Y-%m-%d'),))
            
            # Vacuum database to reclaim space
            cursor.execute('VACUUM')
            conn.close()
            
            new_size = self.db_path.stat().st_size
            space_saved = (original_size - new_size) / (1024 * 1024)
            
            result["space_freed_mb"] = space_saved
            result["optimization_applied"] = True
            
        except Exception as e:
            logger.error(f"Database optimization error: {e}")
        
        return result
    
    def get_storage_health_report(self) -> dict:
        """Get comprehensive storage health report"""
        current_usage = self.get_current_storage_usage()
        projection = self.project_6_month_storage()
        
        health_score = 100
        health_issues = []
        
        # Check current usage
        if current_usage["total_gb"] > self.warning_threshold_gb:
            health_score -= 30
            health_issues.append("Current storage usage exceeds warning threshold")
        
        # Check projection
        if projection["projected_6month_gb"] > self.max_storage_gb:
            health_score -= 40
            health_issues.append("6-month projection exceeds maximum storage limit")
        elif projection["projected_6month_gb"] > self.warning_threshold_gb:
            health_score -= 20
            health_issues.append("6-month projection approaches storage limit")
        
        # Check cleanup needs
        if projection["optimization_needed"]:
            health_score -= 10
            health_issues.append("Storage optimization recommended")
        
        return {
            "health_score": max(0, health_score),
            "health_status": "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical",
            "health_issues": health_issues,
            "current_usage": current_usage,
            "6_month_projection": projection,
            "recommendations": projection["cleanup_recommendation"]
        }


# Integration with transfer learning lifecycle
def integrate_storage_management():
    """Integration example"""
    storage_manager = StorageManager()
    
    # Get health report
    health_report = storage_manager.get_storage_health_report()
    print(f"📊 Storage Health: {health_report['health_status']} ({health_report['health_score']}/100)")
    print(f"💾 Current Usage: {health_report['current_usage']['total_gb']:.1f} GB")
    print(f"📈 6-Month Projection: {health_report['6_month_projection']['projected_6month_gb']:.1f} GB")
    
    # Optimize if needed
    if health_report["6_month_projection"]["optimization_needed"]:
        print("🔧 Running storage optimization...")
        optimization = storage_manager.optimize_storage()
        print(f"✅ Optimization complete: {optimization['space_freed_mb']:.1f} MB freed")
    
    return storage_manager


if __name__ == "__main__":
    storage_manager = integrate_storage_management()
