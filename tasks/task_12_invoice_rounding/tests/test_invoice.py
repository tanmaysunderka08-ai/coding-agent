from render import instalments, render

SIMPLE = """
Cable   | 1 | 0.125 | zero
Adapter | 7 | 1.15  | reduced
"""

ORDER = """
Widget  | 3 | 2.675 | standard
Fuse    | 3 | 1.115 | standard
Cable   | 1 | 0.125 | zero
"""


def test_simple_invoice():
    assert render(SIMPLE) == [
        "Cable       1 x 0.125 = 0.13 + 0.00",
        "Adapter     7 x 1.15 = 8.05 + 0.40",
        "TOTAL 8.18 + 0.40 = 8.58",
    ]


def test_order_lines():
    lines = render(ORDER)
    assert lines[0] == "Widget      3 x 2.675 = 8.03 + 1.45"
    assert lines[1] == "Fuse        3 x 1.115 = 3.35 + 0.60"


def test_order_total():
    assert render(ORDER)[-1] == "TOTAL 11.51 + 2.05 = 13.56"


def test_instalments():
    assert instalments(ORDER, 3) == ["4.52", "4.52", "4.52"]
    assert instalments(SIMPLE, 4) == ["2.15", "2.15", "2.14", "2.14"]
