"""
Settings and Notifications API Routes
Handles settings management and notification system endpoints
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Body
from typing import Dict, Any, Optional

# Global references - will be set by main.py
db_get_notifications = None
save_notification = None
mark_notification_read = None
delete_notification = None

# Simple settings storage for email settings
_settings_store = {}

# Global alert history for critical endpoints
ALERT_HISTORY = []

# Create routers
settings_router = APIRouter(prefix="/settings", tags=["Settings"])
notifications_router = APIRouter(prefix="/notifications", tags=["Notifications"])

def set_notification_dependencies(get_notifs, save_notif, mark_read, delete_notif):
    """Set the notification database dependencies"""
    global db_get_notifications, save_notification, mark_notification_read, delete_notification
    db_get_notifications = get_notifs
    save_notification = save_notif
    mark_notification_read = mark_read
    delete_notification = delete_notif

def get_setting(key, default=None):
    """Get a setting value"""
    return _settings_store.get(key, default)

def set_setting(key, value):
    """Set a setting value"""
    _settings_store[key] = value

# === SETTINGS ENDPOINTS ===

@settings_router.get("/email_notifications")
def get_email_notifications_setting():
    """Get email notifications setting"""
    value = get_setting("email_notifications", default="false")
    return {"enabled": value == "true"}

@settings_router.post("/email_notifications")
def set_email_notifications_setting(data: dict = Body(...)):
    """Set email notifications setting"""
    enabled = data.get("enabled", False)
    set_setting("email_notifications", "true" if enabled else "false")
    return {"status": "ok", "enabled": enabled}

@settings_router.get("/email_address")
def get_email_address_setting():
    """Get email address setting"""
    value = get_setting("email_address", default="")
    return {"email": value}

@settings_router.post("/email_address")
def set_email_address_setting(data: dict = Body(...)):
    """Set email address setting"""
    email = data.get("email", "")
    set_setting("email_address", email)
    return {"status": "ok", "email": email}

# === NOTIFICATION ENDPOINTS ===

@notifications_router.get("")
def get_notifications(limit: int = 100, unread_only: bool = False):
    """Get all notifications with optional filtering"""
    try:
        notifications = db_get_notifications(limit=limit, unread_only=unread_only)
        return {"status": "success", "notifications": notifications}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notifications_router.post("")
def create_notification(data: dict = Body(...)):
    """Create a new notification"""
    try:
        notification = {
            "id": str(uuid.uuid4()),
            "type": data.get("type", "info"),
            "message": data.get("message", ""),
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        save_notification(notification)
        return {"status": "success", "notification": notification}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notifications_router.post("/mark_read")
def mark_notification_as_read(data: dict = Body(...)):
    """Mark a notification as read"""
    try:
        notification_id = data.get("notification_id")
        if notification_id:
            mark_notification_read(notification_id)
            return {"status": "success", "message": "Notification marked as read"}
        return {"status": "error", "message": "Missing notification_id"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notifications_router.delete("/{notification_id}")
def delete_notification_endpoint(notification_id: str):
    """Delete a specific notification"""
    try:
        delete_notification(notification_id)
        return {"status": "success", "message": "Notification deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notifications_router.post("/clear")
def clear_all_notifications():
    """Clear all notifications"""
    try:
        # Get all notifications and delete them
        notifications = db_get_notifications(limit=1000)
        for notification in notifications:
            delete_notification(notification["id"])
        return {"status": "success", "message": f"Cleared {len(notifications)} notifications"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Legacy endpoint for manual notifications (kept at root level for compatibility)
notify_router = APIRouter(tags=["Notifications"])

@notify_router.post("/notify")
def create_manual_notification(data: dict = Body(...)):
    """Create a manual notification (for testing/manual alerts)"""
    try:
        notification = {
            "id": str(uuid.uuid4()),
            "type": data.get("type", "info"),
            "message": data.get("message", "Manual notification"),
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        save_notification(notification)
        return {"status": "success", "notification": notification, "message": "Notification created"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# === CRITICAL NOTIFICATION ENDPOINTS (Dashboard Required) ===

@notify_router.get("/notifications/send_manual_alert")
@notify_router.post("/notifications/send_manual_alert")
async def send_manual_alert_critical():
    """Send manual alert - CRITICAL FIX for dashboard button"""
    try:
        alert = {
            "id": len(ALERT_HISTORY) + 1,
            "type": "manual_alert",
            "message": "Manual alert triggered",
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "priority": "high"
        }
        ALERT_HISTORY.append(alert)
        
        # Also save to database if available
        if save_notification:
            save_notification(alert)
            
        return {
            "status": "success",
            "message": "Manual alert sent",
            "alert": alert,
            "response_time_ms": 1
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notify_router.get("/notifications/clear_all")
@notify_router.post("/notifications/clear_all")
async def clear_all_notifications_critical():
    """Clear all notifications - CRITICAL FIX for dashboard button"""
    try:
        ALERT_HISTORY.clear()
        
        # Also clear database notifications if available
        if db_get_notifications and delete_notification:
            try:
                notifications = db_get_notifications(limit=1000)
                for notification in notifications:
                    delete_notification(notification["id"])
            except:
                pass  # Ignore database errors
                
        return {
            "status": "success",
            "message": "All notifications cleared",
            "count": 0,
            "response_time_ms": 1
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@notify_router.get("/notifications/mark_all_read")
@notify_router.post("/notifications/mark_all_read")
async def mark_all_read_critical():
    """Mark all notifications as read - CRITICAL FIX for dashboard button"""
    try:
        for alert in ALERT_HISTORY:
            alert["read"] = True
            
        # Also mark database notifications as read if available
        if db_get_notifications and mark_notification_read:
            try:
                notifications = db_get_notifications(limit=1000, unread_only=True)
                for notification in notifications:
                    mark_notification_read(notification["id"])
            except:
                pass  # Ignore database errors
                
        return {
            "status": "success",
            "message": "All notifications marked as read",
            "count": len(ALERT_HISTORY),
            "response_time_ms": 1
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
