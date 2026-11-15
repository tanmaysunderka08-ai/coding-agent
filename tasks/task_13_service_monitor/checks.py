from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    minute: int
    service: str
    ok: bool
    latency_ms: int


def parse_checks(text):
    checks = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        minute, service, result, latency = [p.strip() for p in line.split(",")]
        checks.append(Check(int(minute), service, result == "ok", int(latency)))
    return checks
