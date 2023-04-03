from typing import Optional, cast

from geopy import Location
from geopy.geocoders import Nominatim


def get_location(user_input: str) -> Optional[Location]:
    geolocator = Nominatim(user_agent=__name__)
    response = cast(Optional[Location], geolocator.geocode(user_input))
    return response
