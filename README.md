# Project: Live Dollar Price Display in Iraq

## Project Description:
Create a website that displays the exchange rates of the US Dollar against the Iraqi Dinar, based **solely on reliable sources** within Iraq. The site should only display actual rates from real sources, without using any AI for prediction or analysis.

---

## Required Features:

### 1. User Interface (Frontend):
- A table displaying cities (e.g., Baghdad, Basra, Erbil).
- Columns: Buy Price – Sell Price – Last Updated Time.
- Lightweight design using TailwindCSS or Bootstrap.
- Full support for Arabic language (Right-to-Left layout).
- Responsive design (works on mobile and desktop).

### 2. Data Source:
- Utilize Web Scraping or APIs to fetch rates from:
  - Central Bank of Iraq website: https://cbi.iq
  - Reliable channels like [@dollariraqi](https://t.me/dollariraqi) on Telegram.
  - Trusted Iraqi news websites (e.g., Shafaq News, Al Muraa News).

### 3. Backend API:
- Preferred technologies: FastAPI (Python) or Express (Node.js).
- An API route providing data in JSON format to the frontend.
- Local caching of updates to minimize load on source websites/APIs.
- Automated job (CRON) to update data every 10 minutes.

### 4. Data Storage:
- A simple database (SQLite, MongoDB, or even a JSON file).
- Store the latest prices along with their update timestamps.

### 5. Deployment:
- Frontend: Deploy using Vercel or Netlify.
- Backend: Deploy using Render or Railway.

---

## Example API JSON Response Format:
```json
[
  {
    "city": "بغداد / الكفاح",
    "buy_price": 146750,
    "sell_price": 147000,
    "last_updated": "2025-04-24T10:30:00"
  },
  {
    "city": "أربيل",
    "buy_price": 147050,
    "sell_price": 147300,
    "last_updated": "2025-04-24T10:30:00"
  },
  {
    "city": "السعر الرسمي",
    "buy_price": 1310,
    "sell_price": 1310,
    "last_updated": "2025-04-24T10:30:00" // Example timestamp
  }
]
```

---

## Additional Requirements:
- Display the source of the price below each table or entry.
- Clearly show the last update time.
- Implement measures against IP blocking (e.g., appropriate user-agents, proxies if necessary).

---

## Future Enhancements (Optional):
- Support for other currencies (Euro, Turkish Lira).
- A simple mobile application.
- Price change notifications (via Telegram Bot or web notifications).
