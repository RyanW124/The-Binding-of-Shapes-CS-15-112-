import Generation
import random
import Obstacles
import Characters
from Shapes import Rect
from Util import *

class DungeonRoom(Generation.Room):
    objectMap = {
        0: None,
        1: Obstacles.Rock,
        2: Characters.Fly,
        3: Characters.Gaper,
        4: Characters.DukeOfFlies,
        5: Characters.Horf
    }

    def __init__(self, room, player):
        super().__init__(room.grid, room.r, room.c)
        self.N, self.E, self.S, self.W = room.neighbors
        self.map = []
        self.obstacles = []
        self.player = player
        self.distances = None
        self.isBoss = False
        self.playerR, self.playerC = XYtoRC(self.player.pos.x, self.player.pos.y)
        self.visited = False
        self.monsters = []
        self.id = room.id
        self.doors = [None] * 4
        if self.N:
            self.doors[0] = Rect(WIDTH/2, 0, SIZE, MARGIN, anchor='n')
        if self.S:
            self.doors[2] = Rect(WIDTH/2, HEIGHT, SIZE, MARGIN, anchor='s')
        if self.E:
            self.doors[1] = Rect(WIDTH, HEIGHT/2, MARGIN, SIZE, anchor='e')
        if self.W:
            self.doors[3] = Rect(0, HEIGHT/2, MARGIN, SIZE, anchor='w')
        self.borders = [Rect(0, 0, WIDTH, MARGIN, anchor="nw"),
                        Rect(0, 0, MARGIN, HEIGHT, anchor="nw"),
                        Rect(WIDTH-MARGIN, 0, MARGIN, HEIGHT, anchor="nw"),
                        Rect(0, HEIGHT-MARGIN, WIDTH, MARGIN, anchor="nw")]
    def cleared(self):
        return not self.monsters
    def update(self):
        self.monsters = [i for i in self.monsters if i.health>0]
        for i in self.monsters:
            i.update()
    def initMap(self):
        if self.id == 0:
            return
        chapter = "Boss" if self.isBoss else "Basement"
        with open("Maps/"+chapter) as f:
            rooms = list(f)
        total = len(rooms)//(ROWS+1)
        chosen = random.randint(0, total)
        # 2 is rock 1 is river 0 is blank
        for r, line in enumerate(rooms[chosen*(ROWS+1):chosen*(ROWS+1)+ROWS]):
            row = []
            for c, obj in enumerate(line.split(' ')):
                cls = self.objectMap[int(obj)]
                if cls in [Obstacles.Rock]:
                    row.append(2)
                elif cls in []:
                    row.append(1)
                else:
                    row.append(0)
                if cls is not None:
                    if issubclass(cls, Obstacles.Obstacle):
                        self.obstacles.append(cls(r, c))
                    elif issubclass(cls, Characters.Monster):
                        self.monsters.append(cls(r, c, self.player))
                        # if issubclass(cls, Characters.Gaper):
                        #     self.distances = self.djikstra()

            self.map.append(row)
    def draw(self, canvas):
        color = "black" if self.cleared() else "grey"

        for i in self.borders:
            i.draw(canvas, fill="grey")
        for i in self.doors:
            if i:
                i.draw(canvas, fill=color)
        for i in self.obstacles+self.monsters:
            i.draw(canvas)
    # written with some reference to TP guide on pathfinding but using a priority queue instead of a
    # list of unvisited nodes
    def djikstra(self):
        r, c = XYtoRC(self.player.pos.x, self.player.pos.y)
        if r == self.playerR and self.playerC == c:
            return self.distances
        self.playerR, self.playerC = r, c
        visited = [[False] * COLS for _ in range(ROWS)]
        distance = [[float('inf')] * COLS for _ in range(ROWS)]
        distance[r][c] = 0
        queue = [(r, c)]
        visited[r][c] = True
        while queue:
            r, c = min(queue, key=lambda cell: distance[cell[0]][cell[1]])
            queue.remove((r, c))
            d = distance[r][c] + 1
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if not (0<=r+dr<ROWS and 0<=c+dc<COLS):
                    continue
                nr, nc = r+dr, c+dc
                if self.map[nr][nc] or visited[nr][nc]:
                    continue
                visited[nr][nc] = True
                queue.append((nr, nc))
                distance[nr][nc] = min(distance[nr][nc], d)
        self.distances = distance
        return distance

class BossRoom(DungeonRoom):

    def __init__(self, room, player):
        super().__init__(room, player)
        self.trapdoor = None
        self.boss = None
        self.isBoss = True

    def initMap(self):
        super().initMap()
        self.boss = self.monsters[0]

    def update(self):
        super().update()
        if self.cleared() and self.trapdoor is None:
            self.trapdoor = Rect(COLS/2*SIZE+MARGIN, ROWS/2*SIZE+MARGIN,
                                 SIZE, SIZE)
        if self.trapdoor is not None:
            if self.trapdoor.collide(self.player.hitbox()):
                self.grid.nextLevel()

    def draw(self, canvas):
        super().draw(canvas)
        if self.cleared():
            self.trapdoor.draw(canvas, fill="Black")
        else:
            canvas.create_text(WIDTH+UIBAR-MARGIN, HEIGHT-MARGIN,
                               text=f"Boss health: {self.boss.health}/{self.boss.maxHealth}",
                               anchor="se", font="Arial 20")


if __name__ == '__main__':
    pass