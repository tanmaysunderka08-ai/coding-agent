def merge(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return merged


def clip(intervals, lo, hi):
    return [(max(s, lo), min(e, hi)) for s, e in intervals if e > lo and s < hi]


def gaps(intervals, lo, hi):
    free = []
    cursor = lo
    for start, end in intervals:
        if start > cursor:
            free.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < hi:
        free.append((cursor, hi))
    return free
