"""Sightings loaded from 'x, y, kind' lines (metres east/north of the city centre)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Sighting:
    x: float
    y: float
    kind: str


def parse_sightings(text):
    out = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        x, y, kind = [p.strip() for p in line.split(",")]
        out.append(Sighting(float(x), float(y), kind.lower()))
    return out


def of_kind(sightings, kind):
    return [s for s in sightings if s.kind == kind.lower()]
