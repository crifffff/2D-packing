class Gap:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

        self.prior = self.next = None

    def __lt__(self, other):
        return self.y < other.y

    def __le__(self, other):
        return self.y <= other.y

    def __repr__(self):
        return "{}-{}-{}".format(self.x, self.y, self.w)
