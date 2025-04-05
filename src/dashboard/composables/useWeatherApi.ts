import type { LocationCoords } from "~/types";

export const useWeatherApi = () => {

  // set config for retrieving .env
  const config = useRuntimeConfig();

  // connect to GET /locations endpoint for retrieving all locations from the database with their current weather
  const getAllWeatherData = async () => {
    try {
      // make a GET request to /locations
      const data = await fetch(`${config.public.apiBase}/locations`, {
          method: "GET"
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return an empty array
      // the error will be displayed as a notification
      return [];
    }
  }

  // connect to POST for fetching current weather data for current location
  const getSingleWeatherData = async (locationData: LocationCoords) => {
    try {
      // make a POST request to /locations with the city name
      const data = await fetch(`${config.public.apiBase}/locations/single`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(locationData)
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return
      // an error notification will be displayed as a notification
      return;
    }
  }

  // connect to GET /forecast/:location_id endpoint for retrieving the seven day forecast for a location
  const getForecastData = async (locationId: number) => {
    try {
      // make a GET request to /forecast/:location_id
      const data = await fetch(`${config.public.apiBase}/forecast/${locationId}`, {
          method: "GET"
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return
      // the error will be displayed as a notification
      return;
    }
  }

  // connect to POST /locations endpoint to add a new location to the database
  const addLocation = async (city: string) => {
    try {
      // make a POST request to /locations with the city name
      const data = await fetch(`${config.public.apiBase}/locations`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ city: city })
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return
      // an error notification will be displayed as a notification
      return;
    }
  }

  // connect to GET /locations/:city endpoint to search for a matching location in the provided CSV file
  const searchLocation = async (city: string) => {
    try {
      // make a GET request to /locations/:city endpoint with {city} being the search term
      const data = await fetch(`${config.public.apiBase}/locations/${city}`, {
          method: "GET"
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return an empty array
      // an error notification will be displayed as a notification
      return [];
    }
  }

  // connect to DELETE /locations/:locationId endpoint to delete a location from the database
  const deleteLocation = async (locationId: number) => {
    try {
      // make a DELETE request to /locations/:lcoationId endpoint with {locationId} being the ID of the location to remove
      const data = await fetch(`${config.public.apiBase}/locations/${locationId}`, {
          method: "DELETE"
        }
      );

      // parse and return the response
      const response = await data.json();
      return response;
    } catch (error) {
      // if an error has occured, return
      // an error notification will be displayed as a notification
      return;
    }
  }

  return { getAllWeatherData, getSingleWeatherData, getForecastData, addLocation, searchLocation, deleteLocation };
}
