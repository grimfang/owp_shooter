from direct.showbase.DirectObject import DirectObject
from hud import Hud

class Weapon(DirectObject):
    def __init__(self):
        self.name = ""

    def acceptKeys(self):
        self.accept("w", self.setKey, ["up", True])
        self.accept("w-up", self.setKey, ["up", False])

    def ignoreKeys(self):
        self.ignore("w")

    def setKey(self, action, pressed):
        self.keyMap[action] = pressed

    def start(self, startPos, playerName):
        self.name = playerName
        self.points = 0
        self.model.show()
        self.model.reparentTo(render)
        taskMgr.add(self.move, "moveTask")
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.acceptKeys()
        self.playerHud.show()

    def stop(self):
        taskMgr.remove("moveTask")
        self.ignoreKeys()
        self.playerHud.hide()
        self.model.hide()

    def move(self, task):
        elapsed = globalClock.getDt()
        return task.cont