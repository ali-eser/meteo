from datetime import datetime
import re

# round current timestamp to 15 minutes for caching data
def get_cache_timestamp():
    now = datetime.now()
    return now.replace(minute=now.minute - now.minute % 15, second=0, microsecond=0)

# normalizes city names for easier comparison and search
def normalize_name(city: str) -> str:
    # convert the string to lowercase
    city = city.lower()

    # remove all puncuation except spaces
    city = re.sub(r'[^\w\s]', '', city)

    # remove extra spaces
    city = " ".join(city.split())
    return city

# map the weather code into five svg filenames that are provided
# returned integer will be used for placing the correct svg icon
def map_weather_code(code: int) -> int:
    if code == 0:
        return 1

    if code in [1, 2]:
        return 3

    if code == 3:
        return 4

    if 45 <= code <= 49:
        return 4

    if 51 <= code <= 57:
        return 5

    if 61 <= code <= 67:
        return 5

    if 71 <= code <= 77:
        return 4

    if 80 <= code <= 82:
        return 5

    if 85 <= code <= 86:
        return 4

    if 95 <= code <= 99:
        return 2
