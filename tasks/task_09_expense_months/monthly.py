from collections import defaultdict

from dates import month_key, month_name


def monthly_totals(bills):
    totals = defaultdict(float)
    for b in bills:
        totals[month_key(b.issued)] += b.amount
    return {k: round(v, 2) for k, v in sorted(totals.items())}


def monthly_table(bills):
    return [f"{month_name(k)}: {v:.2f}" for k, v in monthly_totals(bills).items()]
