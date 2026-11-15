class RoadMap:
    def __init__(self):
        self.roads = {}

    def add_road(self, a, b, km):
        self.roads.setdefault(a, []).append((b, km))
        self.roads.setdefault(b, []).append((a, km))

    def __contains__(self, city):
        return city in self.roads

    def neighbours(self, city):
        return self.roads.get(city, [])


def load(text):
    roads = RoadMap()
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pair, km = line.rsplit(":", 1)
        a, b = [p.strip() for p in pair.split(" - ")]
        roads.add_road(a, b, int(km))
    return roads
