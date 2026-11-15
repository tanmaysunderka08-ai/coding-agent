from ring import RingBuffer


class Monitor:
    def __init__(self, keep=5):
        self.keep = keep
        self.history = {}

    def record(self, check):
        self.history.setdefault(check.service, RingBuffer(self.keep)).append(check)

    def last(self, service):
        latest = self.history[service].latest(1)
        return latest[0] if latest else None

    def recent(self, service, n):
        return self.history[service].latest(n)

    def uptime(self, service):
        checks = self.history[service].items()
        return round(100 * sum(c.ok for c in checks) / len(checks), 1)
