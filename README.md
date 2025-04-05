# Météo

### A simple capital weather tracker utilizing OpenMeteo API with Nuxt 3 frontend.

## Directories
- `src` - Main directory.
  - `api` - The backend directory.
    - `data` - Includes the csv file contains capital cities.
    - `.env.example` - Example dotenv file.
    - `database.py` - Creates and manages database connections.
    - `main.py` - Main entry point of the app and definition of API endpoints.
    - `models.py` - Defines the `Location` model used by the app.
    - `utils.py` - Few utility functions that are used throughout the codebase.
    - `weather_api.py` - Handles external connections to Open Meteo API.
  - `dashboard` - The frontend directory.
    - `components` - Contains three main components used.
      - `Modal.vue` - Defines the modal pop up component and its related functions.
      - `Sidebar.vue` - Defines the sidebar component and its related functions.
      - `Table.vue` - Defines the table component and its related functions.
    - `composables` - Contains the `useWeatherApi` composable.
      - `useWeatherApi.ts` - Handles requests to the FastAPI app.
    - `pages` - Contains the entry point to the app.
      - `index.vue` - Defines the structure of the app, base functions, and states.
    - `.env.example` - Example dotenv file.
    - `types.d.ts` - Contains type definitions.
    - `utils.ts` - Contains logic for fetching user location data.

## How to run
1. Create a table in a local PostgreSQL database. (e.g. psql 16).
1. In a terminal emulator, `cd` into `src/api`.
2. Create a virtual env.
3. Activate the virtual env.
4. `pip install -r requirements.txt` (or `pip3` for that matter).
5. Either `uvicorn main:app --reload` or `python main.py` (on macOS you might need `python3 main.py`). Both will run in a hot reloading dev env.
6. Create a `.env` file and configure it according to the `.env.example` I provided.
7. In another terminal instance, `cd` into `src/dashboard`.
8. Create a `.env` file and configure it according to the `.env.example` I provided.
9. Type `npm install` and press return.
10. Type `npm run dev` to run in a dev env.
11. You can access the app at the URL assigned by Nuxt.


## Notes
- The data is cached for 15 minutes to speed up the app and to reduce API calls.
- User must choose a city from the dropdown menu before adding, custom entries are not accepted.
- A user should allow location access to enjoy the local weather feature.
