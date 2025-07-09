import base64
import io
import json
import logging
import pandas as pd
import requests


def make_api_call(url, method="GET", data=None, params=None, timeout=10):
    """
    Generic API call function for making requests to the backend
    """
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=timeout)
        elif method.upper() == "DELETE":
            response = requests.delete(url, timeout=timeout)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}
        
        response.raise_for_status()
        
        # Try to parse JSON response
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"text": response.text}
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error - check if backend is running"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def fetch_model_logs():
    try:
        r = requests.get("http://localhost:5000/model/logs")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return []

def fetch_model_errors():
    try:
        r = requests.get("http://localhost:5000/model/errors")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return []

def batch_predict_from_csv(contents):
    """Accepts Dash upload contents, decodes, parses CSV, and sends to backend for batch prediction."""
    try:
        print("[DEBUG] Starting batch_predict_from_csv")
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        print("[DEBUG] Decoded CSV, length:", len(decoded))
        # Save to temp file for upload
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(decoded)
            tmp_path = tmp.name
        print(f"[DEBUG] Temp file saved at {tmp_path}")
        # Upload to backend for retraining
        with open(tmp_path, 'rb') as f:
            files = {'file': ('uploaded.csv', f, 'text/csv')}
            retrain_resp = requests.post("http://localhost:5000/model/upload_and_retrain", files=files)
        print(f"[DEBUG] Retrain response: {retrain_resp.status_code} {retrain_resp.text}")
        # Check retrain status
        if retrain_resp.status_code != 200:
            return {"error": f"Retrain failed: {retrain_resp.text}"}
        retrain_result = retrain_resp.json()
        if retrain_result.get('status') != 'success':
            return {"error": f"Retrain error: {retrain_result.get('stderr', '')}"}
        # Now run batch prediction with the same data
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        data = df.to_dict(orient='records')
        r = requests.post("http://localhost:5000/model/predict_batch", json=data)
        print(f"[DEBUG] Batch prediction response: {r.status_code} {r.text}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Exception in batch_predict_from_csv: {e}")
        return {"error": str(e)}

def open_trade(symbol, direction, amount, entry_price, tp_pct, sl_pct):
    try:
        r = requests.post("http://localhost:5000/trade", json={
            "symbol": symbol,
            "direction": direction,
            "amount": amount,
            "entry_price": entry_price,
            "tp_pct": tp_pct,
            "sl_pct": sl_pct
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def fetch_notifications():
    try:
        r = requests.get("http://localhost:5000/notifications")
        r.raise_for_status()
        return r.json()
    except Exception:
        return []

def run_backtest(symbol, initial_capital):
    try:
        # For demo, send empty data. In production, send real price data.
        r = requests.post("http://localhost:5000/backtest", json={
            "symbol": symbol,
            "data": [],
            "initial_capital": initial_capital
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def fetch_backtests():
    try:
        r = requests.get("http://localhost:5000/backtest/results")
        r.raise_for_status()
        return r.json()
    except Exception:
        return []

def fetch_ml_prediction(features):
    try:
        r = requests.post("http://localhost:5000/model/predict_batch", json=[features])
        r.raise_for_status()
        results = r.json().get("results", [{}])
        return results[0] if results else {"mean": None, "per_model": {}, "agreement": None}
    except Exception:
        return {"mean": None, "per_model": {}, "agreement": None}

def fetch_analytics():
    try:
        r = requests.get("http://localhost:5000/trades/analytics")
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"win_rate": None, "avg_pnl": None, "sharpe": None}


def fetch_trades():
    try:
        r = requests.get("http://localhost:5000/trades")
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


# --- Trade Management API Helpers ---
def close_trade(trade_id, close_price):
    try:
        r = requests.post(f"http://localhost:5000/trades/{trade_id}/close", params={"close_price": close_price})
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"error": "Failed to close trade"}

def cancel_trade(trade_id):
    try:
        r = requests.post(f"http://localhost:5000/trades/{trade_id}/cancel")
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"error": "Failed to cancel trade"}

def activate_trade(trade_id):
    try:
        r = requests.post(f"http://localhost:5000/trades/{trade_id}/activate")
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"error": "Failed to activate trade"}


# --- Safety Check API Helper ---
def safety_check(symbol, direction, amount, entry_price, tp_pct, sl_pct):
    try:
        payload = {
            "symbol": symbol,
            "direction": direction,
            "amount": amount,
            "entry_price": entry_price,
            "tp_pct": tp_pct,
            "sl_pct": sl_pct
        }
        r = requests.post("http://localhost:5000/safety/check", json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"ok": False, "warnings": [f"Error: {e}"], "errors": [str(e)]}


# --- Advanced Analytics API Helper ---
def fetch_portfolio_analytics():
    try:
        r = requests.get("http://localhost:5000/trades/analytics")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# --- Model Feature Importance API Helper ---
def fetch_feature_importance():
    try:
        r = requests.get("http://localhost:5000/model/feature_importance")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# --- Model Metrics API Helper ---
def fetch_model_metrics():
    try:
        r = requests.get("http://localhost:5000/model/metrics")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# --- Notification Management API Helpers ---
def mark_notification_read(notification_id):
    try:
        r = requests.post("http://localhost:5000/notifications/mark_read", json=notification_id)
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}
    except Exception as e:
        return {"error": str(e)}

def delete_notification(notification_id):
    try:
        r = requests.delete(f"http://localhost:5000/notifications/{notification_id}")
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}
    except Exception as e:
        return {"error": str(e)}

# --- System Status API Helper ---
def fetch_system_status():
    try:
        r = requests.get("http://localhost:5000/system/status")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

