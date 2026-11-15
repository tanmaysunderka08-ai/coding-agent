"""Map tiles: the plane around the city centre is cut into square tiles of TILE metres."""

TILE = 100


def tile_of(x, y):
    return int(x / TILE), int(y / TILE)


def tile_bounds(tx, ty):
    return (tx * TILE, ty * TILE, (tx + 1) * TILE, (ty + 1) * TILE)


def contains(bounds, x, y):
    x0, y0, x1, y1 = bounds
    return x0 <= x < x1 and y0 <= y < y1


def neighbours(tx, ty):
    return [(tx + dx, ty + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]
