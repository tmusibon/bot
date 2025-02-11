import sqlite3

def init_db():
    conn = sqlite3.connect('trading_bot.db')
    c = conn.cursor()
    
    # Create trades table
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            token_address TEXT,
            amount REAL,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create watchlist table
    c.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            token_address TEXT,
            alert_price REAL
        )
    ''')
    
    conn.commit()
    conn.close()
