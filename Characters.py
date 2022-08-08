from Shapes import Circle, Rect
from Controller import Key
import Projectiles
from Util import *
import math, random

class Damageable:
    def __init__(self, maxHealth, health=None):
        self.maxHealth = maxHealth
        self.health = maxHealth if health is None else health
        self.dead = False
    def takeDamage(self, dmg=1):
        self.health = max(0, self.health-dmg)
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
    def __init__(self, row, col, player, speed, r, maxHealth, color, dmg=1, fireSpeed=30, *, absolutePos=False):
        super().__init__(maxHealth)
        self.pos = Vector2(row, col) if absolutePos else Vector2(*RCtoXY(row, col))
        self.player = player
        self.speed = speed
        self.body = Circle(self.pos.x, self.pos.y, r)
        self.color = color
        self.dmg = dmg
        self.shootCD = Timer(fireSpeed)
    def move(self, delta):
        self.pos += delta
        self.body.x, self.body.y = self.pos.x, self.pos.y

    def moveTo(self, pos):
        self.pos = pos
        self.body.x, self.body.y = self.pos.x, self.pos.y

    def update(self):
        self.shootCD.update()
        if self.hitbox().collide(self.player.hitbox()) and self.shootCD.ended():
            self.shootCD.reset()
            self.player.takeDamage(self.dmg)
    def draw(self, canvas):
        self.body.draw(canvas, fill=self.color)
    def hitbox(self):
        return self.body

class Fly(Monster):
    def __init__(self, row, col, player, *, absolutePos=False):
        super().__init__(row, col, player, 2, 5, 5, "red", absolutePos=absolutePos)
    def update(self):
        super(Fly, self).update()
        delta = self.player.pos - self.pos
        if delta.magnitude() < self.speed:
            self.moveTo(self.player.pos)
        else:
            delta.normalize(self.speed)
            self.move(delta)

class Horf(Monster, Shooter):
    def __init__(self, row, col, player):
        super().__init__(row, col, player, 0, 30, 10, "red")
        super(Damageable, self).__init__()
        self.CD = Timer(50)

    def shoot(self):
        for d in [Vector2.N(), Vector2.S(), Vector2.E(), Vector2.W()]:
            self.bullets.append(Projectiles.Bullet([self.player]+self.player.room.obstacles, self.pos, d * 10, 1, color="red"))
        self.CD.reset()
    def update(self):
        super().update()
        super(Damageable, self).update()
        self.CD.update()
        if self.CD.ended():
            self.shoot()

    def draw(self, canvas):
        super().draw(canvas)
        super(Damageable, self).draw(canvas)
        canvas.create_text(self.pos.x, self.pos.y, text="Horf")



class Gaper(Monster):
    def __init__(self, row, col, player):
        super().__init__(row, col, player, 3, 30, 10, "red")
        self.moving = 0
        self.direction = None
        self.maxMoving = SIZE/self.speed
    def update(self):
        super(Gaper, self).update()
        if self.moving:
            self.move(self.direction)
            self.moving += 1
            if self.moving == self.maxMoving:
                self.moving = 0
            return
        r, c = XYtoRC(self.pos.x, self.pos.y)
        djikstra = self.player.room.djikstra()
        for delta in [Vector2.N(), Vector2.E(), Vector2.S(), Vector2.W()]:
            nr, nc = r+delta.y, c+delta.x
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if djikstra[r][c] <= djikstra[nr][nc]:
                    continue
                direction = delta * self.speed
                self.direction = direction
                self.moving += 1
                self.move(self.direction)
                break

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.pos.x, self.pos.y, text="Gaper")

class OrbitFly(Fly):
    SPEED = 0.1
    RADIUS = 100
    def __init__(self, player, duke, angle):
        super().__init__(0, 0, player)
        self.duke = duke
        self.angle = angle
        self.angleToPos()
    def angleToPos(self):
        x = self.RADIUS * math.cos(self.angle) + self.duke.pos.x
        y = self.RADIUS * math.sin(self.angle) + self.duke.pos.y
        self.moveTo(Vector2(x, y))
    def update(self):
        super(Fly, self).update()
        self.angle += self.SPEED
        self.angleToPos()


