from version import Version, parse_version


def caret_upper(low):
    if low.major > 0 or low.minor > 0:
        return Version(low.major + 1, 0, 0)
    return Version(0, 0, low.patch + 1)


def tilde_upper(low):
    return Version(low.major, low.minor + 1, 0)


def parse_range(text):
    text = text.strip()
    if text == "*":
        return Version(0, 0, 0), None
    if text.startswith("^"):
        low = parse_version(text[1:])
        return low, caret_upper(low)
    if text.startswith("~"):
        low = parse_version(text[1:])
        return low, tilde_upper(low)
    if text.startswith(">="):
        return parse_version(text[2:]), None
    exact = parse_version(text)
    return exact, Version(exact.major, exact.minor, exact.patch + 1)


def matches(version, rng):
    low, high = rng
    return version >= low and (high is None or version < high)
