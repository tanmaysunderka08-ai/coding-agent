from report import city_map, kind_report, locate, sightings_in_tile

DATA = """
120, 40, fox
130, 60, fox
-30, 40, fox
-60, -20, fox
-150, 30, fox
40, 70, fox
-5, -5, owl
250, 10, owl
-200, 50, owl
"""


def test_east_side_location():
    assert locate(250, 10) == {"tile": (2, 0), "bounds": (200, 0, 300, 100)}


def test_west_side_location():
    assert locate(-30, 40) == {"tile": (-1, 0), "bounds": (-100, 0, 0, 100)}


def test_fox_report():
    assert kind_report(DATA, "fox") == {
        "sightings": 6,
        "tiles": {(-2, 0): 1, (-1, -1): 1, (-1, 0): 1, (0, 0): 1, (1, 0): 2},
        "hottest": (1, 0),
        "score": 2.5,
    }


def test_owl_report():
    report = kind_report(DATA, "owl")
    assert report["tiles"] == {(-2, 0): 1, (-1, -1): 1, (2, 0): 1}
    assert report["hottest"] == (-2, 0)


def test_report_agrees_with_tile_bounds():
    for kind in ("fox", "owl"):
        for tile, n in kind_report(DATA, kind)["tiles"].items():
            assert len(sightings_in_tile(DATA, kind, tile)) == n, (kind, tile)


def test_city_map():
    assert city_map(DATA, "fox") == ["....", "1112", ".1.."]
