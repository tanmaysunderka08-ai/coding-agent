from errors import UnknownCity, Unreachable
from paths import shortest


def route(roads, a, b):
    for city in (a, b):
        if city not in roads:
            raise UnknownCity(city)
    dist, prev = shortest(roads, a)
    path = [b]
    while path[-1] != a:
        path.append(prev[path[-1]])
    return dist[b], path[::-1]


def plan_tour(roads, start, stops):
    here = start
    remaining = list(stops)
    legs, skipped = [], []
    while remaining:
        options = []
        for city in remaining:
            try:
                km, path = route(roads, here, city)
            except Unreachable:
                skipped.append(city)
                continue
            options.append((km, city, path))
        remaining = [c for c in remaining if c not in skipped]
        if not options:
            break
        km, city, path = min(options)
        legs.append((city, km, path))
        remaining.remove(city)
        here = city
    return legs, skipped
