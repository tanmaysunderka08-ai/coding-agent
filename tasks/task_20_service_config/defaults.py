DEFAULTS = {
    "server": {"host": "0.0.0.0", "port": 8000, "workers": 2},
    "db": {"url": "sqlite:///app.db", "pool": {"size": 5, "timeout": 30}},
    "features": {"signup": True, "beta": False},
    "log_level": "info",
}

PROFILES = {
    "base": {},
    "dev": {"log_level": "debug", "db": {"pool": {"size": 1}}},
    "test": {"db": {"url": "sqlite://"}, "features": {"beta": True}},
    "prod": {"server": {"workers": 8}, "db": {"url": "postgres://db/app", "pool": {"size": 20}}},
}