class DukeOfFlies(Monster):
    NSPAWN = 3
    MAXORBIT = 4
    MAXSPAWN = 12
    def __init__(self, row, col, player):
        super().__init__(row, col, player, 3, 70, 110, "red", )
        self.delta = Vector2.N() if random.random() >.5 else Vector2.S()
        self.delta += Vector2.E() if random.random() >.5 else Vector2.W()
        self.orbits = []
        self.cd = Timer(200)
    def spawnOrbit(self):
        start = random.uniform(0, math.pi)
        for i in range(self.NSPAWN):
            fly = OrbitFly(self.player, self, start+i)
            self.orbits.append(fly)
            self.player.room.monsters.append(fly)
    def spawnAttack(self):
        self.player.room.monsters.append(Fly(self.pos.x, self.pos.y, self.player, absolutePos=True))
    def release(self):
        monsters = self.player.room.monsters
        for i, m in enumerate(monsters):
            if isinstance(m, OrbitFly):
                fly = Fly(m.pos.x, m.pos.y, self.player, absolutePos=True)
                fly.health = m.health
                monsters[i] = fly


    def takeDamage(self, dmg=1):
        dead = super().takeDamage(dmg)
        if self.dead:
            self.release()
        return dead

    def update(self):
        super().update()
        self.cd.update()
        self.orbits = [i for i in self.orbits if i.health>0]
        self.move(self.delta)
        if not (MARGIN+self.body.r<self.pos.x<WIDTH-MARGIN-self.body.r):
            self.delta.x *= -1
        if not (MARGIN+self.body.r<self.pos.y<HEIGHT-MARGIN-self.body.r):
            self.delta.y *= -1
        if len(self.player.room.monsters) < self.MAXSPAWN and self.cd.ended():
            if len(self.orbits) >= 4:
                self.spawnAttack()
            else:
                if random.random() > .5:
                    self.spawnAttack()
                else:
                    self.spawnOrbit()
            self.cd.reset()

    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.pos.x, self.pos.y, text="Duke of Flies")


class Player(Damageable, Shooter):
    POS = [Vector2(WIDTH/2, HEIGHT-SIZE/2),
           Vector2(SIZE/2, HEIGHT/2),
           Vector2(WIDTH/2, SIZE/2),
           Vector2(WIDTH-SIZE/2, HEIGHT/2),
           Vector2(WIDTH/2, HEIGHT/2)]
    def __init__(self, grid):
        super().__init__(10, 6)
        super(Damageable, self).__init__()
        self.grid = grid
        self.app = grid.app
        self.room = None
        self.speed = 5
        self.facing = Vector2.S() * self.speed

        self.size = SIZE/2
        self.pos = Vector2(MARGIN+13 * self.size, 100)
        self.shootCD = Timer(10)
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

        self.pos.x = max(MARGIN+self.size/2, min(self.pos.x, WIDTH-MARGIN-self.size/2))
        self.pos.y = max(MARGIN+self.size/2, min(self.pos.y, HEIGHT-MARGIN-self.size/2))
        self.body.move(self.pos.x, self.pos.y)

    def shoot(self):
        self.bullets.append(Projectiles.Bullet(self.room.obstacles+self.room.monsters, self.pos, self.facing*2, 3))
        self.shootCD.reset()

    def hitbox(self):
        return self.body

    def update(self):
        delta = Vector2.ZERO()
        if Key.getKey("Left").pressed:
            # print(Key.getKey("Shoot").pressed)
            delta += Vector2.W()
        if Key.getKey("Right").pressed:
            delta += Vector2.E()
            # print(Key.getKey("Right").history)
        if Key.getKey("Up").pressed:
            delta += Vector2.N()
        if Key.getKey("Down").pressed:
            delta += Vector2.S()
        if delta.x or delta.y:
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
        self.body.draw(canvas, fill="blue")
        x, y = (self.pos+self.facing*2).unpack()
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
        super().draw(canvas)
        canvas.create_text(WIDTH+MARGIN, 200+MARGIN, text=f"Health: {self.health}",
                           font="Arial 30", anchor="nw")

    def __repr__(self):
        return f"Player({self.pos.x} {self.pos.y})"