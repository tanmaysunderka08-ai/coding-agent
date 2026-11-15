from busy import parse_calendar
from clock import fmt, to_minutes
from intervals import clip, gaps, merge


def _day(day):
    lo, hi = (to_minutes(t) for t in day.split("-"))
    return lo, hi


def free_slots(calendar_text, day="09:00-18:00", min_minutes=30, people=None):
    calendar = parse_calendar(calendar_text)
    names = people or sorted(calendar)
    lo, hi = _day(day)
    busy = merge(clip([iv for name in names for iv in calendar.get(name, [])], lo, hi))
    return [f"{fmt(s)}-{fmt(e)}" for s, e in gaps(busy, lo, hi) if e - s >= min_minutes]


def busy_minutes(calendar_text, day="09:00-18:00"):
    calendar = parse_calendar(calendar_text)
    lo, hi = _day(day)
    return {name: sum(e - s for s, e in merge(clip(ivs, lo, hi))) for name, ivs in sorted(calendar.items())}
