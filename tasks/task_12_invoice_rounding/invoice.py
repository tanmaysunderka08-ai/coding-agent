from dataclasses import dataclass

from money import to_money
from tax import tax_for


@dataclass
class Line:
    description: str
    qty: int
    price: object
    category: str


def parse_lines(text):
    lines = []
    for row in text.strip().splitlines():
        if not row.strip():
            continue
        description, qty, price, category = [p.strip() for p in row.split("|")]
        lines.append(Line(description, int(qty), float(price), category))
    return lines


def line_amounts(line):
    net = to_money(line.qty * line.price)
    tax = tax_for(net, line.category)
    return net, tax


def totals(lines):
    net = tax = to_money(0)
    for line in lines:
        n, t = line_amounts(line)
        net += n
        tax += t
    return {"net": net, "tax": tax, "gross": net + tax}
