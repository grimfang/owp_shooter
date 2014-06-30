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
        self.health = 100.0
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
        self.isAutoActive = False
        self.trigger = False
        self.lastShot = 0.0
        self.fireRate = 0.0

        self.playerTraverser = CollisionTraverser()
        self.playerEH = CollisionHandlerEvent()
        ## INTO PATTERNS
        self.playerEH.addInPattern('intoPlayer-%in')
        #self.playerEH.addInPattern('colIn-%fn')
        self.playerEH.addInPattern('intoHeal-%in')
        self.playerEH.addInPattern('intoWeapon-%in')
        ## OUT PATTERNS
        self.playerEH.addOutPattern('outOfPlayer-%in')
        playerCNode = CollisionNode('playerSphere')
        playerCNode.setFromCollideMask(BitMask32.bit(1))
        self.playerSphere = CollisionSphere(0, 0, 0, 0.6)
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
        self.accept("mouse1", self.setWeaponTrigger, [True])
        self.accept("mouse1-up", self.setWeaponTrigger, [False])

        # Killed enemies
        self.accept("killEnemy", self.addPoints)

        # Game states
        self.accept("doDamageToPlayer", self.doDamage)

    def ignoreKeys(self):
        self.ignore("w")
        self.ignore("a")
        self.ignore("s")
        self.ignore("d")
        self.ignore("killEnemy")
        self.ignore("mouse1")
        self.ignore("mouse1-up")

        for item in self.main.itemList:
            if item.type == "heal":
                self.ignore("intoHeal-" + "itemHeal" + str(item.id))
            elif item.type == "gun":
                self. ignore("intoWeapon-" + "itemWeapon" + str(item.id))

        for enemy in self.main.enemyList:
            self.ignore("intoPlayer-" + "colEnemy" + str(enemy.id))

        # Add mouse btn for fire to ignore

    def setKey(self, action, pressed):
        self.keyMap[action] = pressed

    def start(self, startPos, playerName):
        self.name = playerName
        self.points = 0
        self.health = 100
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
        #self.playerTraverser.traverse(self.main.enemyParent)
        #self.playerTraverser.traverse(self.main.itemParent)

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
        self.fireRate = self.activeWeapon.fireRate

    def setWeaponTrigger(self, _state):
        self.trigger = _state

        if _state:
            mpos = self.main.mouse.getMousePos()
            self.activeWeapon.doFire(mpos)
            if self.activeWeapon.weaponType == "MG":
                self.fireActiveWeapon()
        else:
            taskMgr.remove("Fire")

    def fireActiveWeapon(self):
        if self.activeWeapon:
            #mpos = self.main.mouse.getMousePos()
            taskMgr.add(self.fireUpdate, "Fire")
            #self.activeWeapon.doFire(mpos)

    def fireUpdate(self, task):
        dt = globalClock.getDt()
        self.lastShot += dt
        mpos = self.main.mouse.getMousePos()
        #print self.lastShot
        if self.lastShot >= self.fireRate:
            self.lastShot -= self.fireRate

            if self.trigger:
                self.activeWeapon.doFire(mpos)
                #task.delayTime += self.fireRate
        return task.again

    def setMouseBtn(self):
        self.trigger = False

        print "Mouse Released"

    def addEnemyDmgEvent(self, _id):
        self.accept("intoPlayer-" + "colEnemy" + str(_id), self.setEnemyAttack)
        #self.accept("outOfPlayer-" + "colEnemy" + str(_id), self.setEnemyAttackOutOfRange)

    def setEnemyAttack(self, _entry):
        enemyColName = _entry.getIntoNodePath().node().getName()
        base.messenger.send("inRange-" + enemyColName, [True])
    def setEnemyAttackOutOfRange(self, _entry):
        enemyColName = _entry.getIntoNodePath().node().getName()
        base.messenger.send("inRange-" + enemyColName)

    def doDamage(self, _dmg):

        if self.health == 0:
            #print "KILLED IN ACTION"
            self.main.stop()
        else:
            self.health -= _dmg
            print "Remaining Health: ", self.health
        base.messenger.send("setHealth", [self.health])

    def addHealItemEvent(self, _id):
        self.accept("intoHeal-" + "itemHeal" + str(_id), self.healPlayer)

    def healPlayer(self, _entry):
        itemColName = _entry.getIntoNodePath().node().getName()

        if self.health == 100:
            pass

        else:
            self.health += 50
            base.messenger.send("into-" + itemColName)
            if self.health > 100:
                self.health = 100

        print self.health

    def addWeaponItemEvent(self, _id):
        self.accept("intoWeapon-" + "itemWeapon" + str(_id), self.changeWeapon)

    def changeWeapon(self, _entry):
        itemColName = _entry.getIntoNodePath().node().getName()
        base.messenger.send("into-" + itemColName)
