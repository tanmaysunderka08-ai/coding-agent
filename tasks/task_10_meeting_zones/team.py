from tzparse import parse_offset

TEAM = {
    "tanmay": "+05:30",
    "raj": "+05:45",
    "li": "+08:00",
    "ana": "-03:30",
    "sam": "-05:00",
}


def offset_of(name):
    return parse_offset(TEAM[name])
