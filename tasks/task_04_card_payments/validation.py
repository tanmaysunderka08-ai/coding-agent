from brands import brand_of, cvv_length
from cards import checksum_ok, is_plausible, normalize


def expiry_ok(expiry, today):
    month, year = expiry.split("/")
    month, year = int(month), 2000 + int(year)
    if not 1 <= month <= 12:
        return False
    if year != today.year:
        return year > today.year
    return month >= today.month


def validate(number, expiry, cvv, today):
    if not is_plausible(number):
        return ["card number has the wrong format"]
    errors = []
    digits = normalize(number)
    if not checksum_ok(digits):
        errors.append("card number is not valid")
    brand = brand_of(digits)
    if brand is None:
        errors.append("card type is not accepted")
    if not expiry_ok(expiry, today):
        errors.append("card has expired")
    if not (cvv.isdigit() and len(cvv) == cvv_length(brand)):
        errors.append("security code is wrong")
    return errors
