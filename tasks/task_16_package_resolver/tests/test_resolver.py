import pytest

from resolver import ResolutionError, lockfile


def test_web_app():
    manifest = {"left-pad": "^1.1.0", "chalk": "^2.0.0", "colors": "~1.2.0"}
    assert lockfile(manifest) == ["ansi@3.2.0", "chalk@2.4.1", "colors@1.2.7", "left-pad@1.3.0"]


def test_pinned_and_open_ranges():
    assert lockfile({"left-pad": ">=1.1.0", "colors": "1.2.0"}) == ["colors@1.2.0", "left-pad@2.0.0"]


def test_unknown_package():
    with pytest.raises(LookupError):
        lockfile({"left-padd": "^1.0.0"})


def test_conflicting_requirements():
    with pytest.raises(ResolutionError):
        lockfile({"tiny-json": "^0.3.0", "yaml-lite": "0.4.2"})


def test_cli_tool():
    assert lockfile({"tiny-json": "^0.2.1", "nano-id": "^0.0.3"}) == ["nano-id@0.0.3", "tiny-json@0.2.4"]


def test_config_loader():
    manifest = {"yaml-lite": "^0.4.0", "tiny-json": "^0.2.0"}
    assert lockfile(manifest) == ["tiny-json@0.2.4", "yaml-lite@0.4.2"]
