# Retrieve the API key from environment variables
from collections import Counter
import traceback
from typing import List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import requests

from configs.configs import app_configs
from logics.airport_schedule import AirportSchedule

router = APIRouter()

class CountryFlight(BaseModel):
    country: str
    flight_count: int

class FlightsResponse(BaseModel):
    status: str = "error"
    data: List[CountryFlight]

@router.get("/flights", response_model=FlightsResponse, status_code=200)
def get_flights(airport: str = Query(..., min_length=3, max_length=3, description="3-character Airport Code")):
    airport_code = airport.strip().upper()
    print("airport_code", airport_code)

    # Validate airport code
    if not airport_code.isalpha():
        raise HTTPException(status_code=400, detail="Airport code must consist of 3 alphabetic characters.")

    if not app_configs.FLIGHTAPI_KEY:
        raise HTTPException(status_code=500, detail="FLIGHTAPI_KEY not found in environment variables.")

    try:
        airport_schedule = AirportSchedule(api_key=app_configs.FLIGHTAPI_KEY,
                                           airport_code=airport_code,
                                           mode="arrivals",)

        countries = airport_schedule.get_flights_by_airport()

        counter = Counter(countries)
        flight_data = [CountryFlight(country=country, flight_count=count) for country, count in counter.most_common()]

        return FlightsResponse(status='success', data=flight_data)

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error fetching data from FlightAPI.io: {e}")
    except ValueError as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error parsing the API response {e}.")
    except Exception as e:
        print(traceback.format_exc())
        raise e

# Root endpoint
@router.get("/")
def read_root():
    return {"message": "Welcome to the Flights by Country API. Use the /flights endpoint with an 'airport' query parameter."}
