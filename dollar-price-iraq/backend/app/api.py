from fastapi import APIRouter, Depends
from typing import List
from . import database, models

router = APIRouter()

@router.get("/rates", response_model=List[models.Price])
async def get_rates(db=Depends(database.get_db)):
    """
    Get all dollar exchange rates.
    """
    rates = database.get_rates(db)
    return rates
