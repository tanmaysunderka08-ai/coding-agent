from accounts import parse_accounts
from gateway import call

ACCOUNTS = """
acme, free, 99
beta, free, 100
corp, team, 999
dyno, team, 1000
euro, enterprise, 123456
fizz, custom:500, 500
"""


def accounts():
    return parse_accounts(ACCOUNTS)


def test_free_plan():
    a = accounts()
    assert call(a["acme"]) == (200, {"X-Remaining": "0", "X-Quota-Warning": "true"})
    assert call(a["acme"]) == (429, {"X-Remaining": "0"})
    assert call(a["beta"]) == (429, {"X-Remaining": "0"})


def test_enterprise_is_unlimited():
    assert call(accounts()["euro"]) == (200, {})


def test_team_plan_last_call():
    a = accounts()
    assert call(a["corp"]) == (200, {"X-Remaining": "0", "X-Quota-Warning": "true"})
    assert call(a["corp"]) == (429, {"X-Remaining": "0"})


def test_team_plan_at_limit():
    assert call(accounts()["dyno"]) == (429, {"X-Remaining": "0"})


def test_custom_limit():
    assert call(accounts()["fizz"]) == (429, {"X-Remaining": "0"})
