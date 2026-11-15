from datetime import timedelta

from events import last_seen, users_between
from windows import calendar_week, previous_window, trailing_window


def active_users(events, day, days):
    start, end = trailing_window(day, days)
    return users_between(events, start, end)


def dau(events, day):
    return len(users_between(events, day, day))


def wau(events, day):
    return len(active_users(events, day, 7))


def mau(events, day):
    return len(active_users(events, day, 30))


def churned(events, day, days=14):
    cutoff = day - timedelta(days=days)
    return sorted(user for user, seen in last_seen(events).items() if seen <= cutoff)


def growth(events, day, days=7):
    now = len(active_users(events, day, days))
    start, end = previous_window(day, days)
    before = len(users_between(events, start, end))
    if before == 0:
        return None
    return round((now - before) / before, 3)


def week_actives(events, day):
    start, end = calendar_week(day)
    return len(users_between(events, start, end))
