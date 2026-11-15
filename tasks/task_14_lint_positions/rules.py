import re

MAX_LINE = 40


def trailing_whitespace(text):
    for m in re.finditer(r"[ \t]+$", text, re.MULTILINE):
        yield m.start(), "W291", "trailing whitespace"


def tab_indent(text):
    for m in re.finditer(r"^\t+", text, re.MULTILINE):
        yield m.start(), "W191", "indentation contains tabs"


def todo_comment(text):
    for m in re.finditer(r"#\s*TODO", text):
        yield m.start(), "T001", "TODO comment"


def bare_except(text):
    for m in re.finditer(r"^except\s*:", text, re.MULTILINE):
        yield m.start(), "E722", "bare except"


def long_line(text):
    offset = 0
    for line in text.split("\n"):
        if len(line) > MAX_LINE:
            yield offset + MAX_LINE, "E501", f"line too long ({len(line)} > {MAX_LINE})"
        offset += len(line) + 1


ALL_RULES = [trailing_whitespace, tab_indent, todo_comment, bare_except, long_line]
