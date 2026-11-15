import pytest

from config import describe, load_config

BASE = {
    "server": {"host": "0.0.0.0", "port": 8000, "workers": 2},
    "db": {"url": "sqlite:///app.db", "pool": {"size": 5, "timeout": 30}},
    "features": {"signup": True, "beta": False},
    "log_level": "info",
}


def test_unknown_profile():
    with pytest.raises(ValueError):
        load_config("staging")


def test_env_overrides():
    env = "APP__SERVER__PORT=9000\nAPP__FEATURES__BETA=true\nPATH=/usr/bin\n# APP__LOG_LEVEL=debug\n"
    config = load_config("prod", env)
    assert config["server"]["port"] == 9000
    assert config["features"]["beta"] is True
    assert config["log_level"] == "info"


def test_dev_settings():
    assert describe("dev") == [
        "db.pool.size = 1",
        "db.pool.timeout = 30",
        "db.url = sqlite:///app.db",
        "features.beta = False",
        "features.signup = True",
        "log_level = debug",
        "server.host = 0.0.0.0",
        "server.port = 8000",
        "server.workers = 2",
    ]


def test_prod_settings():
    config = load_config("prod")
    assert config["db"] == {"url": "postgres://db/app", "pool": {"size": 20, "timeout": 30}}
    assert config["server"] == {"host": "0.0.0.0", "port": 8000, "workers": 8}


def test_override_applies_to_one_load_only():
    assert load_config("test", "APP__DB__POOL__SIZE=3")["db"]["pool"]["size"] == 3
    assert load_config("test")["db"]["pool"]["size"] == 5


def test_base_profile_after_others():
    for name in ("prod", "dev", "test"):
        load_config(name)
    load_config("test", "APP__SERVER__WORKERS=4")
    assert load_config("base") == BASE
