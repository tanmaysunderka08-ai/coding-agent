from catalog import PRODUCTS, name_of
from inventory import parse_counts, stock_level
from reorder import arrival, needs_reorder, order_quantity


def reorder_plan(counts_text, today):
    counts = parse_counts(counts_text)
    plan = []
    for sku in sorted(PRODUCTS):
        level = stock_level(counts, sku)
        if needs_reorder(sku, level):
            qty = order_quantity(sku, level)
            if qty > 0:
                plan.append({"sku": sku, "name": name_of(sku), "order": qty,
                             "arrives": arrival(sku, today).isoformat()})
    return plan
