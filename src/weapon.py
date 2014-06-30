from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, CollisionSegment, Point3
from panda3d.core import BitMask32, CollisionTraverser, CollisionHandlerEvent, CollisionHandlerQueue
from direct.interval.IntervalGlobal import ProjectileInterval, LerpPosInterval

class Weapon(DirectObject):
    def __init__(self, _main, _name, _fireRate, _dmg=20,_mountSlot=0, weaponType="Pistol"):
        self.main = _main
        self.name = _name
        self.fireRate = _fireRate
        self.dmg = _dmg
        self.weaponType = weaponType
        self.mountSlot = _mountSlot
        if weaponType == "Pistol":
            self.style = "OneHand"
            self.model = loader.loadModel("Pistol")
        else:
            self.style = "TwoHand"
            self.model = loader.loadModel("MG")

        # Load bullet model
        self.bullet = loader.loadModel("Bullet")
        self.bullet.setP(-90)
        self.bullet.setH(180)
        self.bullet.setPos(0, 0.5, 0)

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
        self.shootingQH = CollisionHandlerQueue()
        #self.shootingEH = CollisionHandlerEvent()
        #self.shootingEH.addInPattern('into-%in')
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
        #self.shootTraverser.addCollider(self.shootNP, self.shootingEH)
        self.shootTraverser.addCollider(self.shootNP, self.shootingQH)
        #self.shootNP.show()

    def doFire(self, _toPos=(0, 0, 0)):
        self.isFiring = True

        # For some reason the mouse ray end up at posZ -1 (which causes a problem when we make the enemy spheres smaller in radius)
        # so here for now.. ill make a quick fix.
        adjustedZ = (_toPos[0], _toPos[1], 0)

        self.shootRay.setPointA(self.main.player.model.getPos())
        self.shootRay.setPointB(adjustedZ)

        self.setProjectile(self.model.getPos(), adjustedZ)#_toPos)

        self.shootTraverser.traverse(self.main.enemyParent)
        if self.shootingQH.getNumEntries() > 0:
            self.shootingQH.sortEntries()
            enemyCol = self.shootingQH.getEntry(0).getIntoNodePath().node().getName()
            base.messenger.send("into-" + enemyCol, [self.dmg])

    def stopFire(self):
        pass

    def reload(self):
        pass

    def setProjectile(self, _from, _to):
        self.bullet.reparentTo(self.model)
        # setup the projectile interval
        #self.bulletProjectile = ProjectileInterval(self.bullet,
        #                                startPos = Point3(_from),
        #                                duration = 1,
        #                                endPos = Point3(_to))
        #self.bulletProjectile = self.bullet.posInterval(1.0, Point3(_to), startPos=Point3(_from))
        self.bulletProjectile = LerpPosInterval(self.bullet, 1.0, _to, _from)
        self.bulletProjectile.start()



