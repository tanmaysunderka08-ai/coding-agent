from collections import Counter

from tiles import neighbours, tile_of


def counts_by_tile(sightings):
    return Counter(tile_of(s.x, s.y) for s in sightings)


def hottest(counts):
    if not counts:
        return None
    return max(sorted(counts), key=lambda tile: counts[tile])


def hotspot_score(counts, tile):
    return counts.get(tile, 0) + sum(counts.get(n, 0) for n in neighbours(*tile)) / 2


def render(counts, tx_range, ty_range):
    rows = []
    for ty in reversed(range(ty_range[0], ty_range[1] + 1)):
        row = ""
        for tx in range(tx_range[0], tx_range[1] + 1):
            n = counts.get((tx, ty), 0)
            row += "." if n == 0 else str(min(n, 9))
        rows.append(row)
    return rows
