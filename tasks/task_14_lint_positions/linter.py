from rules import ALL_RULES
from source import Source


def lint(name, text, rules=ALL_RULES):
    src = Source(name, text)
    problems = []
    for rule in rules:
        for offset, code, message in rule(text):
            line, col = src.position(offset)
            problems.append((line, col, code, message))
    return sorted(problems)
