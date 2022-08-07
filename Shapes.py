class Collision:
    @staticmethod
    def pointRect(x, y, r):
        return r.left <= x <= r.right and r.top <= y <= r.bottom

    @staticmethod
    def pointCircle(x, y, c):
        return (c.x-x)**2+(c.y-y)**2 <= c.r**2
    @staticmethod
    def rects(r1, r2):
        return r1.right >= r2.left and r1.left <= r2.right and \
               r1.bottom >= r2.top and r1.top <= r2.bottom
    @staticmethod
    def circleRect(c, r):
        x = max(r.left, min(c.x, r.right))
        y = max(r.top, min(c.y, r.bottom))
        return Collision.pointCircle(x, y, c)

    @staticmethod
    def circles(c1, c2):
        return (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2 <= (c1.r+c2.r) ** 2



class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    def collide(self, obj, y=None):
        if y is not None:
            Collision.pointCircle(obj, y, self)
        elif isinstance(obj, Circle):
            return Collision.circles(self, obj)
        elif isinstance(obj, Rect):
            return Collision.circleRect(self, obj)
        elif isinstance(obj, list):
            for i in obj:
                if self.collide(i):
                    return True
            return False
        raise ValueError("Invalid collision")
    def draw(self, canvas, *args, **kwargs):
        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           *args, **kwargs)




class Rect:
    def __init__(self, x, y, w, h, *, anchor="c"):
        self.w = w
        self.h = h
        self.move(x, y, anchor=anchor)

    def move(self, x, y, *, anchor="c"):
        anchor = anchor.lower()
        if anchor == 'c':
            self.x = x - self.w / 2
            self.y = y - self.h / 2
        elif anchor == 'n':
            self.x = x - self.w / 2
            self.y = y
        elif anchor == 'ne':
            self.x = x - self.w
            self.y = y
        elif anchor == 'e':
            self.x = x - self.w
            self.y = y - self.h / 2
        elif anchor == 'se':
            self.x = x - self.w
            self.y = y - self.h
        elif anchor == 's':
            self.x = x - self.w / 2
            self.y = y - self.h
        elif anchor == 'sw':
            self.x = x
            self.y = y - self.h
        elif anchor == 'w':
            self.x = x
            self.y = y - self.h / 2
        elif anchor == 'nw':
            self.x = x
            self.y = y
        else:
            raise ValueError("Invalid anchor")

    def collide(self, obj, y=None):
        if isinstance(y, int):
            return Collision.pointRect(obj, y, self)
        elif isinstance(obj, Circle):
            return Collision.circleRect(obj, self)
        elif isinstance(obj, Rect):
            return Collision.rects(self, obj)
        elif isinstance(obj, list):
            for i in obj:
                if self.collide(i):
                    return True
            return False
        raise ValueError("Invalid collision")

    def draw(self, canvas, *args, **kwargs):
        canvas.create_rectangle(self.left, self.top,
                           self.right, self.bottom,
                           *args, **kwargs)



    # region Properties
    @property
    def left(self):
        return self.x
    @property
    def right(self):
        return self.x+self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def topleft(self):
        return self.left, self.top

    @property
    def topright(self):
        return self.right, self.top

    @property
    def centerX(self):
        return self.x+self.w/2

    @property
    def centerY(self):
        return self.y + self.h / 2

    @property
    def center(self):
        return self.centerX, self.centerY

    @property
    def bottomleft(self):
        return self.left, self.bottom

    @property
    def bottomright(self):
        return self.right, self.bottom

    @property
    def midleft(self):
        return self.left, self.centerY

    @property
    def midright(self):
        return self.right, self.centerY

    @property
    def midtop(self):
        return self.centerX, self.top

    @property
    def midbottom(self):
        return self.centerX, self.bottom
    # endregion


