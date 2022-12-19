from datetime import date
from pydantic import BaseModel

class TaxiZone(BaseModel):
    locationID: int
    borough: str
    zone: str

    class Config:
        orm_mode = True

class UberTrip(BaseModel):
    id: int
    date_time: date
    lat: str
    lon: str
    base: str

    class Config:
        orm_mode = True

class RawTrip(BaseModel):
    id: int
    dispatching_base_num: str
    pickup_date: date
    affiliated_base_num: str
    locationID: int

    class Config:
        orm_mode = True