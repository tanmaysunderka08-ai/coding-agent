import hashlib
from pathlib import Path

# pytest writes these by itself, they should not count as a change to the tests
IGNORED_DIRS = {"__pycache__", ".pytest_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def hash_directory(directory):
    # sha256 over (relative path, file bytes) of every file, in sorted order.
    # returns None if the folder does not exist.
    directory = Path(directory)
    if not directory.is_dir():
        return None

    h = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(directory)
        if IGNORED_DIRS.intersection(rel.parts) or path.suffix in IGNORED_SUFFIXES:
            continue
        h.update(rel.as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()
