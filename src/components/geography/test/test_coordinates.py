from components.geography.coordbox_collector import get_coord_box


def test_get_coord_box():
    coord_box = get_coord_box(latitude=1.0, longitude=2.0, padding=0.1)

    assert coord_box.north == 1.1
    assert coord_box.south == 0.9
    assert coord_box.east == 2.1
    assert coord_box.west == 1.9
