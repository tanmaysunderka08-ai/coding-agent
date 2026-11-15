def to_minutes(text):
    hours, minutes = text.strip().split(":")
    return int(hours) * 60 + int(minutes)


def fmt(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"
