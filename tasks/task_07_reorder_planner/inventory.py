def parse_counts(text):
    counts = {}
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        sku, qty = [p.strip() for p in line.split(",")]
        counts[sku] = counts.get(sku, 0) + int(qty)
    return counts


def stock_level(counts, sku):
    return counts.get(sku, 0)
