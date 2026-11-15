from clock import to_minutes


def parse_calendar(text):
    people = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        name, blocks = line.split(":", 1)
        intervals = []
        for block in blocks.split(","):
            block = block.strip()
            if not block:
                continue
            start, end = block.split("-")
            intervals.append((to_minutes(start), to_minutes(end)))
        people[name.strip()] = intervals
    return people
