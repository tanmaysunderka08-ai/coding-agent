from version import parse_version

REGISTRY = {
    "left-pad": {"1.0.0": {}, "1.1.0": {}, "1.3.0": {}, "2.0.0": {}},
    "chalk": {"2.0.0": {"ansi": "^3.0.0"}, "2.4.1": {"ansi": "^3.1.0"}, "3.0.0": {"ansi": "^4.0.0"}},
    "ansi": {"3.0.0": {}, "3.0.2": {}, "3.2.0": {}, "4.0.0": {}},
    "colors": {"1.2.0": {}, "1.2.7": {}, "1.3.0": {}},
    "tiny-json": {"0.2.1": {}, "0.2.4": {}, "0.3.0": {}, "0.9.0": {}},
    "nano-id": {"0.0.3": {}, "0.0.4": {}, "0.1.0": {}},
    "yaml-lite": {
        "0.4.0": {"tiny-json": "^0.2.0"},
        "0.4.2": {"tiny-json": "~0.2.3"},
        "0.5.0": {"tiny-json": "^0.3.0"},
    },
}


def versions_of(name):
    if name not in REGISTRY:
        raise LookupError(f"unknown package: {name}")
    return sorted(parse_version(v) for v in REGISTRY[name])


def deps_of(name, version):
    return REGISTRY[name][str(version)]
