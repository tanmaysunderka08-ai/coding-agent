DEFAULTS = {"min_stock": 5, "max_stock": 20, "pack": 1, "lead_days": 7}

PRODUCTS = {
    "MUG-RED": {"name": "Red mug", "pack": 6},
    "MUG-OLD": {"name": "Old logo mug", "min_stock": 0, "max_stock": 0},
    "PEN-BLU": {"name": "Blue pen", "min_stock": 50, "max_stock": 200, "pack": 25},
    "BAG-TOT": {"name": "Tote bag", "lead_days": 0, "max_stock": 12},
    "CAP-GRN": {"name": "Green cap", "min_stock": 2, "lead_days": 14},
}


def setting(sku, key):
    return PRODUCTS[sku].get(key) or DEFAULTS[key]


def name_of(sku):
    return PRODUCTS[sku]["name"]
