import uuid
import datetime
from db import save_trade

def open_virtual_trade(symbol, direction, amount, price, tp_pct, sl_pct):
    trade_id = str(uuid.uuid4())
    tp_price = price * (1 + tp_pct/100) if direction == "LONG" else price * (1 - tp_pct/100)
    sl_price = price * (1 - sl_pct/100) if direction == "LONG" else price * (1 + sl_pct/100)
    trade = {
        'id': trade_id,
        'symbol': symbol,
        'direction': direction,
        'amount': amount,
        'entry_price': price,
        'tp_price': tp_price,
        'sl_price': sl_price,
        'status': 'OPEN',
        'open_time': str(datetime.datetime.now()),
        'close_time': None,
        'pnl': 0.0,
        'current_price': price,
        'close_price': None
    }
    save_trade(trade)
    return trade_id
