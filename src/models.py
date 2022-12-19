from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from database import Base

class TaxiZone(Base):
    __tablename__ = "taxi_zone_lookup"

    locationID = Column(Integer, primary_key = True)
    borough = Column(String(255))
    zone = Column(String(255))

class UberTrip(Base):
    __tablename__ = "uber_sep"

    id = Column(Integer, primary_key = True)
    date_time = Column(Date)
    lat = Column(String(255))
    lon = Column(String(255))
    base = Column(String(255))

class RawTrip(Base):
    __tablename__ = "uber_raw_data"

    id = Column(Integer, primary_key = True)
    dispatching_base_num = Column(String(255))
    pickup_date = Column(Date)
    affiliated_base_num = Column(String(255))
    locationID = Column(Integer)


