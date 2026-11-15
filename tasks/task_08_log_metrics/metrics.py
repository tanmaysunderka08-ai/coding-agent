from collections import Counter


def status_classes(requests):
    return dict(sorted(Counter(f"{r.status // 100}xx" for r in requests).items()))


def slow(requests, limit_ms=1000):
    return sorted({r.path for r in requests if r.duration_ms > limit_ms})


def errors_by_user(requests):
    counts = Counter(r.user for r in requests if r.status >= 500)
    return dict(sorted(counts.items()))


def error_messages(requests):
    return sorted({r.message for r in requests if r.status >= 500 and r.message})
