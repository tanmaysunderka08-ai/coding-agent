from reviews import by_product, parse_reviews
from scoring import mean, shrink, weighted_mean
from weights import review_weight


def summarize(reviews):
    rating = weighted_mean((r.stars, review_weight(r)) for r in reviews)
    return {
        "reviews": len(reviews),
        "plain": round(mean(r.stars for r in reviews), 2),
        "rating": round(rating, 2),
        "score": round(shrink(rating, len(reviews)), 2),
    }


def leaderboard(text):
    groups = by_product(parse_reviews(text))
    rows = [(name, summarize(rs)) for name, rs in groups.items()]
    rows.sort(key=lambda row: (-row[1]["score"], row[0]))
    return [name for name, _ in rows]


def product_page(text, product):
    return summarize(by_product(parse_reviews(text)).get(product, []))
