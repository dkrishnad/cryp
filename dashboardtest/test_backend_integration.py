import requests

API_URL = "http://localhost:8000"

def test_backend_health():
    endpoints = [
        ("/trades", "GET"),
        ("/backtest/results", "GET"),
        ("/notifications", "GET"),
        ("/trades/analytics", "GET"),
        ("/predict", "POST"),
        ("/trade", "POST"),
        ("/backtest", "POST"),
    ]
    test_payloads = {
        "/predict": {"data": {"amount": 1, "entry_price": 50000, "tp_pct": 2, "sl_pct": 1}},
        "/trade": {"id": 0, "symbol": "BTCUSDT", "direction": "LONG", "amount": 0.1, "entry_price": 50000, "tp_pct": 2, "sl_pct": 1},
        "/backtest": {"symbol": "BTCUSDT", "data": [50000, 50100, 50200], "initial_capital": 10000},
    }
    for endpoint, method in endpoints:
        url = API_URL + endpoint
        try:
            if method == "GET":
                r = requests.get(url)
            else:
                payload = test_payloads.get(endpoint, {})
                r = requests.post(url, json=payload)
            print(f"{method} {endpoint}: {r.status_code} {r.reason}")
            if r.ok:
                print("  Response:", r.json())
            else:
                print("  Error:", r.text)
        except Exception as e:
            print(f"{method} {endpoint}: Exception {e}")

if __name__ == "__main__":
    test_backend_health()
