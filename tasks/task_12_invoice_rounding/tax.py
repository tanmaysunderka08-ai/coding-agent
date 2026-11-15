from decimal import Decimal

from money import to_money

RATES = {"standard": Decimal("0.18"), "reduced": Decimal("0.05"), "zero": Decimal("0")}


def tax_for(net, category):
    return to_money(net * RATES[category])
