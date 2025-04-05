from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Location
from weather_api import get_current_weather, get_forecast
from utils import get_cache_timestamp, normalize_name, map_weather_code
import csv
import re


# initialize FastAPI app
app = FastAPI()

# configure CORS to allow requests from localhost
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# define Pydantic models for POST requests
class CityModel(BaseModel):
    city: str

class LocationModel(BaseModel):
    lat: float
    lon: float


# GET /locations endpoint for fetching all saved locations with their current weather
@app.get("/locations")
def read_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()

    # mark the last api call timestamp for caching
    current_timestamp = get_cache_timestamp()

    location_list = []

    for location in locations:
        # fetch and append weather data for each saved city
        weather_data = get_current_weather(
            location.latitude,
            location.longitude,
            _timestamp=current_timestamp
        )

        location_list.append({
            "id": location.id,
            "name": location.name,
            "temperature": f'{round(weather_data["current"]["temperature_2m"])}°C',
            "rain": f'{round(weather_data["current"]["rain"])} mm',
            "weather_code": map_weather_code(weather_data["current"]["weather_code"])
        })

    # no need to check for empty list, as it can be checked in frontend
    return location_list

@app.post("/locations/single")
def get_single_weather(location_coords: LocationModel):
    lat = location_coords.lat
    lon = location_coords.lon

    current_timestamp = get_cache_timestamp()

    data = get_current_weather(lat, lon, _timestamp=current_timestamp)
    return f'{round(data["current"]["temperature_2m"])}°C'


# POST /locations endpoint for adding a new city
@app.post("/locations")
def add_location(location_request: CityModel, db: Session = Depends(get_db)):
    city = location_request.city # access city from request body

    # open csv file
    with open("data/country-capital-lat-long-population.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')

        # skip title row that contains "country", "capital" etc.
        next(reader)

        # look for full city names without punctuation or multi-names
        whole_word_pattern = r"\b" + normalize_name(city) + r"\b"
        for row in reader:
            if re.search(whole_word_pattern, normalize_name(row[1])):

                # check if location already exists in the database
                if (db.query(Location).filter(Location.name == row[1]).first()):
                    return {"error": f"{city} is already added to the database!"}

                print(row[0])
                location_to_add = Location(name=row[1], country=row[0], latitude=float(row[2]), longitude=float(row[3]))
                db.add(location_to_add)
                db.commit()

                # fetch current weather for the new location
                weather_data = get_current_weather(location_to_add.latitude, location_to_add.longitude)

                # return required data with correct formatting
                return {
                    "id": location_to_add.id,
                    "name": location_to_add.name,
                    "temperature": f'{round(weather_data["current"]["temperature_2m"])}°C',
                    "rain": f'{round(weather_data["current"]["rain"])} mm',
                    "weather_code": map_weather_code(weather_data["current"]["weather_code"])
                }


# GET Search endpoint for searching cities with each request
@app.get("/locations/{city_name}")
def search_location(city_name: str):

    # open csv file
    with open("data/country-capital-lat-long-population.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')

        # skip title row that contains "country", "capital" etc.
        next(reader) 
        matching_locations = []

        # find and append all cities containing the search term
        for row in reader:
            if normalize_name(city_name) in normalize_name(row[1]):
                matching_locations.append(row[1])
        return matching_locations


# DELETE /locations/{location_id} endpoint for deleting a location by its id
@app.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()

    # if location with given id is not found, return an error message
    if db_location is None:
        return {"error": f"Location already deleted!"}

    # delete location
    db.delete(db_location)
    db.commit()
    return {"message": f"{db_location.name} deleted successfully!"}


# GET /forecast/{location_id} endpoint for retrieving seven day forecast for a city
@app.get("/forecast/{location_id}")
def forecast(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()

    # mark the last api call timestamp for caching
    current_timestamp = get_cache_timestamp()

    # confirm city is in the database
    if db_location is None:
        raise HTTPException(status_code=404, detail=f"Location with given id({location_id}) not found")

    # fetch forecast data and map weather codes to provided svg files
    forecast = get_forecast(db_location.latitude, db_location.longitude, _timestamp=current_timestamp)
    mapped_data = forecast["daily"].copy()
    mapped_data["weather_code"] = [map_weather_code(code) for code in forecast["daily"]["weather_code"]]

    return {
        "name": db_location.name,
        "country": db_location.country,
        "daily": mapped_data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
