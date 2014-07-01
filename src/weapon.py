from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionNode, CollisionSegment
from panda3d.core import BitMask32, CollisionTraverser, CollisionHandlerQueue
from direct.interval.IntervalGlobal import ProjectileInterval, LerpPosInterval

class Weapon(DirectObject):
    def __init__(self, _main, _name, _fireRate, _dmg=20,_mountSlot=0, weaponType="Pistol"):
        self.main = _main
        self.name = _name
        self.fireRate = _fireRate
        self.dmg = _dmg
        self.weaponType = weaponType
        self.mountSlot = _mountSlot

        self.muzzleFlash = loader.loadModel("muzzleflash")
        if weaponType == "Pistol":
            self.style = "OneHand"
            self.model = loader.loadModel("Pistol")
            self.muzzleFlash.setZ(0.65)
            self.muzzleFlash.setX(-0.04)
            self.muzzleFlash.setScale(0.25)
            self.muzzleFlash.find('**/+SequenceNode').node().setFrameRate(20)
        else:
            self.style = "TwoHand"
            self.model = loader.loadModel("MG")
            self.muzzleFlash.setZ(0.65)
            self.muzzleFlash.setX(0.08)
            self.muzzleFlash.setScale(0.3)
            self.muzzleFlash.find('**/+SequenceNode').node().setFrameRate(20)
        self.model.setY(2)
        self.muzzleFlash.reparentTo(self.model)
        self.muzzleFlash.find('**/+SequenceNode').node().stop()
        self.muzzleFlash.hide()

        # Load bullet model
        self.bullet = loader.loadModel("Bullet")
        self.bullet.setP(-90)
        self.bullet.setH(180)
        #self.bullet.setPos(0, 0.5, 0)

        # Control
        self.isFiring = False

        # Collision Stuff
        self.wepRay = None
        # Make weapon ray
        self.setupRay()
        self.model.show()

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

        if self.weaponType == "Pistol":
            self.muzzleFlash.find('**/+SequenceNode').node().play(0, 1)
        else:
            self.muzzleFlash.find('**/+SequenceNode').node().loop(True)
        self.muzzleFlash.show()

        # For some reason the mouse ray end up at posZ -1 (which causes a problem when we make the enemy spheres smaller in radius)
        # so here for now.. ill make a quick fix.
        adjustedZ = (_toPos[0], _toPos[1], 0)

        self.shootRay.setPointA(self.main.player.model.getPos())
        self.shootRay.setPointB(adjustedZ)

        fromPos = self.main.player.model.getPos() #self.model.getPos()
        #self.setProjectile(fromPos, adjustedZ)#_toPos)

        self.shootTraverser.traverse(self.main.enemyParent)
        if self.shootingQH.getNumEntries() > 0:
            self.shootingQH.sortEntries()
            enemyCol = self.shootingQH.getEntry(0).getIntoNodePath().node().getName()
            base.messenger.send("into-" + enemyCol, [self.dmg])

    def stopFire(self):
        if self.weaponType == "Pistol" and \
               self.muzzleFlash.find('**/+SequenceNode').node().isPlaying():
            taskMgr.add(self.waitForFrame, "waitForFrame")
            return
        self.muzzleFlash.find('**/+SequenceNode').node().stop()
        self.muzzleFlash.hide()

    def waitForFrame(self, task):
        if self.muzzleFlash.find('**/+SequenceNode').node().isPlaying():
            return task.cont
        self.muzzleFlash.find('**/+SequenceNode').node().stop()
        self.muzzleFlash.hide()

    def reload(self):
        pass

    def setProjectile(self, _from, _to):
        self.bullet.reparentTo(render)#self.model)
        # setup the projectile interval
        #self.bulletProjectile = ProjectileInterval(self.bullet,
        #                                startPos = Point3(_from),
        #                                duration = 1,
        #                                endPos = Point3(_to))
        #self.bulletProjectile = self.bullet.posInterval(1.0, Point3(_to), startPos=Point3(_from))
        #self.bulletProjectile = LerpPosInterval(self.bullet, 2.0, _to, _from)
        print "POSITIONS:"
        print _to
        print _from
        frm = render.getPos(self.main.player.model)
        print frm

        self.bulletProjectile = LerpPosInterval(self.bullet, 1.0, _to, _from)
        self.bulletProjectile.start()



