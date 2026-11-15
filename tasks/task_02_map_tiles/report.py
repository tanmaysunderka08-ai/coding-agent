from heatmap import counts_by_tile, hotspot_score, hottest, render
from points import of_kind, parse_sightings
from tiles import contains, tile_bounds, tile_of


def kind_report(text, kind):
    sightings = of_kind(parse_sightings(text), kind)
    counts = counts_by_tile(sightings)
    top = hottest(counts)
    return {
        "sightings": len(sightings),
        "tiles": dict(sorted(counts.items())),
        "hottest": top,
        "score": hotspot_score(counts, top) if top else 0,
    }


def locate(x, y):
    tile = tile_of(x, y)
    return {"tile": tile, "bounds": tile_bounds(*tile)}


def sightings_in_tile(text, kind, tile):
    bounds = tile_bounds(*tile)
    return [s for s in of_kind(parse_sightings(text), kind) if contains(bounds, s.x, s.y)]


def city_map(text, kind, tx_range=(-2, 1), ty_range=(-1, 1)):
    return render(counts_by_tile(of_kind(parse_sightings(text), kind)), tx_range, ty_range)
