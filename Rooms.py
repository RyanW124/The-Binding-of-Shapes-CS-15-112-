import Generation
import random
import Obstacles
import Characters
from Shapes import Rect

class DungeonRoom(Generation.Room):
    ROWS, COLUMNS = 7, 13
    SIZE = 75
    MARGIN = 10
    WIDTH = 995
    HEIGHT = 545
    objectMap = {
        0: None,
        1: Obstacles.Rock,
        2: Characters.Fly
    }

    def __init__(self, room, player):
        super().__init__(room.grid, room.r, room.c)
        self.N, self.E, self.S, self.W = room.neighbors
        self.map = []
        self.obstacles = []
        self.player = player
        self.visited = False
        self.monsters = []
        self.initMap()
        self.id = room.id
        self.doors = [None] * 4
        if self.N:
            self.doors[0] = Rect(self.WIDTH/2, 0, self.SIZE, self.MARGIN, anchor='n')
        if self.S:
            self.doors[2] = Rect(self.WIDTH/2, self.HEIGHT, self.SIZE, self.MARGIN, anchor='s')
        if self.E:
            self.doors[1] = Rect(self.WIDTH, self.HEIGHT/2, self.MARGIN, self.SIZE, anchor='e')
        if self.W:
            self.doors[3] = Rect(0, self.HEIGHT/2, self.MARGIN, self.SIZE, anchor='w')




        self.borders = [Rect(0, 0, self.WIDTH, self.MARGIN, anchor="nw"),
                        Rect(0, 0, self.MARGIN, self.HEIGHT, anchor="nw"),
                        Rect(self.WIDTH-self.MARGIN, 0, self.MARGIN, self.HEIGHT, anchor="nw"),
                        Rect(0, self.HEIGHT-self.MARGIN, self.WIDTH, self.MARGIN, anchor="nw")]
    def cleared(self):
        return not self.monsters
    def update(self):
        self.monsters = [i for i in self.monsters if i.health>0]
        for i in self.monsters:
            i.update()
    def initMap(self):
        chapter = "Basement" if self.grid.depth == 0 else "None"
        with open("Maps/"+chapter) as f:
            rooms = list(f)
        total = len(rooms)//(self.ROWS+1)
        chosen = random.randint(0, total)
        # 2 is rock 1 is river 0 is blank
        row = []
        for r, line in enumerate(rooms[chosen*(self.ROWS+1):chosen*(self.ROWS+1)+self.ROWS]):
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
    def draw(self, canvas):
        color = "black" if self.cleared() else "grey"

        for i in self.borders:
            i.draw(canvas, fill="grey")
        for i in self.doors:
            if i:
                i.draw(canvas, fill=color)
        for i in self.obstacles+self.monsters:
            i.draw(canvas)



if __name__ == '__main__':
    pass