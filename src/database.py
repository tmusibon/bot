import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (id INTEGER PRIMARY KEY,
                  token_address TEXT,
                  entry_price REAL,
                  entry_time TIMESTAMP,
                  exit_price REAL,
                  exit_time TIMESTAMP,
                  status TEXT,
                  profit_loss REAL)''')
    conn.commit()
    conn.close()

def add_trade(token_address: str, entry_price: float):
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    c.execute('''INSERT INTO trades 
                 (token_address, entry_price, entry_time, status)
                 VALUES (?, ?, ?, ?)''',
              (token_address, entry_price, datetime.now(), 'OPEN'))
    conn.commit()
    conn.close()

def update_trade(trade_id: int, exit_price: float):
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    
    # First get the entry price to calculate profit/loss
    c.execute('SELECT entry_price FROM trades WHERE id = ?', (trade_id,))
    result = c.fetchone()
    if result:
        entry_price = result[0]
        profit_loss = ((exit_price - entry_price) / entry_price) * 100
        
        c.execute('''UPDATE trades 
                     SET exit_price = ?, 
                         exit_time = ?,
                         status = ?,
                         profit_loss = ?
                     WHERE id = ?''',
                  (exit_price, datetime.now(), 'CLOSED', profit_loss, trade_id))
        conn.commit()
    conn.close()

def get_active_trades():
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM trades WHERE status = ?', ('OPEN',))
    trades = c.fetchall()
    conn.close()
    return trades

def get_trade_history():
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM trades WHERE status = ?', ('CLOSED',))
    trades = c.fetchall()
    conn.close()
    return trades
