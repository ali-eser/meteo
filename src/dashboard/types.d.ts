// WeatherObj is stored as an array in the location state
export interface WeatherObj {
  id: number;
  name: string;
  country: string;
  temperature: number;
  rain: number;
  weather_code: number;
}

export interface DailyData {
  time: string[];
  weather_code: number[];
  temperature_2m_max: number[];
  temperature_2m_min: number[];
  rain_sum: number[];
}

// ForecastObj is stored in the forecastData state
export interface ForecastObj {
  name: string;
  country: string;
  daily: DailyData;
}

// LocationCoords is used for fetching current location's temperature from the backend
export interface LocationCoords {
  lat: number;
  lon: number;
}
