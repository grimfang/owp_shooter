from direct.showbase.DirectObject import DirectObject
from hud import Hud

class Player(DirectObject):
    def __init__(self):
        self.name = ""
        self.points = 0
        self.runSpeed = 1.8
        self.keyMap = {
            "left":False,
            "right":False,
            "up":False,
            "down":False
            }
        base.camera.setPos(0,-20,0)
        self.model = loader.loadModel("Player")
        self.model.setP(-90)
        base.camera.reparentTo(self.model)
        self.playerHud = Hud()
        self.playerHud.hide()
        self.model.hide()

    def acceptKeys(self):
        self.accept("w", self.setKey, ["up", True])
        self.accept("w-up", self.setKey, ["up", False])
        self.accept("a", self.setKey, ["left", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("s", self.setKey, ["down", True])
        self.accept("s-up", self.setKey, ["down", False])
        self.accept("d", self.setKey, ["right", True])
        self.accept("d-up", self.setKey, ["right", False])

    def ignoreKeys(self):
        self.ignore("w")
        self.ignore("a")
        self.ignore("s")
        self.ignore("d")

    def setKey(self, action, pressed):
        self.keyMap[action] = pressed

    def start(self, startPos, playerName):
        self.name = playerName
        self.points = 0
        self.model.show()
        self.model.reparentTo(render)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.acceptKeys()
        self.playerHud.show()
        taskMgr.add(self.move, "moveTask")

    def stop(self):
        taskMgr.remove("moveTask")
        self.ignoreKeys()
        self.playerHud.hide()
        self.model.hide()

    def move(self, task):
        elapsed = globalClock.getDt()
        if self.keyMap["up"]:
            self.model.setY(self.model.getY() + elapsed * self.runSpeed)
        elif self.keyMap["down"]:
            self.model.setY(self.model.getY() - elapsed * self.runSpeed)

        if self.keyMap["left"]:
            self.model.setX(self.model.getX() - elapsed * self.runSpeed)
        elif self.keyMap["right"]:
            self.model.setX(self.model.getX() + elapsed * self.runSpeed)
        return task.cont
