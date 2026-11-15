from datetime import date

from cards import mask
from validation import validate

TODAY = date(2026, 11, 14)


def pay(amount, number, expiry, cvv, today=TODAY):
    errors = validate(number, expiry, cvv, today)
    if errors:
        return {"status": "declined", "reasons": errors}
    return {"status": "approved", "amount": round(amount, 2), "card": mask(number)}
