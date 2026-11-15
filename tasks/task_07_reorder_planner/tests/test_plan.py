from datetime import date

from report import reorder_plan

TODAY = date(2026, 11, 14)


def skus(plan):
    return [row["sku"] for row in plan]


def test_everything_well_stocked():
    counts = "MUG-RED, 30\nPEN-BLU, 120\nBAG-TOT, 9\nCAP-GRN, 4\nMUG-OLD, 3"
    assert reorder_plan(counts, TODAY) == []


def test_pens_and_mugs_running_low():
    counts = "MUG-RED, 3\nPEN-BLU, 20\nPEN-BLU, 10\nBAG-TOT, 9\nCAP-GRN, 4\nMUG-OLD, 3"
    assert reorder_plan(counts, TODAY) == [
        {"sku": "MUG-RED", "name": "Red mug", "order": 18, "arrives": "2026-11-21"},
        {"sku": "PEN-BLU", "name": "Blue pen", "order": 175, "arrives": "2026-11-21"},
    ]


def test_empty_warehouse():
    assert reorder_plan("", TODAY) == [
        {"sku": "BAG-TOT", "name": "Tote bag", "order": 12, "arrives": "2026-11-14"},
        {"sku": "CAP-GRN", "name": "Green cap", "order": 20, "arrives": "2026-11-28"},
        {"sku": "MUG-RED", "name": "Red mug", "order": 24, "arrives": "2026-11-21"},
        {"sku": "PEN-BLU", "name": "Blue pen", "order": 200, "arrives": "2026-11-21"},
    ]
