from dataclasses import dataclass


@dataclass
class Request:
    level: str
    path: str
    status: int
    duration_ms: int
    user: str
    message: str


def to_request(fields):
    return Request(
        level=fields.get("level", "info"),
        path=fields.get("path", "?"),
        status=int(fields.get("status", "0") or 0),
        duration_ms=int(float(fields.get("dur", "0") or 0)),
        user=fields.get("user", "anonymous"),
        message=fields.get("msg", ""),
    )
