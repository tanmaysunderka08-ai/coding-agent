UNLIMITED = object()

PLANS = {"free": "100", "team": "1000", "enterprise": "unlimited"}


def parse_limit(text):
    if text.startswith("custom:"):
        return int(text.split(":", 1)[1])
    if text == "unlimited":
        return UNLIMITED
    return int(text)


def limit_for(plan):
    return parse_limit(PLANS.get(plan, plan))
