from metrics import churned, dau, growth, mau, wau, week_actives


def daily_report(events, day):
    d, w, m = dau(events, day), wau(events, day), mau(events, day)
    return {
        "day": day.isoformat(),
        "dau": d,
        "wau": w,
        "mau": m,
        "stickiness": round(d / w, 2) if w else 0.0,
        "churned": churned(events, day),
    }


def trend(events, days):
    return [(day.isoformat(), wau(events, day)) for day in days]


def weekly_summary(events, day):
    return {"calendar_week_actives": week_actives(events, day), "growth": growth(events, day)}
