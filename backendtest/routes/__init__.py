"""
Routes Package
Contains all API route modules for the backend
"""

from .risk_management_routes import router as risk_management_router
from .email_alert_routes import router as email_alert_router
from .advanced_auto_trading_routes import router as advanced_auto_trading_router, set_engine_instance
from .ml_prediction_routes import router as ml_prediction_router, set_dependencies as set_ml_dependencies
from .settings_notifications_routes import (
    settings_router, 
    notifications_router, 
    notify_router,
    set_notification_dependencies
)
from .system_routes import router as system_router, set_system_dependencies
from .hft_analysis_routes import router as hft_analysis_router
from .data_collection_routes import router as data_collection_router, set_data_dependencies
from .futures_trading_routes import router as futures_trading_router, set_futures_dependencies
from .spot_trading_routes import router as spot_trading_router
from .market_data_routes import router as market_data_router
from .auto_trading_routes import router as auto_trading_router
from .simple_ml_routes import router as simple_ml_router

__all__ = [
    "advanced_auto_trading_router",
    "ml_prediction_router", 
    "settings_router",
    "notifications_router",
    "notify_router",
    "system_router",
    "hft_analysis_router",
    "data_collection_router", 
    "futures_trading_router",
    "risk_management_router",
    "email_alert_router",
    "spot_trading_router",
    "market_data_router", 
    "auto_trading_router",
    "simple_ml_router",
    "set_engine_instance",
    "set_ml_dependencies",
    "set_notification_dependencies",
    "set_system_dependencies",
    "set_data_dependencies",
    "set_futures_dependencies"
]
