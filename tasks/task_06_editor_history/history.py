class History:
    def __init__(self, limit=100):
        self.limit = limit
        self._undo = []
        self._redo = []

    def run(self, command, doc):
        command.do(doc)
        self._undo.append(command)
        if len(self._undo) > self.limit:
            self._undo.pop(0)
        self._redo.clear()

    def undo(self, doc):
        if not self._undo:
            return False
        command = self._undo.pop()
        command.undo(doc)
        self._redo.append(command)
        return True

    def redo(self, doc):
        if not self._redo:
            return False
        command = self._redo.pop()
        command.do(doc)
        self._undo.append(command)
        return True
