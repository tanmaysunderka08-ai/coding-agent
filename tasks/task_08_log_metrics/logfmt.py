"""Parser for logfmt lines: key=value pairs, values may be "quoted"."""

import re

PAIR = re.compile(r'(\w+)=(?:"(.*)"|(\S*))')


def parse_line(line):
    fields = {}
    for key, quoted, bare in PAIR.findall(line):
        fields[key] = quoted if quoted else bare
    return fields


def parse_lines(text):
    return [parse_line(line) for line in text.splitlines() if line.strip()]
