from quota import blocked, remaining, warning


def call(account):
    if blocked(account):
        return 429, {"X-Remaining": "0"}
    account.used += 1
    headers = {}
    left = remaining(account)
    if left is not None:
        headers["X-Remaining"] = str(left)
    if warning(account):
        headers["X-Quota-Warning"] = "true"
    return 200, headers
