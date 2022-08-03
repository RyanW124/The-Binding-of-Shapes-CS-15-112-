from Shapes import Circle
import Characters

class Bullet:
    def __init__(self, hits, pos, speed, damage, _range=450, r=5):
        self.hits = hits
        self.speed = speed
        self.pos = self.start = pos
        self.range = _range
        self.damage = damage
        self.body = Circle(pos.x, pos.y, r)

    def hit(self, obj):
        if isinstance(obj, Characters.Damageable):
            obj.takeDamage(self.damage)


    def update(self):
        self.pos += self.speed
        if (self.pos-self.start).magnitude() >= self.range:
            return True
        self.body.x, self.body.y = self.pos.x, self.pos.y
        for obj in self.hits:
            if self.body.collide(obj.hitbox()):
                self.hit(obj)
                return True
        return False

    def draw(self, canvas):
        self.body.draw(canvas)