class Vector:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __neg__(self):
        return Vector(self.X * -1, self.Y * -1)

    def __add__(self, other):
        return Vector(self.X + other.X, self.Y + other.Y)

    @property
    def pos(self):
        return (self.X, self.Y)
