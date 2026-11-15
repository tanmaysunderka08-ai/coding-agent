def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def weighted_mean(pairs):
    weighted_sum = 0.0
    total_weight = 0.0
    count = 0
    for value, weight in pairs:
        weighted_sum += value * weight
        total_weight += weight
        count += 1
    if count == 0:
        return 0.0
    return weighted_sum / count


def shrink(value, n, prior=3.0, strength=4):
    return (value * n + prior * strength) / (n + strength)
