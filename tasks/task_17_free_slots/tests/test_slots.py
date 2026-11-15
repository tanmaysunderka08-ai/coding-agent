from slots import busy_minutes, free_slots

TEAM = """
ana: 09:00-10:00, 13:00-14:00
raj: 09:30-10:30, 16:00-17:00
li: 11:00-11:30
"""

WORKSHOP_DAY = """
ana: 09:00-12:30, 15:00-15:30
raj: 10:00-10:30, 11:00-11:15, 14:00-14:45
sam: 08:00-09:30, 17:30-19:00
"""

OUT_OF_OFFICE = """
li: 09:00-17:00, 12:00-13:00
mo: 10:00-11:00, 10:30-11:30
"""


def test_team_day():
    assert free_slots(TEAM) == ["10:30-11:00", "11:30-13:00", "14:00-16:00", "17:00-18:00"]


def test_longer_meetings_only():
    assert free_slots(TEAM, min_minutes=60) == ["11:30-13:00", "14:00-16:00", "17:00-18:00"]


def test_subset_of_people():
    assert free_slots(TEAM, people=["li"]) == ["09:00-11:00", "11:30-18:00"]


def test_workshop_day():
    assert free_slots(WORKSHOP_DAY) == ["12:30-14:00", "15:30-17:30"]


def test_busy_minutes():
    assert busy_minutes(OUT_OF_OFFICE) == {"li": 480, "mo": 90}
    assert busy_minutes(TEAM) == {"ana": 120, "li": 30, "raj": 120}
