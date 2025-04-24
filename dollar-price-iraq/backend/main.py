from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
from bs4 import BeautifulSoup
import sqlite3
import json
from datetime import datetime

app = FastAPI()

# Allow CORS for frontend development
origins = ["*"]  # Restrict in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
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

# Scraping functions
async def scrape_cbi():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://cbi.iq")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract data based on CBI website structure (adjust as needed)
            # Example:
            # buy_price = soup.find("span", {"class": "buy-price"}).text
            # sell_price = soup.find("span", {"class": "sell-price"}).text
            # For now, return dummy data
            return {"buy_price": 1310, "sell_price": 1310, "source": "cbi.iq"}
    except httpx.HTTPError as e:
        print(f"HTTPError while scraping CBI: {e}")
        return None
    except Exception as e:
        print(f"Error while scraping CBI: {e}")
        return None

async def scrape_dollariraqi():
    try:
        # Telegram scraping is complex and may require a dedicated library or API
        # For demonstration purposes, return dummy data
        return {"buy_price": 147000, "sell_price": 147300, "source": "dollariraqi"}
    except Exception as e:
        print(f"Error while scraping dollariraqi: {e}")
        return None

# Data update function
async def update_data():
    create_table()
    cbi_data = await scrape_cbi()
    dollariraqi_data = await scrape_dollariraqi()

    conn = create_db_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    if cbi_data:
        cursor.execute("""
            INSERT OR REPLACE INTO prices (city, buy_price, sell_price, last_updated, source)
            VALUES (?, ?, ?, ?, ?)
        """, ("السعر الرسمي", cbi_data["buy_price"], cbi_data["sell_price"], now, cbi_data["source"]))

    if dollariraqi_data:
        cursor.execute("""
            INSERT OR REPLACE INTO prices (city, buy_price, sell_price, last_updated, source)
            VALUES (?, ?, ?, ?, ?)
        """, ("بغداد / الكفاح", dollariraqi_data["buy_price"], dollariraqi_data["sell_price"], now, dollariraqi_data["source"]))

    conn.commit()
    conn.close()

# API endpoint
@app.get("/api/rates")
async def get_rates():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city, buy_price, sell_price, last_updated, source FROM prices")
    rows = cursor.fetchall()
    conn.close()

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

# Schedule the data updates
scheduler = AsyncIOScheduler()
scheduler.add_job(update_data, "interval", minutes=10)

@app.on_event("startup")
async def startup_event():
    create_table()
    scheduler.start()

# To run the server (from the 'backend' directory):
# uvicorn main:app --reload
