from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, CollisionRay
from hud import Hud

class Weapon(DirectObject):
    def __init__(self, _main, _name, _fireRate, _mountSlot=0):
        self.main = _main
        self.name = _name
        self.fireRate = _fireRate
        self.mountSlot = _mountSlot

        # Control
        self.isFiring = False

        # Collision Stuff
        self.wepRay = None

    def setupModel(self):
        pass

    def setAmmo(self):
        pass

    def setupRay(self):
        self.wepRay = CollisionNode("WeaponRay")
        self.cRay = CollisionSegment()
        self.wepRay.addSolid(self.cRay)
        self.wepRay.setFromCollideMask(BitMask32.bit(8))
        self.wepRay.setIntoCollideMask(BitMask32.allOff())

        #self.wepRay.setOrigin(self.player.model.getPos())
        #self.wepRay.setDirection(0, 1, 0)

    def doFire(self, _toPos=(0, 0, 0)):
        print "Weapon - Fire!!"
        self.isFiring = True

        # No idea how the fk this works...
        #self.wepRay.setPointA(self.main.player.model.getPos())
        #self.wepRay.setPointB(0, 0, 0) # _toPos Should be the mouse clicked pos

    def stopFire(self):
        pass

    def reload(self):
        pass