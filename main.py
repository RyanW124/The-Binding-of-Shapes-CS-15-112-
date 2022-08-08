from cmu_112_graphics import *
import Generation
from Controller import *
from Util import *

def appStarted(app):
    app.timerDelay = 20
    app.page = 0
    app.titles = ["Basics", "Monsters", "Duke of Flies"]
    setMode(app, 'menu')
    initButtons(app)
    app.setMode = setMode
    app.changePage = changePage
    app.resume = resume

def setMode(app, mode):
    app.mode = mode
    MyButton.mode = mode

def initButtons(app):
    # Lost
    MyButton(TOTALWIDTH/2, HEIGHT/2+10, 300, 50, "Play Again", "lost",
             'black', 'white', reset, app, anchor="n")
    MyButton(TOTALWIDTH/2, HEIGHT/2+70, 300, 50, "Back to Menu", "lost",
             'black', 'white', setMode, app, 'menu', anchor='n')
    # Menu
    MyButton(TOTALWIDTH / 2, HEIGHT / 2, 300, 50, "Play", "menu",
             'black', 'white', reset, app)
    MyButton(TOTALWIDTH / 2, HEIGHT / 2 + 60, 300, 50, "How to Play", "menu",
             'black', 'white', setMode, app, 'help')
    MyButton(TOTALWIDTH / 2, HEIGHT / 2 + 120, 300, 50, "Quit", "menu",
             'black', 'white', app.quit)
    # Help
    MyButton(MARGIN, MARGIN, 100, 50, "Back", "help",
             'black', 'white', setMode, app, 'menu', anchor='nw')
    MyButton(TOTALWIDTH-MARGIN, HEIGHT/2, 150, 50, "Next", "help",
             'black', 'white', changePage, app, anchor='e')

    MyButton(MARGIN, HEIGHT / 2, 150, 50, "Previous", "help",
             'black', 'white', changePage, app, -1, anchor='w')
    # Game
    MyButton(WIDTH+MARGIN, 260+3*MARGIN, UIBAR-2*MARGIN, 50, "Pause", "game",
             'black', 'white', setMode, app, "pause", anchor='nw')
    # Paused
    MyButton(TOTALWIDTH / 2, HEIGHT / 2 + 10, 300, 50, "Resume", "pause",
             'black', 'white', resume, app, anchor="n")
    MyButton(TOTALWIDTH / 2, HEIGHT / 2 + 70, 300, 50, "Back to Menu", "pause",
             'black', 'white', setMode, app, 'menu', anchor='n')
    MyButton(TOTALWIDTH / 2, HEIGHT / 2 + 130, 300, 50, "Quit", "pause",
             'black', 'white', app.quit, anchor='n')

def resume(app):
    setMode(app, 'game')
    Key.init()

def reset(app):
    Key.init()
    app.grid = Generation.Grid(app)
    setMode(app, "game")

#################################################
# Game + Lost + Pause
#################################################

def game_timerFired(app):
    Key.update()
    app.grid.player.update()
    app.grid.currentRoom.update()
    if app.grid.player.dead:
        setMode(app, "lost")


def game_redrawAll(app, canvas):
    MyButton.drawButtons(canvas)
    app.grid.draw(canvas)
    app.grid.player.draw(canvas)

def lost_redrawAll(app, canvas):
    canvas.create_text(TOTALWIDTH/2, HEIGHT/2-10, font="Arial 25", anchor="s",
                       text=f"You died on depth {app.grid.depth+1}")
    MyButton.drawButtons(canvas)

def pause_redrawAll(app, canvas):
    canvas.create_text(TOTALWIDTH / 2, HEIGHT/2-10, font="Arial 50", anchor="s",
                       text="Paused")
    MyButton.drawButtons(canvas)


#################################################
# Menu + Help
#################################################
def menu_redrawAll(app, canvas):
    canvas.create_text(TOTALWIDTH/2, HEIGHT/2-35, font="Arial 50", anchor="s",
                       text=f"The Binding of Isaac")
    MyButton.drawButtons(canvas)

def changePage(app, delta=1):
    app.page = (app.page+delta)%len(app.titles)

def help_redrawAll(app, canvas):
    canvas.create_text(TOTALWIDTH/2, 20, font="Arial 50", anchor="n",
                       text=f"How to Play: {app.titles[app.page]}")
    MyButton.drawButtons(canvas)
    x, y, fontSize = 200, 100, 25
    texts = []
    if app.page == 0:
        texts = ["Use the arrow keys to move", "Press enter to shoot in the direction you are moving",
                 "Defeat all monsters in a room to unlock doors", "Navigate to boss room and defeat the boss",
                 "Defeating the boss unlocks a trapdoor that leads to the next level"]
    elif app.page == 1:
        texts = ["Fly: flies towards you and deals contact damage (can fly over rocks)",
                 "Gaper: walk towards you and deals contact damage"]
    elif app.page == 2:
        texts = ["Floats around the room diagonally and deals contact damage",
                 "Could spawn 3 flies that orbit around itself",
                 "Could spawn a fly that attacks you",
                 "Could send orbiting flies to attack you",
                 "Releases orbiting flies upon death"]
    for i, text in enumerate(texts):
        canvas.create_text(x, i*(fontSize+10)+y, text=text, anchor='nw', font=f"Arial {fontSize}")




def main():
    runApp(width=WIDTH+UIBAR, height=HEIGHT, title="The Binding of Shapes")


if __name__ == '__main__':
    main()