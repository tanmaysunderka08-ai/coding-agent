from dataclasses import dataclass


@dataclass(frozen=True)
class Review:
    product: str
    stars: int
    helpful: int
    verified: bool


def parse_reviews(text):
    reviews = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        product, stars, helpful, verified = [p.strip() for p in line.split("|")]
        stars = int(stars)
        if not 1 <= stars <= 5:
            continue
        reviews.append(Review(product, stars, int(helpful), verified == "yes"))
    return reviews


def by_product(reviews):
    groups = {}
    for r in reviews:
        groups.setdefault(r.product, []).append(r)
    return groups
