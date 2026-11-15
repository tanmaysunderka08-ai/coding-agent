from report import describe_trip

ROADS = """
# south India + islands
Chennai - Bengaluru : 350
Bengaluru - Mysuru : 145
Chennai - Puducherry : 150
Puducherry - Bengaluru : 310
Mysuru - Ooty : 125
Port Blair - Havelock : 50
"""


def test_mainland_tour():
    assert describe_trip(ROADS, "Chennai", ["Mysuru", "Puducherry"]) == [
        "Puducherry: 150 km via Chennai > Puducherry",
        "Mysuru: 455 km via Puducherry > Bengaluru > Mysuru",
        "total 605 km",
    ]


def test_typo_in_stop():
    assert describe_trip(ROADS, "Chennai", ["Atlantis"]) == ["unknown city: Atlantis"]


def test_typo_in_start():
    assert describe_trip(ROADS, "Delhi", ["Ooty"]) == ["unknown city: Delhi"]


def test_tour_with_island_stop():
    assert describe_trip(ROADS, "Chennai", ["Ooty", "Port Blair"]) == [
        "Ooty: 620 km via Chennai > Bengaluru > Mysuru > Ooty",
        "total 620 km",
        "no road to: Port Blair",
    ]


def test_island_start():
    assert describe_trip(ROADS, "Port Blair", ["Chennai", "Havelock"]) == [
        "Havelock: 50 km via Port Blair > Havelock",
        "total 50 km",
        "no road to: Chennai",
    ]
