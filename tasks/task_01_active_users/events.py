"""Activity events loaded from 'YYYY-MM-DD, user, action' lines."""

from collections import namedtuple
from datetime import date

Event = namedtuple("Event", "day user action")


def parse_events(text):
    events = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        day, user, action = [part.strip() for part in line.split(",")]
        events.append(Event(date.fromisoformat(day), user, action))
    return events


def users_between(events, start, end):
    return {e.user for e in events if start <= e.day <= end}


def last_seen(events):
    seen = {}
    for e in events:
        if e.user not in seen or e.day > seen[e.user]:
            seen[e.user] = e.day
    return seen
