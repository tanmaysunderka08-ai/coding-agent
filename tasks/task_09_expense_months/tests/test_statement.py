from monthly import monthly_table, monthly_totals
from payments import late_payments, unpaid
from statement import parse_statement

DATA = """
03/04/2026; Power Co; 1200; 10/04/2026
10/04/2026; Landlord; 15000; 11/04/2026
05/03/2026; Water Board; 900; 09/04/2026
11/03/2026; Internet; 3000; -
02/02/2026; Insurance; 4800; 06/03/2026
"""


def test_unpaid():
    assert unpaid(parse_statement(DATA)) == ["Internet"]


def test_monthly_totals():
    assert monthly_totals(parse_statement(DATA)) == {
        "2026-02": 4800.0, "2026-03": 3900.0, "2026-04": 16200.0}


def test_monthly_table():
    assert monthly_table(parse_statement(DATA)) == [
        "February 2026: 4800.00", "March 2026: 3900.00", "April 2026: 16200.00"]


def test_late_payments():
    assert late_payments(parse_statement(DATA)) == [("Water Board", 35), ("Insurance", 32)]
