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

# Mock data - same as frontend for initial setup
mock_data = [
    {
        "city": "بغداد / الكفاح",
        "buy": "146,750",
        "sell": "147,000",
        "updated": "2025-04-24 10:30 AM"
    },
    {
        "city": "أربيل",
        "buy": "147,050",
        "sell": "147,300", 
        "updated": "2025-04-24 10:30 AM"
    },
    {
        "city": "البصرة",
        "buy": "146,800",
        "sell": "147,100",
        "updated": "2025-04-24 10:30 AM"
    },
    {
        "city": "السعر الرسمي",
        "buy": "1,310",
        "sell": "1,310",
        "updated": "البنك المركزي"
    }
]

@app.get("/api/rates")
async def get_rates():
    # In the future, this will fetch data from the scraper/database
    return mock_data

# To run the server (from the 'backend' directory):
# uvicorn main:app --reload
