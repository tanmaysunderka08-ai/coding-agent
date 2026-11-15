from linter import lint
from source import Source


def format_problems(name, text):
    return [f"{name}:{line}:{col}: {code} {msg}" for line, col, code, msg in lint(name, text)]


def with_context(name, text):
    src = Source(name, text)
    return [f"{line}| {src.line_text(line).strip()}  <- {code}" for line, _, code, _ in lint(name, text)]


def summary(name, text):
    counts = {}
    for _, _, code, _ in lint(name, text):
        counts[code] = counts.get(code, 0) + 1
    return dict(sorted(counts.items()))
