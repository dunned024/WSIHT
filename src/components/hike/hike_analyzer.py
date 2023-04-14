from sqlalchemy import and_

from components.forecast.forecast_record import Forecast
from components.geography.coordbox_collector import get_coord_box
from components.geography.coordbox_record import CoordBox
from components.hike.hike_record import Hike
from components.trail.trail_record import Trail


def generate_hikes(trails: list[Trail]):
    """
    Combines Forecast data stored in DB with scraped Trails to create list
    of Hikes
    """
    hikes = []
    for trail in trails:
        hike_coordbox = get_coord_box(
            latitude=trail.latitude, longitude=trail.longitude, padding=0.01
        )
        forecasts = get_forecasts_in_coordbox(hike_coordbox)
        # TODO: Figure out better way to handle no forecasts
        if len(forecasts) == 0:
            continue

        hike = merge_trail_with_forecasts(trail, forecasts)
        hikes.append(hike)

    return hikes


def get_forecasts_in_coordbox(coordbox: CoordBox) -> list[Forecast]:
    return Forecast.query.filter(
        and_(
            Forecast.latitude <= coordbox.north,
            Forecast.latitude >= coordbox.south,
            Forecast.longitude <= coordbox.east,
            Forecast.longitude >= coordbox.west,
        )
    ).all()


def merge_trail_with_forecasts(trail: Trail, forecasts: list[Forecast]) -> Hike:
    return Hike(
        id=trail.id,
        name=trail.name,
        day=forecasts[0].day,
        latitude=trail.latitude,
        longitude=trail.longitude,
        temperature=float(sum(f.temperature for f in forecasts)) / len(forecasts),
        precipitation=float(sum(f.precipitation for f in forecasts)) / len(forecasts),
        humidity=float(sum(f.humidity for f in forecasts)) / len(forecasts),
        cloud_coverage=float(sum(f.cloud_coverage for f in forecasts)) / len(forecasts),
        visibility=float(sum(f.visibility for f in forecasts)) / len(forecasts),
        wind=float(sum(f.wind for f in forecasts)) / len(forecasts),
        wind_gust=float(sum(f.wind_gust for f in forecasts)) / len(forecasts),
        dew_point=float(sum(f.dew_point for f in forecasts)) / len(forecasts),
    )


def _merge_forecast_field(forecasts: list[Forecast], fieldname: str) -> float:
    return float(sum(f[fieldname] for f in forecasts)) / len(forecasts)
