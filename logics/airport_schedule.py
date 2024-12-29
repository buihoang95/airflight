
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel
import requests


class AirportSchedule(BaseModel):
    api_key: str
    airport_code: str
    mode: Optional[str] = "arrivals"
    day: Optional[int] = 1 # Default to today

    def get_flights_by_airport(self) -> List[str]:
        """Get the list of countries that have flights arriving at the airport

        Raises:
            HTTPException: exception when the API request fails

        Returns:
            List[str]: list of countries
        """
        url = f"https://api.flightapi.io/compschedule/{self.api_key}?day={self.day}&mode={self.mode}&iata={self.airport_code}"
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        print("data", data)
        countries = []
        for page in data:
            flights = page["airport"]["pluginData"]["schedule"]["arrivals"]["data"]
            for flight in flights:
                country = flight["flight"]["airport"]["origin"]["position"]["country"]["name"]
                countries.append(country)
        return countries


