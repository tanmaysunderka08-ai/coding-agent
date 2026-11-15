from report import summary

LOG = """
level=info path=/api/users status=200 dur=35 user=u1
level=info path=/api/cart status=200 dur=1400.5 user=u2
level=error path=/api/pay status=502 dur=900 msg="card declined" user=u3
level=error path=/api/pay status=500 dur=1200 msg="timeout talking to bank" user="u7" region="eu west"
level=warn path=/api/login status=401 dur=12 msg="bad password" user="u2"
level=error path=/api/pay status=500 dur=80 user="u3" msg="card declined"
"""


def test_counts_and_slow_paths():
    report = summary(LOG)
    assert report["requests"] == 6
    assert report["statuses"] == {"2xx": 2, "4xx": 1, "5xx": 3}
    assert report["slow_paths"] == ["/api/cart", "/api/pay"]


def test_errors_by_user():
    assert summary(LOG)["errors_by_user"] == {"u3": 2, "u7": 1}


def test_error_messages():
    assert summary(LOG)["error_messages"] == ["card declined", "timeout talking to bank"]
