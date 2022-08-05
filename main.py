from cmu_112_graphics import *
import Generation
from Controller import Key, keyPressed, keyReleased, mousePressed, Button
from Util import *
import random

def appStarted(app):
    Key.init()
    app.timerDelay = 20
    setMode(app, GAME)
    reset(app)

def setMode(app, mode):
    app.mode = mode
    Button.mode = mode

def initLost(app):
    Button(TOTALWIDTH/2, HEIGHT/2, 300, 100, "Play Again", LOST, 'black', 'white', reset, app)
"""transition to lost if dead"""

def reset(app):
    app.grid = Generation.Grid(app)
    setMode(GAME)
def timerFired(app):
    Key.update()
    if app.mode == GAME:
        app.grid.player.update()
        app.grid.currentRoom.update()
    elif app.mode == LOST:
        pass


def redrawAll(app, canvas):
    if app.mode == GAME:
        app.grid.draw(canvas)
        app.grid.player.draw(canvas)
    elif app.mode == LOST:
        pass

def main():
    runApp(width=WIDTH+UIBAR, height=HEIGHT)


if __name__ == '__main__':
    main()