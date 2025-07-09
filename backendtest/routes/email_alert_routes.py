"""
Email and Alert Management Routes
"""
from fastapi import APIRouter, Body
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter(prefix="/email", tags=["Email Management"])

# Email configuration store
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "",
    "password": "",
    "enabled": False
}

@router.get("/config")
async def get_email_config():
    """Get current email configuration"""
    try:
        config = EMAIL_CONFIG.copy()
        config.pop("password", None)  # Don't return password
        return {"status": "success", "config": config}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/config")
async def update_email_config(config: dict = Body(...)):
    """Update email configuration"""
    try:
        EMAIL_CONFIG.update(config)
        return {"status": "success", "message": "Email configuration updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/test")
async def test_email_connection():
    """Test email connection"""
    try:
        if not EMAIL_CONFIG["email"] or not EMAIL_CONFIG["password"]:
            return {"status": "error", "message": "Email credentials not configured"}
        
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        server.quit()
        
        return {"status": "success", "message": "Email connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Email test failed: {str(e)}"}
