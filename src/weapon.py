from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, CollisionSegment
from panda3d.core import BitMask32, CollisionTraverser, CollisionHandlerQueue
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
        # Make weapon ray
        self.setupRay()

    def setupModel(self):
        pass

    def setAmmo(self):
        pass

    def setupRay(self):
        self.picker = CollisionTraverser()
        # Setup mouse ray
        self.pq = CollisionHandlerQueue()
        # Create a collision Node
        pickerNode = CollisionNode('WeaponRay')
        # set the nodes collision bitmask
        pickerNode.setFromCollideMask(BitMask32.bit(1))#GeomNode.getDefaultCollideMask())
        # create a collision ray
        self.pickerRay = CollisionSegment()
        # add the ray as a solid to the picker node
        pickerNode.addSolid(self.pickerRay)
        # create a nodepath with the camera to the picker node
        self.pickerNP = self.main.player.model.attachNewNode(pickerNode)
        # add the nodepath to the base traverser
        self.picker.addCollider(self.pickerNP, self.pq)

        #self.wepRay.setOrigin(self.player.model.getPos())
        #self.wepRay.setDirection(0, 1, 0)

    def doFire(self, _toPos=(0, 0, 0)):
        print "Weapon - Fire!!"
        self.isFiring = True

        # No idea how the fk this works...
        self.pickerRay.setPointA(self.main.player.model.getPos())
        self.pickerRay.setPointB(_toPos) # _toPos Should be the mouse clicked pos


    def stopFire(self):
        pass

    def reload(self):
        pass