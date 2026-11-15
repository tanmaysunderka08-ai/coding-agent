from invoice import line_amounts, parse_lines, totals
from money import fmt, split_evenly


def render(text):
    lines = parse_lines(text)
    out = []
    for line in lines:
        net, tax = line_amounts(line)
        out.append(f"{line.description:<10}{line.qty:>3} x {line.price} = {fmt(net)} + {fmt(tax)}")
    t = totals(lines)
    out.append(f"TOTAL {fmt(t['net'])} + {fmt(t['tax'])} = {fmt(t['gross'])}")
    return out


def instalments(text, parts):
    return [fmt(s) for s in split_evenly(totals(parse_lines(text))["gross"], parts)]
