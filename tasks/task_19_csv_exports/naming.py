import re


def stem(filename):
    return filename.rstrip(".csv")


def slug(text):
    return re.sub(r"[^a-z0-9.]+", "_", text.lower()).strip("_")


def output_name(filename, kind="summary"):
    return f"{slug(stem(filename))}_{kind}.json"
