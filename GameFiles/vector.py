import math

class Vector2(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.thresh = 0.000001
    # method to add two vectors
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    # method to subtract two vectors
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    # method to negate a vector
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    #method to multipy two vectors
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    #method to divide two vectors
    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None
    #used depending on python version
    def __truediv__(self, scalar):
        return self.__div__(scalar)

    # checks the equality of two vectors
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    #useful for comparing the lengths of vectors
    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    #finds the magnitue length of a vector
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    # returns a copy of our vector
    def copy(self):
        return Vector2(self.x, self.y)

    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int (self.y)

    # prints out are vector
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.x)+">"