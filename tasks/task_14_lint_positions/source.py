import bisect


class Source:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == "\n"]

    def line_of(self, offset):
        if not 0 <= offset <= len(self.text):
            raise IndexError(offset)
        return bisect.bisect_left(self.line_starts, offset)

    def position(self, offset):
        line = self.line_of(offset)
        return line, offset - self.line_starts[line - 1] + 1

    def line_text(self, line):
        start = self.line_starts[line - 1]
        end = self.text.find("\n", start)
        return self.text[start:] if end == -1 else self.text[start:end]
