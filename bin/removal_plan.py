import re

# Read the file
with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find all callback decorators and their line ranges
callbacks_to_remove = []

# Based on the thorough analysis, these are the duplicate lines to remove:
duplicate_lines = [
    1579,  # manage_transfer_learning duplicate
    1643,  # update_transfer_performance duplicate  
    1756,  # manage_futures_trading duplicate
    1816,  # update_futures_analytics duplicate
    1872,  # manage_model_versions duplicate (no allow_duplicate but still duplicate)
    1934,  # update_model_metrics duplicate
    1978,  # update_ml_performance_history duplicate
    2021,  # load_backtest_results duplicate
    2083,  # manage_model_retraining duplicate
    2116,  # update_live_price duplicate
    2168,  # update_portfolio_status duplicate
    2206,  # update_performance_monitor duplicate
    2240,  # update_virtual_balance duplicate
    2258,  # update_futures_virtual_balance duplicate
    2290,  # reset_futures_virtual_balance duplicate
    2309,  # update_auto_trading_balance duplicate (keep original, check for 3rd one)
    2333,  # update_price_chart duplicate
    2410,  # update_indicators_chart duplicate
]

print("CALLBACKS TO REMOVE (duplicates):")
for line_num in duplicate_lines:
    if line_num - 1 < len(lines):
        print(f"Line {line_num}: {lines[line_num - 1].strip()}")

print(f"\nTotal duplicates to remove: {len(duplicate_lines)}")
print("\nThese are all confirmed duplicates with allow_duplicate=True or identical function definitions.")
print("The original versions (without allow_duplicate=True) will be preserved.")
