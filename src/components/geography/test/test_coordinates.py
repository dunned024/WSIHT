from unittest.mock import MagicMock

from geopy import Location

from components.geography.coordinates import get_coord_box


def test_get_coord_box():
    mock_location = MagicMock(spec=Location)
    mock_location.latitude = 1.0
    mock_location.longitude = 2.0

    coord_box = get_coord_box(mock_location)

    assert coord_box.north == 1.1
    assert coord_box.south == 0.9
    assert coord_box.east == 2.1
    assert coord_box.west == 1.9
