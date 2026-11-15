"""Card number helpers."""


def normalize(number):
    return "".join(ch for ch in number if ch.isdigit())


def is_plausible(number):
    digits = normalize(number)
    compact = number.replace(" ", "").replace("-", "")
    return 12 <= len(digits) <= 19 and len(digits) == len(compact)


def checksum_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def mask(number):
    digits = normalize(number)
    return "*" * (len(digits) - 4) + digits[-4:]
