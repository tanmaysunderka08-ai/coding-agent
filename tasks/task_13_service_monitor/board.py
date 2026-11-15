from checks import parse_checks
from monitor import Monitor


def status_board(text, keep=5):
    monitor = Monitor(keep)
    for check in parse_checks(text):
        monitor.record(check)
    board = {}
    for service in sorted(monitor.history):
        last = monitor.last(service)
        board[service] = {
            "status": "up" if last.ok else "down",
            "since_minute": last.minute,
            "uptime": monitor.uptime(service),
            "recent_latency": [c.latency_ms for c in monitor.recent(service, 3)],
        }
    return board
