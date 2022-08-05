from Util import *
from Shapes import Rect

class Obstacle:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.x, self.y = RCtoXY(r, c)
    def draw(self, canvas):
        pass

class Rock(Obstacle):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.rect = Rect(self.x, self.y, SIZE, SIZE)

    def draw(self, canvas):
        super().draw(canvas)
        self.rect.draw(canvas, fill="grey")
    def hitbox(self):
        return self.rect