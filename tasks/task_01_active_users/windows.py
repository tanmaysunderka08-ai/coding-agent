"""Date windows used by the metrics."""

from datetime import timedelta


def trailing_window(end_day, days):
    start = end_day - timedelta(days=days)
    return start, end_day


def previous_window(end_day, days):
    start, end = trailing_window(end_day, days)
    shift = timedelta(days=days)
    return start - shift, end - shift


def calendar_week(day):
    start = day - timedelta(days=day.weekday())
    return start, start + timedelta(days=6)
