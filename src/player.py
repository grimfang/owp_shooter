from direct.showbase.DirectObject import DirectObject
from hud import Hud

import math

class Player(DirectObject):
    def __init__(self, _main):
        self.main = _main
        self.name = ""
        self.points = 0
        self.runSpeed = 1.8
        self.keyMap = {
            "left":False,
            "right":False,
            "up":False,
            "down":False
            }
        base.camera.setPos(0,0,0)
        self.model = loader.loadModel("Player")
        #self.model.setP(-90)
        base.camera.setP(-90)
        #base.camera.setP(90)
        #base.camera.reparentTo(self.model)
        self.playerHud = Hud()
        self.playerHud.hide()
        self.model.hide()

        # Weapons: size=2, 0=main, 1=offhand
        self.mountSlot = []
        self.activeWeapon = None

    def acceptKeys(self):
        self.accept("w", self.setKey, ["up", True])
        self.accept("w-up", self.setKey, ["up", False])
        self.accept("a", self.setKey, ["left", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("s", self.setKey, ["down", True])
        self.accept("s-up", self.setKey, ["down", False])
        self.accept("d", self.setKey, ["right", True])
        self.accept("d-up", self.setKey, ["right", False])

        # Add mouse btn for fire()
        self.accept("mouse1", self.fireActiveWeapon)

        # Killed enemies
        self.accept("killEnemy", self.addPoints)

    def ignoreKeys(self):
        self.ignore("w")
        self.ignore("a")
        self.ignore("s")
        self.ignore("d")
        self.ignore("killEnemy")
        self.ignore("mouse1")

        # Add mouse btn for fire to ignore

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
        print "stopped"
        taskMgr.remove("moveTask")
        self.ignoreKeys()
        self.playerHud.hide()
        self.model.hide()

    def addPoints(self, args):
        print "add points"
        self.points += 10

    def move(self, task):
        elapsed = globalClock.getDt()

        # set headding
        pos = self.main.mouse.getMousePos()
        pos.setZ(0)
        self.model.lookAt(pos)
        self.model.setP(-90)

        # new player position
        if self.keyMap["up"]:
            # follow mouse mode
            #self.model.setZ(self.model, 5 * elapsed * self.runSpeed)
            # axis move mode
            self.model.setY(self.model.getY() + elapsed * self.runSpeed)
        elif self.keyMap["down"]:
            #self.model.setZ(self.model, -5 * elapsed * self.runSpeed)
            self.model.setY(self.model.getY() - elapsed * self.runSpeed)

        if self.keyMap["left"]:
            # follow mouse mode
            #self.model.setX(self.model, -5 * elapsed * self.runSpeed)
            # axis move mode
            self.model.setX(self.model.getX() - elapsed * self.runSpeed)
        elif self.keyMap["right"]:
            #self.model.setX(self.model, 5 * elapsed * self.runSpeed)
            self.model.setX(self.model.getX() + elapsed * self.runSpeed)

        # actualize cam position
        base.camera.setPos(self.model.getPos())
        base.camera.setZ(20)
        return task.cont

    def mountWeapon(self, _weaponToMount):
        self.activeWeapon = _weaponToMount # self.mountSlot[0]

    def fireActiveWeapon(self):
        if self.activeWeapon:
            mpos = self.main.mouse.getMousePos()
            self.activeWeapon.doFire(mpos)

