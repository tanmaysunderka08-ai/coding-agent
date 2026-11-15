from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(x):
    return Decimal(x).quantize(CENT, rounding=ROUND_HALF_UP)


def split_evenly(total, parts):
    base = (total / parts).quantize(CENT, rounding="ROUND_DOWN")
    shares = [base] * parts
    remainder = int((total - base * parts) / CENT)
    for i in range(remainder):
        shares[i] += CENT
    return shares


def fmt(amount):
    return f"{amount:,.2f}"
