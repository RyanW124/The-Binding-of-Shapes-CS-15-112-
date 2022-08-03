from cmu_112_graphics import *
import Generation
import os
from Controller import Key, keyPressed, keyReleased, mousePressed
import Util
import random

def appStarted(app):
    Key.init()
    app.timerDelay = 20
    app.multiplier = 3.33
    app.extra = 5
    app.maximum = 20
    reset(app)
    os.system("set r off")
def appStopped(app):
    os.system("set r on")

def reset(app):
    app.depth = 0
    app.grid = Generation.Grid(app, 6, min(20, Util.roundHalfUp(app.multiplier*
                                           app.depth+
                                           random.randint(app.extra,
                                                          app.extra+1))),
                    app.depth)

# def keyPressed(app, event):
#     Key.getKey(event.key).press()
def timerFired(app):
    app.grid.player.update()
    app.grid.currentRoom.update()
    Key.update()


def redrawAll(app, canvas):
    app.grid.draw(canvas)
    app.grid.player.draw(canvas)

def main():
    runApp(width=995, height=545)


if __name__ == '__main__':
    main()