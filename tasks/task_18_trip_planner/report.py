from planner import plan_tour
from roads import load


def describe_trip(road_text, start, stops):
    roads = load(road_text)
    try:
        legs, skipped = plan_tour(roads, start, stops)
    except KeyError as e:
        return [f"unknown city: {e.args[0]}"]
    lines = [f"{city}: {km} km via {' > '.join(path)}" for city, km, path in legs]
    lines.append(f"total {sum(km for _, km, _ in legs)} km")
    if skipped:
        lines.append("no road to: " + ", ".join(skipped))
    return lines
