from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, CollisionSegment
from panda3d.core import BitMask32, CollisionTraverser, CollisionHandlerEvent

class Weapon(DirectObject):
    def __init__(self, _main, _name, _fireRate, _mountSlot=0, weaponType="Pistol"):
        self.main = _main
        self.name = _name
        self.fireRate = _fireRate
        self.mountSlot = _mountSlot
        if weaponType == "Pistol":
            self.style = "OneHand"
            self.model = loader.loadModel("Pistol")
        else:
            self.style = "TwoHand"
            self.model = loader.loadModel("MG")

        # Control
        self.isFiring = False

        # Collision Stuff
        self.wepRay = None
        # Make weapon ray
        self.setupRay()

    def setAmmo(self):
        pass

    def setupRay(self):
        self.shootTraverser = CollisionTraverser()
        # Setup mouse ray
        self.shootingEH = CollisionHandlerEvent()
        self.shootingEH.addInPattern('into-%in')
        # Create a collision Node
        shootNode = CollisionNode('WeaponRay')
        # set the nodes collision bitmask
        shootNode.setFromCollideMask(BitMask32.bit(1))
        # create a collision segment (ray like)
        self.shootRay = CollisionSegment()
        # add the ray as a solid to the picker node
        shootNode.addSolid(self.shootRay)
        # create a nodepath with the camera to the picker node
        #self.pickerNP = self.main.player.model.attachNewNode(pickerNode)
        self.shootNP = render.attachNewNode(shootNode)
        # add the nodepath to the base traverser
        self.shootTraverser.addCollider(self.shootNP, self.shootingEH)
        #self.shootNP.show()

    def doFire(self, _toPos=(0, 0, 0)):
        self.isFiring = True

        # No idea how the fk this works...
        self.shootRay.setPointA(self.main.player.model.getPos())
        self.shootRay.setPointB(_toPos)

        for i in self.main.enemyList:
            self.shootTraverser.traverse(i.colNP)

    def stopFire(self):
        pass

    def reload(self):
        pass



