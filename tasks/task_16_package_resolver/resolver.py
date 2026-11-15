from ranges import matches, parse_range
from registry import deps_of, versions_of


class ResolutionError(Exception):
    pass


def best_match(name, rng_text):
    rng = parse_range(rng_text)
    candidates = [v for v in versions_of(name) if matches(v, rng)]
    if not candidates:
        raise ResolutionError(f"no version of {name} matches {rng_text}")
    return max(candidates)


def resolve(manifest):
    chosen = {}
    queue = list(manifest.items())
    while queue:
        name, rng_text = queue.pop(0)
        if name in chosen:
            if not matches(chosen[name], parse_range(rng_text)):
                raise ResolutionError(f"{name} {chosen[name]} does not satisfy {rng_text}")
            continue
        version = best_match(name, rng_text)
        chosen[name] = version
        queue.extend(deps_of(name, version).items())
    return chosen


def lockfile(manifest):
    return [f"{name}@{version}" for name, version in sorted(resolve(manifest).items())]
