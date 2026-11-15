from defaults import DEFAULTS, PROFILES
from loader import parse_env, set_path
from merge import deep_merge, flatten

_profiles = {}


def profile_config(name):
    if name not in PROFILES:
        raise ValueError(f"unknown profile: {name}")
    if name not in _profiles:
        _profiles[name] = deep_merge(DEFAULTS, PROFILES[name])
    return _profiles[name]


def load_config(profile, env_text=""):
    config = profile_config(profile)
    for dotted, value in parse_env(env_text):
        set_path(config, dotted, value)
    return config


def describe(profile, env_text=""):
    return [f"{k} = {v}" for k, v in sorted(flatten(load_config(profile, env_text)).items())]
