from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Mock data - formatted according to README specification
mock_data = [
    {
        "city": "بغداد / الكفاح",
        "buy_price": 146750,  # Using integer/float is better for prices
        "sell_price": 147000,
        "last_updated": "2025-04-24T10:30:00" # ISO 8601 format
    },
    {
        "city": "أربيل",
        "buy_price": 147050,
        "sell_price": 147300,
        "last_updated": "2025-04-24T10:30:00"
    },
    {
        "city": "البصرة",
        "buy_price": 146800,
        "sell_price": 147100,
        "last_updated": "2025-04-24T10:30:00"
    },
    {
        "city": "السعر الرسمي",
        "buy_price": 1310,
        "sell_price": 1310,
        "last_updated": "2025-04-24T00:00:00" # Example timestamp for official rate
    }
]

@app.get("/api/rates")
async def get_rates():
    # In the future, this will fetch data from the scraper/database
    return mock_data

# To run the server (from the 'backend' directory):
# uvicorn main:app --reload
