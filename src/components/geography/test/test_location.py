from pytest_mock import MockerFixture

from components.geography.coordbox_collector import Nominatim, get_location


def test_get_location(mocker: MockerFixture):
    mocker.patch.object(Nominatim, "geocode", return_value=True)
    location = get_location("test")
    assert location
