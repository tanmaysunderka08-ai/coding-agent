"""Rows exported from the bank: 'DD/MM/YYYY; payee; amount; paid DD/MM/YYYY or -'."""

from dataclasses import dataclass

from dates import parse_date


@dataclass
class Bill:
    issued: object
    payee: str
    amount: float
    paid: object


def parse_statement(text):
    bills = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        issued, payee, amount, paid = [p.strip() for p in line.split(";")]
        bills.append(Bill(parse_date(issued), payee, float(amount),
                          None if paid == "-" else parse_date(paid)))
    return bills
