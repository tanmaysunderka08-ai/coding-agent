from datetime import datetime


def parse_date(text):
    return datetime.strptime(text.strip(), "%m/%d/%Y").date()


def month_key(d):
    return d.strftime("%Y-%m")


def month_name(key):
    return datetime.strptime(key, "%Y-%m").strftime("%B %Y")


def days_between(a, b):
    return (b - a).days
