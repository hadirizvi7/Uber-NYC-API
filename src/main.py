from tracemalloc import start
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import extract
from starlette.responses import RedirectResponse
import models, schemas
from database import SessionLocal, engine
from typing import List
from fastapi import Depends, FastAPI, HTTPException
import datetime
from models import RawTrip, TaxiZone

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    
    finally:
        db.close()

def days_in_month():
    return {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30
    }

@app.get("/")
async def main():
    return RedirectResponse(url="/docs/")

@app.get("/numPerBorough/{borough}")
async def numberOfRidesPerBorough(inputBorough: str, db: Session = Depends(get_db)):
    boroughList = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']

    if inputBorough not in boroughList:
        msg = "Invalid Input"
        print(msg)
        return msg
    
    zoneQuery = db.query(models.TaxiZone).filter_by(borough = inputBorough).all()
    locationIdSet = set()

    for zone in zoneQuery:
        locationIdSet.add(zone.locationID)
    
    output = 0
    for id in locationIdSet:
        query = db.query(models.RawTrip).filter_by(locationID = id).all()
        output += len(query)
    
    return output

@app.get("/numRidesInRange/{startDate}/{endDate}")
async def numRidesInRange(startDate, endDate, db: Session = Depends(get_db)):
    #Sample timestamp from PostgreSQL: 2015-03-28 15:24:00 
    date_format = '%Y-%m-%d'
    try:
        startDate = datetime.datetime.strptime(startDate, date_format)
        endDate = datetime.datetime.strptime(endDate, date_format)

    except ValueError:
        msg = "Incorrect data format, should be YYYY-MM-DD"
        print(msg)
        return msg
    
    startDate = startDate + datetime.timedelta(0, 0, 0, 0, 0, 0, 0) # "00:00:00"
    endDate = endDate + datetime.timedelta(0, 59, 0, 0, 59, 23, 0) # "23:59:59"

    if startDate < datetime.datetime(2015, 1, 1) or endDate > datetime.datetime(2015, 6, 30, 23, 59, 59, 59):
        msg = "Invalid Input. Please enter date in valid range"
        print(msg)
        return msg

    query = db.query(models.RawTrip).filter(RawTrip.pickup_date.between(startDate, endDate))
    return query.count()

@app.get("/ridesInDay/{date}")
async def numRidesInDay(date, db: Session = Depends(get_db)):
    #Sample timestamp from PostgreSQL: 2015-03-28 15:24:00 
    date_format = '%Y-%m-%d'
    try:
        startDate = datetime.datetime.strptime(date, date_format)
        endDate = datetime.datetime.strptime(date, date_format)

    except ValueError:
        msg = "Incorrect data format, should be YYYY-MM-DD"
        print(msg)
        return msg
    
    startDate = startDate + datetime.timedelta(0, 0, 0, 0, 0, 0, 0) # "00:00:00"
    endDate = endDate + datetime.timedelta(0, 59, 0, 0, 59, 23, 0) # "23:59:59"

    if startDate < datetime.datetime(2015, 1, 1) or endDate > datetime.datetime(2015, 6, 30, 23, 59, 59, 59):
        msg = "Invalid Input. Please enter date in valid range"
        print(msg)
        return msg

    query = db.query(models.RawTrip).filter(RawTrip.pickup_date.between(startDate, endDate))
    return query.count()

@app.get("/getRidesInMonth/{inputMonth}")
async def getRidesInMonth(inputMonth: int, db: Session = Depends(get_db)):
    if inputMonth not in range(1, 7):
        msg = "Invalid Month. Must be between January and June (inclusive)."
        print(msg)
        return msg
    
    startDate = '2015-0{}-01 00:00:00'.format(str(inputMonth))
    endDate = '2015-0{}-{} 23:59:59'.format(str(inputMonth), str(days_in_month()[inputMonth]))

    #"%d/%m/%y %H:%M:%S.%f"
    '''
    date_format = '%Y-%m-%d %-H:%M:%S'
    try:
        startDate  = datetime.datetime.strptime(startDate, date_format)
        endDate = datetime.datetime.strptime(endDate, date_format)
    
    except:
        msg = "Incorrect data format, should be YYYY-MM-DD"
        print(msg)
        return msg
    '''
    query = db.query(models.RawTrip).filter(RawTrip.pickup_date.between(startDate, endDate))
    return query.count()

@app.get("/getNumRidesInZone/{inputZone}")
async def getNumRidesInZone(inputZone: str, db: Session = Depends(get_db)):
    zoneQuery = db.query(models.TaxiZone).all()

    targetID = None
    for item in zoneQuery:
        if item.zone == inputZone:
            targetID = item.locationID
    
    if not targetID:
        msg = "Invalid Zone. Please retry."
        print(msg)
        return msg
    
    mainQuery = db.query(models.RawTrip).filter_by(locationID = targetID).all()
    return len(mainQuery)

@app.get("/getRidesByHour")
async def getRidesByHour(db: Session = Depends(get_db)):
    monthList = ["January", "February", "March", "April", "May", "June"]
    _map = {}
    '''
    startDate = '2015-0{}-01 00:00:00'.format(str(inputMonth))
    endDate = '2015-0{}-30 23:59:59'.format(str(inputMonth))
    '''
    for i in range(1, len(monthList) + 1):
        month = monthList[i-1]
        _map[month] = {}
        for x in range(0, 24):
            start_ts = "2015-0{}-01 00:00:00".format(str(i))
            end_ts = "2015-0{}-{} 23:59:59".format(str(i), str(days_in_month()[i]))
            query = db.query(models.RawTrip).filter(RawTrip.pickup_date.between(start_ts, end_ts)).filter(extract("hour", RawTrip.pickup_date) == x).all()
            _map[month][x] = len(query)
    
    return _map

@app.get("/zonesPerBorough")
async def zonesPerBorough(db: Session = Depends(get_db)):
    boroughList = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']
    _map = {}

    for currBorough in boroughList:
        _map[currBorough] = []
        query = db.query(models.TaxiZone).filter_by(borough = currBorough).all()

        for item in query:
            _map[currBorough].append(item.zone)

    return _map

@app.get("/getZonesBorough/{inputZone}")
async def getZonesBorough(inputZone: str, db: Session = Depends(get_db)):
    query = db.query(models.TaxiZone).filter_by(zone = inputZone).all()

    if not query:
        msg = "Invalid Zone. Please retry with valid entry."
        print(msg)
        return msg
        
    return query[0].borough
    
