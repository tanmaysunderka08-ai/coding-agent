def review_weight(review):
    base = 2.0 if review.verified else 1.0
    return base + min(review.helpful, 10) / 10
