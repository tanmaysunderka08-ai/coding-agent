from datetime import date, timedelta

from dashboard import daily_report, trend, weekly_summary
from events import parse_events

D = date(2026, 11, 30)
ACTIVITY = {"u1": [0], "u2": [3], "u3": [6], "u4": [7, 20], "u5": [29, 40], "u6": [30], "u7": [14], "u8": [13]}


def events():
    lines = [f"{(D - timedelta(days=ago)).isoformat()}, {user}, open"
             for user, agos in ACTIVITY.items() for ago in agos]
    return parse_events("\n".join(lines))


def test_quiet_day_report():
    report = daily_report(events(), D + timedelta(days=60))
    assert report["dau"] == 0 and report["wau"] == 0 and report["stickiness"] == 0.0


def test_calendar_week():
    assert weekly_summary(events(), D)["calendar_week_actives"] == 1


def test_report_for_end_of_month():
    assert daily_report(events(), D) == {
        "day": "2026-11-30", "dau": 1, "wau": 3, "mau": 7,
        "stickiness": 0.33, "churned": ["u5", "u6", "u7"],
    }


def test_trend_over_two_days():
    assert trend(events(), [D, D - timedelta(days=1)]) == [("2026-11-30", 3), ("2026-11-29", 3)]


def test_growth_week_over_week():
    assert weekly_summary(events(), D)["growth"] == 0.5
