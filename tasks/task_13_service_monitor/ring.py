class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = [None] * capacity
        self.start = 0
        self.count = 0

    def append(self, item):
        end = (self.start + self.count) % self.capacity
        self.slots[end] = item
        if self.count < self.capacity:
            self.count += 1
        else:
            self.start = (self.start + 1) % self.capacity

    def items(self):
        return [self.slots[(self.start + i) % self.capacity] for i in range(self.count)]

    def latest(self, n):
        n = min(n, self.count)
        return [self.slots[(self.start + self.count - i) % self.capacity] for i in range(n)]

    def __len__(self):
        return self.count
