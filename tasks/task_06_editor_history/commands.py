class Insert:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text

    def do(self, doc):
        doc.insert(self.pos, self.text)

    def undo(self, doc):
        doc.delete(self.pos, self.pos + len(self.text))


class Delete:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.removed = ""

    def do(self, doc):
        self.removed = doc.delete(self.start, self.end)

    def undo(self, doc):
        doc.insert(self.end, self.removed)


class Replace:
    def __init__(self, start, end, new_text):
        self.parts = [Delete(start, end), Insert(start, new_text)]

    def do(self, doc):
        for part in self.parts:
            part.do(doc)

    def undo(self, doc):
        for part in reversed(self.parts):
            part.undo(doc)


class Move:
    def __init__(self, start, end, to):
        self.start, self.end, self.to = start, end, to
        self.cut = self.paste = None

    def do(self, doc):
        self.cut = Delete(self.start, self.end)
        self.cut.do(doc)
        pos = self.to - (self.end - self.start) if self.to > self.end else self.to
        self.paste = Insert(pos, self.cut.removed)
        self.paste.do(doc)

    def undo(self, doc):
        self.paste.undo(doc)
        self.cut.undo(doc)
