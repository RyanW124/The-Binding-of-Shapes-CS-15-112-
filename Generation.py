import random
import Characters
from Util import WIDTH, HEIGHT

class Grid:
    W, H = 200, 200
    MAPX, MAPY = WIDTH - 2, 0
    MAPS = 7
    CELLW, CELLH = W/MAPS, H/MAPS
    GAP = 5
    def __init__(self, app, size, n, depth):
        self.app = app
        self.size = size
        self.grid = [[Room(self, r, c) for c in range(self.size)]
                     for r in range(self.size)]
        self.n = n
        self.depth = depth
        self.wilson()
        self.rooms = []
        self.hub = self.end = None
        self.chooseRoom()
        self.pos = 0
        self.player = Characters.Player(self)
        self.rooms = [DungeonRoom(r, self.player) for r in self.rooms]
        for r in self.rooms:
            self[r.r, r.c] = r
        for r in self.rooms:
            if r.N:
                r.N = self[r.N.r, r.N.c]
            if r.E:
                r.E = self[r.E.r, r.E.c]
            if r.S:
                r.S = self[r.S.r, r.S.c]
            if r.W:
                r.W = self[r.W.r, r.W.c]
        self.player.room = self.currentRoom

    def moveTo(self, direction):
        if direction == 0:
            self.pos = self.getPos(self.currentRoom.N)
        elif direction == 1:
            self.pos = self.getPos(self.currentRoom.E)
        elif direction == 2:
            self.pos = self.getPos(self.currentRoom.S)
        elif direction == 3:
            self.pos = self.getPos(self.currentRoom.W)
        self.player.setPos(direction)
    def getPos(self, room):
        return self.rooms.index(room)
    @property
    def currentRoom(self):
        return self.rooms[self.pos]
    def chooseRoom(self):
        r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        self.hub = self[r, c]
        queue = [self.hub]
        i = 0
        while len(self.rooms) < self.n and queue:
            room = queue.pop(0)
            for nextRoom in room.neighbors:
                if nextRoom and nextRoom not in self.rooms:
                    self.rooms.append(nextRoom)
                    nextRoom.id = i
                    i += 1
                    queue.append(nextRoom)
        self.end = self.rooms[-1]
        for r, row in enumerate(self.grid):
            for c, room in enumerate(row):
                if room in self.rooms:
                    for i in room.neighbors:
                        if i is not None and i not in self.rooms:
                            room.connect(i, disconnect=True)
                else:
                    self[r, c] = None
    def draw(self, canvas):
        self.currentRoom.draw(canvas)

    def drawMap(self, canvas, room, x, y, *, start=False, near=False):
        canvas.create_rectangle(x*)
        if near:
            return





    def wilson(self):
        unvisited = [(i, j) for i in range(self.size) for j in range(self.size)]
        r, c = unvisited.pop(random.randint(0, self.size ** 2 - 1))
        visited = [[False] * self.size for _ in range(self.size)]
        visited[r][c] = True
        while unvisited:
            r, c = unvisited.pop(random.randint(0, len(unvisited) - 1))
            walked = [(r, c)]
            while not visited[r][c]:
                dr, dc = [float('inf')] * 2
                while not (0 <= r + dr < self.size and 0 <= c + dc < self.size):
                    dr, dc = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
                r += dr
                c += dc

                if (r, c) in walked:
                    index = walked.index((r, c))
                    walked = walked[:index]
                walked.append((r, c))
            pR, pC = walked[0]
            visited[pR][pC] = True
            for r, c in walked[1:]:
                self[pR, pC].connect(self[r, c])
                visited[r][c] = True
                if (r, c) in unvisited:
                    unvisited.remove((r, c))
                pR, pC = r, c

    def __getitem__(self, item):
        if isinstance(item, tuple):
            r, c = item
            return self.grid[r][c]
        return self.grid[item]

    def __setitem__(self, item, value):
        if isinstance(item, tuple):
            r, c = item
            self.grid[r][c] = value
        else:
            raise ValueError("Cannot set item on a row")

    def __repr__(self):
        text = ""
        for i in self.grid:
            text += str(i) + "\n"
        return text.strip()

    def __iter__(self):
        for i in self.grid:
            for j in i:
                yield j


class Room:
    def __init__(self, grid, r, c):
        self.grid = grid
        self.r = r
        self.c = c
        self.N = self.E = self.S = self.W = None

    @property
    def neighbors(self):
        return [self.N, self.E, self.S, self.W]

    def connect(self, other, bidirectional=True, *, disconnect=False):
        r, c = other.r, other.c
        diff = (self.r - r, self.c - c)
        if diff == (1, 0):
            self.N = None if disconnect else other
        elif diff == (0, -1):
            self.E = None if disconnect else other
        elif diff == (-1, 0):
            self.S = None if disconnect else other
        elif diff == (0, 1):
            self.W = None if disconnect else other
        else:
            raise ValueError("Rooms not adjacent")
        if bidirectional:
            other.connect(self, False)

    # def __repr__(self):
    #     return f"(n={'o' if self.N else 'x'} e={'o' if self.E else 'x'} " \
    #            f"s={'o' if self.S else 'x'} w={'o' if self.W else 'x'})"
    def __repr__(self):
        return f"Room({self.r}, {self.c})"
    def draw(self, canvas):
        pass


class Tile:
    pass


def main():
    grid = Grid(6, 10)
    print(grid.rooms)

from Rooms import DungeonRoom

if __name__ == '__main__':
    main()
