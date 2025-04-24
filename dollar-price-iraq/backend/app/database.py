import sqlite3

DATABASE_URL = "dollar_prices.db"

def create_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    return conn

def create_table():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            city TEXT PRIMARY KEY,
            buy_price REAL,
            sell_price REAL,
            last_updated TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_rates(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("SELECT city, buy_price, sell_price, last_updated, source FROM prices")
    rows = cursor.fetchall()

    # Convert rows to JSON format
    rates = []
    for row in rows:
        city, buy_price, sell_price, last_updated, source = row
        rates.append({
            "city": city,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "last_updated": last_updated,
            "source": source
        })
    return rates
