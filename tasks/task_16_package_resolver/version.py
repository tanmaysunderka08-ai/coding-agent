import re
from dataclasses import dataclass

_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def parse_version(text):
    m = _PATTERN.match(text.strip())
    if not m:
        raise ValueError(f"bad version: {text!r}")
    return Version(*map(int, m.groups()))
