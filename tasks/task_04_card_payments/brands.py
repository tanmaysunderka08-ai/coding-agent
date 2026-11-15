def brand_of(digits):
    if digits.startswith(("34", "37")) and len(digits) == 15:
        return "amex"
    if digits[0] == "4" and len(digits) in (13, 16, 19):
        return "visa"
    first_two, first_four = int(digits[:2]), int(digits[:4])
    if (51 <= first_two <= 55 or 2221 <= first_four <= 2720) and len(digits) == 16:
        return "mastercard"
    if digits.startswith("6011") and len(digits) == 16:
        return "discover"
    return None


def cvv_length(brand):
    return 4 if brand == "amex" else 3
