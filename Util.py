import decimal

WIDTH, HEIGHT = 995, 545
SIZE = 75
UIBAR = 200
MARGIN = 10
UIX = WIDTH-UIBAR
ROWS, COLS = 7, 13
EXTRA = 5
MULTIPLIER = 1.33
TOTALWIDTH=WIDTH+UIBAR


# code from hw starter files
def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def RCtoXY(r, c):
    return SIZE*(c+.5)+MARGIN, SIZE*(r+.5)+MARGIN

def XYtoRC(x, y):
    return int((y-MARGIN)/SIZE), int((x-MARGIN)/SIZE)

class Timer:
    def __init__(self, duration, *, loop=False, paused=False):
        self.time = 0
        self.duration = duration
        self.loop = loop
        self.paused = paused
    def update(self):
        if self.paused:
            return
        if self.time < self.duration:
            self.time += 1
        else:
            if self.loop:
                self.time = 0
            return True
        return False
    def pause(self):
        self.paused = True
    def resume(self):
        self.paused = False
    def reset(self):
        self.time = 0
    def ended(self):
        return self.time == self.duration

class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def normalize(self, magnitude=1):
        if self.magnitude() == 0:
            return
        multiplier = magnitude/self.magnitude()
        self.x *= multiplier
        self.y *= multiplier
    def magnitude(self):
        return (self.x**2+self.y**2)**.5
    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)
    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)
    def __mul__(self, other):
        return Vector2(self.x*other, self.y*other)
    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)
    def __isub__(self, other):
        return self-other
    def __iadd__(self, other):
        return self + other

    def __idiv__(self, other):
        return self / other

    def __imul__(self, other):
        return self * other
    def unpack(self):
        return self.x, self.y
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    def copy(self):
        return Vector2(self.x, self.y)
    def __abs__(self):
        return self.magnitude()
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    @classmethod
    def N(cls, length=1):
        return Vector2(0, -length)
    @classmethod
    def S(cls, length=1):
        return Vector2(0, length)
    @classmethod
    def E(cls, length=1):
        return Vector2(length, 0)
    @classmethod
    def W(cls, length=1):
        return Vector2(-length, 0)
    @classmethod
    def ZERO(cls):
        return Vector2(0, 0)