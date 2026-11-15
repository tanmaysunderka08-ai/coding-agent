from datetime import datetime, timedelta

from clock import parse_local, to_local, to_utc
from team import TEAM, offset_of

WORK_START, WORK_END = 9 * 60, 17 * 60


def local_times(utc):
    return {name: to_local(utc, offset_of(name)).strftime("%a %H:%M") for name in sorted(TEAM)}


def schedule(local_text, organizer):
    utc = to_utc(parse_local(local_text), offset_of(organizer))
    return {"utc": utc.strftime("%Y-%m-%d %H:%M"), "local": local_times(utc)}


def free_for(name, utc, minutes):
    start = to_local(utc, offset_of(name))
    begin = start.hour * 60 + start.minute
    return start.weekday() < 5 and WORK_START <= begin and begin + minutes <= WORK_END


def common_slots(day, names, minutes=30):
    slots = []
    t = datetime(day.year, day.month, day.day)
    while t < datetime(day.year, day.month, day.day) + timedelta(days=1):
        if all(free_for(n, t, minutes) for n in names):
            slots.append(t.strftime("%H:%M"))
        t += timedelta(minutes=30)
    return slots
