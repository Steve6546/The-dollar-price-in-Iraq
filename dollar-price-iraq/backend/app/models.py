from pydantic import BaseModel

class Price(BaseModel):
    city: str
    buy_price: float
    sell_price: float
    last_updated: str
    source: str
