import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import logging

logger = logging.getLogger(__name__)

# Email configuration file path
EMAIL_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'email_config.json')

def get_email_config():
    """Get email configuration from file or environment variables"""
    config = {}
    
    # Try to load from config file first
    if os.path.exists(EMAIL_CONFIG_PATH):
        try:
            with open(EMAIL_CONFIG_PATH, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load email config file: {e}")
    
    # Fill in missing values from environment variables or defaults
    return {
        'smtp_server': config.get('smtp_server', os.environ.get("SMTP_SERVER", "smtp.gmail.com")),
        'smtp_port': int(config.get('smtp_port', os.environ.get("SMTP_PORT", 587))),
        'smtp_user': config.get('smtp_user', os.environ.get("SMTP_USER", "")),
        'smtp_pass': config.get('smtp_pass', os.environ.get("SMTP_PASS", "")),
        'from_email': config.get('from_email', config.get('smtp_user', os.environ.get("SMTP_USER", ""))),
        'to_email': config.get('to_email', os.environ.get("NOTIFY_EMAIL", "")),
        'enabled': config.get('enabled', False)
    }

def save_email_config(config):
    """Save email configuration to file"""
    try:
        os.makedirs(os.path.dirname(EMAIL_CONFIG_PATH), exist_ok=True)
        with open(EMAIL_CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Could not save email config: {e}")
        return False

def test_email_connection():
    """Test email configuration by attempting to connect"""
    config = get_email_config()
    
    if not config['enabled'] or not config['smtp_user'] or not config['smtp_pass']:
        return {'success': False, 'message': 'Email not configured or disabled'}
    
    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['smtp_user'], config['smtp_pass'])
        return {'success': True, 'message': 'Email connection successful'}
    except Exception as e:
        return {'success': False, 'message': f'Email connection failed: {str(e)}'}

def send_email(subject, body, to_email=None):
    """Send email notification"""
    config = get_email_config()
    
    if not config['enabled']:
        logger.info("Email notifications disabled")
        return {'success': False, 'message': 'Email notifications disabled'}
    
    if not config['smtp_user'] or not config['smtp_pass']:
        logger.warning("Email not properly configured")
        return {'success': False, 'message': 'Email not properly configured'}
    
    recipient = to_email or config['to_email'] or config['smtp_user']
    
    try:
        msg = MIMEMultipart()
        msg["From"] = config['from_email']
        msg["To"] = recipient
        msg["Subject"] = f"[Crypto Bot] {subject}"
        
        # Create HTML body with professional styling
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ padding: 10px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🤖 Crypto Trading Bot Notification</h2>
            </div>
            <div class="content">
                <h3>{subject}</h3>
                <p>{body}</p>
                <p><small>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </div>
            <div class="footer">
                <p>This is an automated message from your Crypto Trading Bot</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, "html"))
        msg.attach(MIMEText(body, "plain"))  # Fallback plain text
        
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['smtp_user'], config['smtp_pass'])
            server.sendmail(config['from_email'], recipient, msg.as_string())
        
        logger.info(f"Email sent successfully to {recipient}")
        return {'success': True, 'message': f'Email sent to {recipient}'}
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return {'success': False, 'message': f'Failed to send email: {str(e)}'}

def send_trade_notification(trade_data):
    """Send notification for trade events"""
    subject = f"Trade {trade_data.get('status', 'UPDATE')} - {trade_data.get('symbol', 'N/A')}"
    
    body = f"""
    Trade Details:
    - Symbol: {trade_data.get('symbol', 'N/A')}
    - Direction: {trade_data.get('direction', 'N/A')}
    - Status: {trade_data.get('status', 'N/A')}
    - Entry Price: ${trade_data.get('entry_price', 0):.2f}
    - Current Price: ${trade_data.get('current_price', 0):.2f}
    - P&L: ${trade_data.get('pnl', 0):.2f}
    """
    
    return send_email(subject, body)

def send_system_notification(event_type, message, details=None):
    """Send system event notifications"""
    subject = f"System {event_type}"
    
    body = f"""
    System Event: {event_type}
    Message: {message}
    """
    
    if details:
        body += f"\nDetails:\n{details}"
    
    return send_email(subject, body)

# Import datetime for timestamps
from datetime import datetime
