from Shapes import Circle, Rect
from Controller import Key
import Projectiles
import Util

class Damageable:
    def __init__(self, maxHealth, health=None):
        self.maxHealth = maxHealth
        self.health = maxHealth if health is None else health
        self.dead = False
    def takeDamage(self, dmg=1):
        self.health -= dmg
        self.dead = (self.health <= 0)
        return self.dead
    def heal(self, amount):
        self.health = min(self.health + amount, self.maxHealth)

class Shooter:
    def __init__(self):
        self.bullets = []
    def draw(self, canvas):
        for i in self.bullets:
            i.draw(canvas)
    def update(self):
        i = 0
        while i < len(self.bullets):
            done = self.bullets[i].update()
            if done:
                self.bullets.pop(i)
            else:
                i += 1

class Monster(Damageable):
    def __init__(self, row, col, player, speed, r, maxHealth, color, dmg=1, fireSpeed=10):
        super().__init__(maxHealth)
        self.pos = Util.Vector2(*Util.RCtoXY(row, col))
        self.player = player
        self.speed = speed
        self.body = Circle(self.pos.x, self.pos.y, r)
        self.color = color
        self.dmg = dmg
        self.shootCD = Util.Timer(fireSpeed)
    def move(self, delta):
        self.pos += delta
        self.body.x, self.body.y = self.pos.x, self.pos.y

    def moveTo(self, pos):
        self.pos = pos
        self.body.x, self.body.y = self.pos.x, self.pos.y

    def update(self):
        pass
    def draw(self, canvas):
        self.body.draw(canvas, fill=self.color)
    def hitbox(self):
        return self.body

class Fly(Monster):
    def __init__(self, row, col, player):
        super().__init__(row, col, player, 2, 5, 5, "blue")
    def update(self):
        super(Fly, self).update()
        self.shootCD.update()
        delta = self.player.pos - self.pos
        if delta.magnitude() < self.speed:
            self.moveTo(self.player.pos)
        else:
            delta.normalize(self.speed)
            self.move(delta)
        if self.hitbox().collide(self.player.hitbox()) and self.shootCD.ended():
            self.shootCD.reset()
            self.player.takeDamage(self.dmg)
            # print(2)




class Player(Damageable, Shooter):
    POS = [Util.Vector2(Util.WIDTH/2, Util.HEIGHT-Util.SIZE),
           Util.Vector2(Util.SIZE, Util.HEIGHT/2),
           Util.Vector2(Util.WIDTH/2, Util.SIZE),
           Util.Vector2(Util.WIDTH-Util.SIZE, Util.HEIGHT/2)]
    def __init__(self, grid):
        super().__init__(10, 3)
        super(Damageable, self).__init__()
        self.grid = grid
        self.app = grid.app
        self.room = self.grid.currentRoom
        self.speed = 5
        self.facing = Util.Vector2.S()

        self.size = 75/2
        margin = 10
        self.pos = Util.Vector2(margin+13 * self.size, 100)
        # self.x = margin+Rooms.DungeonRoom.COLUMNS / 2 * size
        # self.y = 100
        self.shootCD = Util.Timer(10)
        # self.y = Rooms.DungeonRoom.ROWS / 2 * size
        self.body = Rect(self.pos.x, self.pos.y, self.size, self.size)
    def setPos(self, direction):
        self.pos = self.POS[direction]
        self.room = self.grid.currentRoom
    def moveBy(self, delta):
        self.pos += delta
        self.body.move(self.pos.x, self.pos.y)
        # step = self.speed * 2
        for obs in self.room.obstacles:
            if self.body.collide(obs.rect):
                self.pos -= delta
                self.body.move(self.pos.x, self.pos.y)
                break

        self.pos.x = max(10+self.size/2, min(self.pos.x, self.app.width-10-self.size/2))
        self.pos.y = max(10+self.size/2, min(self.pos.y, self.app.height-10-self.size/2))
        self.body.move(self.pos.x, self.pos.y)

    def shoot(self):
        self.bullets.append(Projectiles.Bullet(self.room.obstacles+self.room.monsters, self.pos, self.facing, 3))
        self.shootCD.reset()

    def hitbox(self):
        return self.body

    def update(self):
        delta = Util.Vector2.ZERO()
        if Key.getKey("Left").pressed:
            # print(Key.getKey("Shoot").pressed)
            delta += Util.Vector2.W()
        if Key.getKey("Right").pressed:
            delta += Util.Vector2.E()
            # print(Key.getKey("Right").history)
        if Key.getKey("Up").pressed:
            delta += Util.Vector2.N()
        if Key.getKey("Down").pressed:
            delta += Util.Vector2.S()
        if (delta.x == 0) != (delta.y == 0):
            self.facing = delta
        delta.normalize(self.speed)
        self.moveBy(delta)
        if self.room.cleared():
            for i, r in enumerate(self.room.doors):
                if r and self.body.collide(r):
                    self.grid.moveTo(i)
        self.shootCD.update()
        super().update()
        if Key.getKey("Shoot").pressed and self.shootCD.ended():
            self.shoot()
    def draw(self, canvas):
        self.body.draw(canvas, fill="red")
        super().draw(canvas)

    def __repr__(self):
        return f"Player({self.pos.x} {self.pos.y})"