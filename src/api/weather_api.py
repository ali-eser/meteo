from functools import lru_cache
import requests

# fetch current weather for a given coordinate from OpenMeteo API and cache it for 15 minutes
@lru_cache(maxsize=128)
def get_current_weather(lat: float, lon: float, _timestamp=None):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,rain,weather_code"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


# fetch seven-day forecast for a given coordinate from OpenMeteo API and cache it for 15 minutes
@lru_cache(maxsize=128)
def get_forecast(lat: float, lon: float, _timestamp=None):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,rain_sum"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
