
from typing import NamedTuple

from geopy import Location


class CoordBox(NamedTuple):
    north: float
    south: float
    east: float
    west: float


def get_coord_box(location: Location) -> CoordBox:
    """
    Adds some space around lat/lon of location to get a wider range of data
    """
    return CoordBox(
        north=location.latitude + 0.1,
        south=location.latitude - 0.1,
        east=location.longitude + 0.1,
        west=location.longitude - 0.1,
    )
