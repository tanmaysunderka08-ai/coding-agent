from datetime import datetime, timedelta


def to_utc(local, offset_minutes):
    return local - timedelta(minutes=offset_minutes)


def to_local(utc, offset_minutes):
    return utc + timedelta(minutes=offset_minutes)


def parse_local(text):
    return datetime.strptime(text, "%Y-%m-%d %H:%M")
