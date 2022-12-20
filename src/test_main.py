from fastapi.testclient import TestClient
from main import app, days_in_month
import models
from database import SessionLocal, engine
from fastapi import status

client = TestClient(app = app)
models.Base.metadata.create_all(bind=engine)

def test_main():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
'''
def test_numberOfRidesPerBorough():
    input = "Philadelphia"

    #response = client.get("/numPerBorough/{}".format(input))
    #assert response.status_code == status.HTTP_200_OK
    print("/numPerBorough/{}".format(input))
    assert True == True
'''
def test_zonesPerBorough():
    response = client.get("/zonesPerBorough")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

def test_ridesInRange():
    start_date = '2015-01-03'
    end_date = '2015-03-05'

    request = "/numRidesInRange/{}/{}".format(start_date, end_date)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == int
    assert response.json() == 4471813

def test_invalid_ridesInRange():
    start_date = '2014-12-01'
    end_date = '2015-06-01'

    request = "/numRidesInRange/{}/{}".format(start_date, end_date)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Invalid Input. Please enter date in valid range"

def test_incorrect_ridesInRange():
    start_date = 'test'
    end_date = 'test'

    request = "/numRidesInRange/{}/{}".format(start_date, end_date)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Incorrect data format, should be YYYY-MM-DD"

def test_ridesInDay():
    input = '2015-04-30'

    request = "/ridesInDay/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == int
    assert response.json() == 84330

def test_invalid_ridesInDay():
    input = '2015-07-01'

    request = "/ridesInDay/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Invalid Input. Please enter date in valid range"

def test_incorrect_ridesInDay():
    input = 'test'

    request = "/ridesInDay/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Incorrect data format, should be YYYY-MM-DD"

def test_getRidesInMonth():
    input = 'february'

    request = "/getRidesInMonth/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == int
    assert response.json() == 2263620

def test_invalid_ridesInMonth():
    input = "November"

    request = "/getRidesInMonth/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Invalid Month. Must be between January and June (inclusive)."

def test_getNumRidesInZone():
    input = "JFK Airport"

    request = "/getNumRidesInZone/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == int
    assert response.json() == 289169

def test_invalid_getNumRidesInZone():
    input = "San Francisco"

    request = "/getNumRidesInZone/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Invalid Zone. Please retry."

def test_getRidesByHour():
    request = "/getRidesByHour"
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == dict

    output = response.json()
    monthList = ["January", "February", "March", "April", "May", "June"]
    for month in monthList:
        assert output.get(month, None) != None
        value = output[month]

        for x in range(0, 24):
            assert value.get(str(x), None) != None
            assert value[str(x)] > 0


def test_zonesPerBorough():
    request = "/zonesPerBorough"
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == dict

    boroughList = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']
    for bor in boroughList:
        assert len(response.json()[bor]) > 0

def test_getZonesBorough():
    input = 'East Village'

    request = "/getZonesBorough/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Manhattan"

def test_invalid_getZonesBorough():
    input = "Trenton"

    request = "/getZonesBorough/{}".format(input)
    response = client.get(request)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == str
    assert response.json() == "Invalid Zone. Please retry with valid entry."


