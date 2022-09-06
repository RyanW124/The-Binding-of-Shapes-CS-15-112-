from Shapes import Rect

class Key:
    buttonToKey = {}
    nameToKey = {}
    def __init__(self, name, button):
        self.name = name
        self.button = None
        self.setButton(button)
        Key.nameToKey[self.name] = self
        self._pressed = False
        self.history = [False] * 2
    @property
    def pressed(self):
        return self._pressed or (True in self.history)
    def press(self):
        self._pressed = True
        self.history.append(True)
        self.history.pop(0)
    def release(self):
        self._pressed = False
        self.history.append(True)
        self.history.pop(0)
    def setButton(self, value):
        if self.button is not None:
            del Key.buttonToKey[self.button]
        self.button = value
        Key.buttonToKey[self.button] = self
    def __eq__(self, other):
        return self.name == other
    def __bool__(self):
        return self.pressed
    def __repr__(self):
        return f"Key({self.name}: {self.button})"
    @classmethod
    def update(cls):
        for i in cls.nameToKey.values():
            i.history.append(False)
            i.history.pop(0)

    @classmethod
    def getKey(cls, name):
        return cls.nameToKey[name]
    @classmethod
    def getKeyFromButton(cls, button):
        return cls.buttonToKey[button]
    @classmethod
    def init(cls):
        cls.buttonToKey = {}
        cls.nameToKey = {}
        Key("Up", "Up")
        Key("Down", "Down")
        Key("Left", "Left")
        Key("Right", "Right")
        Key("Shoot", "Enter")

def game_keyPressed(app, event):
    if event.key in Key.buttonToKey:
        Key.getKeyFromButton(event.key).press()



    if event.key == "Escape":
        app.setMode(app, 'pause')

def pause_keyPressed(app, event):
    if event.key == "Escape":
        app.resume(app)

def game_keyReleased(app, event):
    if event.key in Key.buttonToKey:
        Key.getKeyFromButton(event.key).release()

def help_keyPressed(app, event):
    if event.key == 'Left':
        app.changePage(app, -1)
    elif event.key == 'Right':
        app.changePage(app)
    elif event.key == 'Escape':
        app.setMode(app, 'menu')

class MyButton(Rect):
    mode = 'game'
    buttons = {}
    def __init__(self, x, y, w, h, name, inmode, color, textcolor, action, *args, anchor="c"):
        super().__init__(x, y, w, h, anchor=anchor)
        self.name = name
        self.inmode = inmode
        self.action = action
        self.args = args
        if inmode not in self.buttons:
            self.buttons[inmode] = []
        self.buttons[inmode].append(self)
        self.color = color
        self.textcolor = textcolor

    def check(self, x, y):
        if self.collide(x, y):
            self.action(*self.args)


    def draw(self, canvas, *args, **kwargs):
        super().draw(canvas, fill=self.color)
        canvas.create_text(self.centerX, self.centerY, text=self.name,
                               font=f"Arial {int(self.h/2)}", fill=self.textcolor)

    @classmethod
    def drawButtons(cls, canvas):
        # print(cls.mode)
        for i in cls.buttons.get(cls.mode, []):
            # print(i)
            i.draw(canvas)

    @classmethod
    def update(cls, x, y):
        for i in cls.buttons.get(cls.mode, []):
            i.check(x, y)

menu_mousePressed = lost_mousePressed = help_mousePressed = \
game_mousePressed = pause_mousePressed = lambda app, event: MyButton.update(event.x, event.y)
