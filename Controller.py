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
        Key("Up", "Up")
        Key("Down", "Down")
        Key("Left", "Left")
        Key("Right", "Right")
        Key("Shoot", "Space")



def keyPressed(app, event):
    # print(event.key, Key.buttonToKey)
    if event.key in Key.buttonToKey:
        Key.getKeyFromButton(event.key).press()

def keyReleased(app, event):
    if event.key in Key.buttonToKey:
        Key.getKeyFromButton(event.key).release()


def mousePressed(app, event):
    pass

def main():
    Key.init()
    Key.getKeyFromButton("Up").setButton("Space")
    print(Key.buttonToKey)


if __name__ == '__main__':
    main()