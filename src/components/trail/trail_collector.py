import requests
from typing import Any

from components.geography.coordbox_collector import CoordBox
from components.trail.trail_record import Trail


def get_trails(coord_box: CoordBox):
    url = "https://9ioacg5nhe-dsn.algolia.net/1/indexes/alltrails_primary_en-US/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.8.6)%3B%20Browser"

    headers = {
        "x-algolia-api-key": "63a3cf94e0042b9c67abf0892fc1d223",
        "x-algolia-application-id": "9IOACG5NHE"
    }

    payload = {
        "query": "",
        "hitsPerPage": 100,
        "attributesToRetrieve": [
            "ID",
            "_cluster_geoloc",
            "_geoloc",
            "name",
            "slug",
            "type",
            "is_closed",
            "is_private_property"
        ],
        "attributesToHighlight": [],
        "filters": "type:trail AND ((length>=0)) AND ((elevation_gain>=0))",
        "insideBoundingBox": f"{coord_box.north}, {coord_box.west}, {coord_box.south}, {coord_box.east}",
        "responseFields": [
            "hits",
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    return _parse_trail_hits(response.json()["hits"])


def _parse_trail_hits(hits: list[dict[str, Any]]) -> list[Trail]:
    return [
        Trail(
            id=raw_trail["ID"],
            name=raw_trail["name"],
            latitude=raw_trail["_geoloc"]["lat"],
            longitude=raw_trail["_geoloc"]["lng"],
        )
        for raw_trail in hits
    ]
