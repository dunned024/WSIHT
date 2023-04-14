from typing import NamedTuple


class Hike(NamedTuple):
    id: int
    name: str
    day: str
    latitude: float
    longitude: float
    temperature: float
    precipitation: float
    humidity: float
    cloud_coverage: float
    visibility: float
    wind: float
    wind_gust: float
    dew_point: float
