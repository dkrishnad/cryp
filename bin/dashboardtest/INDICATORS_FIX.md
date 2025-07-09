# Technical Indicators Update Fix

## Issue Identified:
The technical indicators were showing but not updating when switching between different coins in the dropdown.

## Root Cause:
The `update_technical_indicators` callback had an unnecessary dependency on `live-price-cache` data:

```python
# PROBLEMATIC (before fix):
@app.callback(
    [Output('current-regime', 'children'), ...],
    [Input('selected-symbol-store', 'data'),
     Input('live-price-cache', 'data'),        # <-- UNNECESSARY DEPENDENCY
     Input('interval-indicators', 'n_intervals')],
    prevent_initial_call=False
)
def update_technical_indicators(symbol_data, price_cache, n_intervals):
```

## The Problem:
1. When user changes symbol dropdown, it triggers `sync_selected_symbol`
2. This updates `selected-symbol-store` 
3. The `update_technical_indicators` callback should trigger
4. BUT it also waits for `live-price-cache` to update
5. If there's any delay or issue with the price cache update, the indicators won't update

## The Fix:
Removed the unnecessary `live-price-cache` dependency:

```python
# FIXED (after fix):
@app.callback(
    [Output('current-regime', 'children'), ...],
    [Input('selected-symbol-store', 'data'),
     Input('interval-indicators', 'n_intervals')],  # <-- REMOVED price_cache dependency
    prevent_initial_call=False
)
def update_technical_indicators(symbol_data, n_intervals):
```

## Expected Behavior After Fix:
1. User selects symbol from dropdown → `sync_selected_symbol` triggers
2. `selected-symbol-store` updates → `update_technical_indicators` triggers immediately  
3. Backend returns different values for different symbols:
   - **BTCUSDT**: Regime="Sideways", RSI=55.1
   - **KAIAUSDT**: Regime="Bullish", RSI=65.2  
   - **Others**: Regime="Neutral", RSI=50.0
4. Technical indicators display updates instantly

## Testing:
1. Start dashboard: `python app.py`
2. Open http://localhost:8050
3. Change symbol dropdown and verify indicators update
4. Watch console for debug messages confirming callback triggers

This fix ensures technical indicators update immediately when symbols are changed, without waiting for unrelated price cache updates.
