

import joblib
import numpy as np
import os
import threading

MODEL_PATH = os.path.join(os.path.dirname(__file__), "kaia_rf_model.joblib")
_model = None
_model_lock = threading.Lock()

def load_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                if os.path.exists(MODEL_PATH):
                    try:
                        _model = joblib.load(MODEL_PATH)
                    except Exception as e:
                        print(f"[ML ERROR] Failed to load model: {e}")
                        _model = None
                else:
                    print(f"[ML ERROR] Model file not found at {MODEL_PATH}")
                    _model = None
    return _model

def real_predict(row):
    mdl = load_model()
    if mdl is None:
        return "NO_MODEL", 0.0
    feature_cols = [
        'open', 'high', 'low', 'close', 'volume', 'rsi', 'stoch_k', 'stoch_d', 'williams_r', 'roc', 'ao',
        'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
    ]
    try:
        X = np.array([[row.get(col, 0) for col in feature_cols]])
        pred = mdl.predict(X)[0]
        prob = mdl.predict_proba(X)[0][1] if hasattr(mdl, 'predict_proba') else 0.0
        return ("LONG" if pred else "SHORT"), float(prob)
    except Exception as e:
        print(f"[ML ERROR] Prediction failed: {e}")
        return "ERROR", 0.0
