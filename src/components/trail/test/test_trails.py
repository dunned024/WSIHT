from components.trail.trails import Trail, parse_trail_hits


def test_parse_trail_hits():
    hits = [
        {
            "ID": 1,
            "name": "Test Trail 1",
            "_geoloc": {
                "lat": 1.0,
                "lng": -1.0,
            },
        },
        {
            "ID": 2,
            "name": "Test Trail 2",
            "_geoloc": {
                "lat": 2.0,
                "lng": -2.0,
            },
        },
    ]

    trails = parse_trail_hits(hits)

    assert trails[0] == Trail(
        id=1,
        name="Test Trail 1",
        latitude=1.0,
        longitude=-1.0,
    )

    assert trails[1] == Trail(
        id=2,
        name="Test Trail 2",
        latitude=2.0,
        longitude=-2.0,
    )
