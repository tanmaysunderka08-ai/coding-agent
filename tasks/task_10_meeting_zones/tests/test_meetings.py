from datetime import date

from meetings import common_slots, local_times, schedule
from clock import parse_local

MONDAY = date(2026, 11, 16)


def test_india_and_singapore():
    slots = common_slots(MONDAY, ["tanmay", "li"])
    assert (slots[0], slots[-1], len(slots)) == ("03:30", "08:30", 11)


def test_meeting_seen_by_everyone():
    assert local_times(parse_local("2026-11-16 13:00")) == {
        "ana": "Mon 09:30", "li": "Mon 21:00", "raj": "Mon 18:45",
        "sam": "Mon 08:00", "tanmay": "Mon 18:30"}


def test_meeting_organised_from_newfoundland():
    result = schedule("2026-11-16 09:30", "ana")
    assert result["utc"] == "2026-11-16 13:00"
    assert result["local"]["tanmay"] == "Mon 18:30"


def test_americas_overlap():
    slots = common_slots(MONDAY, ["ana", "sam"])
    assert (slots[0], slots[-1], len(slots)) == ("14:00", "20:00", 13)


def test_no_overlap_india_newfoundland():
    assert common_slots(MONDAY, ["tanmay", "ana"]) == []
