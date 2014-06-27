from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import BitMask32, CollisionTraverser, CollisionHandlerEvent
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
        self.model.find('**/+SequenceNode').node().stop()
        self.model.find('**/+SequenceNode').node().pose(0)
        base.camera.setP(-90)
        self.playerHud = Hud()
        self.playerHud.hide()
        self.model.hide()

        # Weapons: size=2, 0=main, 1=offhand
        self.mountSlot = []
        self.activeWeapon = None

        self.playerTraverser = CollisionTraverser()
        self.playerEH = CollisionHandlerEvent()
        self.playerEH.addInPattern('into-%in')
        self.playerEH.addInPattern('colIn-%fn')
        self.playerEH.addInPattern('bot-%(enemy)fh')
        self.playerEH.addInPattern('heal-%in')
        playerCNode = CollisionNode('playerSphere')
        playerCNode.setFromCollideMask(BitMask32.bit(1))
        self.playerSphere = CollisionSphere(0, 0, 0, 1)
        playerCNode.addSolid(self.playerSphere)
        self.playerNP = self.model.attachNewNode(playerCNode)
        self.playerTraverser.addCollider(self.playerNP, self.playerEH)
        #self.playerNP.show()

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

    def addPoints(self, args):
        self.points += 10
        base.messenger.send("setHighscore", [self.points])

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
        if self.activeWeapon.style == "TwoHand":
            self.model.find('**/+SequenceNode').node().pose(0)
        else:
            self.model.find('**/+SequenceNode').node().pose(1)
        self.activeWeapon.model.reparentTo(self.model)
        self.activeWeapon.model.setY(self.model.getY() - 0.1)
        self.model.show()

    def fireActiveWeapon(self):
        if self.activeWeapon:
            mpos = self.main.mouse.getMousePos()
            self.activeWeapon.doFire(mpos)

    def addEnemyDmgEvent(self, _id):
        self.accept("bot-" + "colEnemy" + str(_id), self.doDamage)

    def doDamage(self):
        print "We have lift off!!"

    def addHealItemEvent(self, _id):
        self.accept("into-" + "itemHeal" + str(_id), self.healPlayer)

    def healPlayer(self):
        print "WE ARE HEALED NOW!!"

