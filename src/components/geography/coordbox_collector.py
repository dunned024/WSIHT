from typing import Optional, cast

from geopy import Location
from geopy.geocoders import Nominatim

from components.geography.coordbox_record import CoordBox


def get_location(user_input: str) -> Optional[Location]:
    geolocator = Nominatim(user_agent=__name__)
    response = cast(Optional[Location], geolocator.geocode(user_input))
    return response


def get_coord_box(latitude: float, longitude: float, padding: float) -> CoordBox:
    """
    Adds some space around lat/lon of location to get a wider range of data
    """
    return CoordBox(
        north=latitude + padding,
        south=latitude - padding,
        east=longitude + padding,
        west=longitude - padding,
    )
