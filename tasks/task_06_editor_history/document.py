class Document:
    def __init__(self, text=""):
        self.text = text

    def insert(self, pos, s):
        if not 0 <= pos <= len(self.text):
            raise IndexError(f"position {pos} out of range")
        self.text = self.text[:pos] + s + self.text[pos:]

    def delete(self, start, end):
        if not 0 <= start <= end <= len(self.text):
            raise IndexError(f"range {start}:{end} out of range")
        removed = self.text[start:end]
        self.text = self.text[:start] + self.text[end:]
        return removed

    def __len__(self):
        return len(self.text)
