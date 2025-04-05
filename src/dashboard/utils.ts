import type { LocationCoords } from "./types";

// returns the current location coordinates in a promise
export const getCurrentCoords = (retries = 5): Promise<LocationCoords | null> => {
  return new Promise((res, rej) => {
    navigator.geolocation.getCurrentPosition(
      (position: GeolocationPosition) => {
        // return coordinates as an object
        res({
          "lat": position.coords.latitude,
          "lon": position.coords.longitude
        });
      },
      // handle some possible errors
      (error: GeolocationPositionError) => {
        console.error("Geolocation error: ", error.message);

        // this error is about macOS location services so retrying multiple times is the best option
        if (error.code === GeolocationPositionError.POSITION_UNAVAILABLE && retries > 0) {
          console.warn("Location temporarily unavailable, retrying...");

          // wait for a moment before retrying
          setTimeout(() => {
            // recursively call the function with one less retry
            getCurrentCoords(retries - 1)
              .then(result => res(result))
              .catch(() => res(null));
          }, 2000); // try every two seconds
        } else {
          // no retries left or different error type
          if (error.code === GeolocationPositionError.PERMISSION_DENIED) {
            console.warn("User denied location access");
          }
          res(null);
        }
        res(null);
      },
      {
        timeout: 15000, // throw error if unable to get a location within 15 seconds
        maximumAge: 86400000,
        enableHighAccuracy: false
      }
    );
  });
}
