from dates import days_between


def late_payments(bills, allowed_days=30):
    late = []
    for b in bills:
        if b.paid is not None and days_between(b.issued, b.paid) > allowed_days:
            late.append((b.payee, days_between(b.issued, b.paid)))
    return late


def unpaid(bills):
    return sorted(b.payee for b in bills if b.paid is None)
