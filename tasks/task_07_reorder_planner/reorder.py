import math
from datetime import timedelta

from catalog import setting


def needs_reorder(sku, level):
    return level < setting(sku, "min_stock")


def order_quantity(sku, level):
    missing = setting(sku, "max_stock") - level
    if missing <= 0:
        return 0
    pack = setting(sku, "pack")
    return math.ceil(missing / pack) * pack


def arrival(sku, today):
    return today + timedelta(days=setting(sku, "lead_days"))
