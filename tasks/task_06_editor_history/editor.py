from commands import Delete, Insert, Move, Replace
from document import Document
from history import History


class Editor:
    def __init__(self, text="", history_limit=100):
        self.doc = Document(text)
        self.history = History(history_limit)

    @property
    def text(self):
        return self.doc.text

    def type(self, pos, s):
        self.history.run(Insert(pos, s), self.doc)

    def erase(self, start, end):
        self.history.run(Delete(start, end), self.doc)

    def replace(self, start, end, s):
        self.history.run(Replace(start, end, s), self.doc)

    def move(self, start, end, to):
        self.history.run(Move(start, end, to), self.doc)

    def find_replace(self, old, new):
        i = self.text.find(old)
        if i == -1:
            return False
        self.replace(i, i + len(old), new)
        return True

    def undo(self):
        return self.history.undo(self.doc)

    def redo(self):
        return self.history.redo(self.doc)
