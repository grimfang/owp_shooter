from panda3d.core import VBase2, CollisionPlane, Vec3, Point3, Plane, CollisionNode
from panda3d.core import BitMask32

class Level():
    def __init__(self):
        self.startPos = VBase2(0,0)
        self.levelfile = "level2"
        self.model = loader.loadModel(self.levelfile)
        self.model.setPos(0,0,-1)
        self.model.setScale(2)
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        planeUp = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, -7.5, 0)))
        planeDown = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 7.5, 0)))
        planeLeft = CollisionPlane(Plane(Vec3(-1, 0, 0), Point3(7.5, 0, 0)))
        planeRight = CollisionPlane(Plane(Vec3(1, 0, 0), Point3(-7.5, 0, 0)))
        cnode = CollisionNode('cnode')
        cnode.setIntoCollideMask(BitMask32.bit(1))
        cnode.setFromCollideMask(BitMask32.bit(1))
        cnode.addSolid(plane)
        cnode.addSolid(planeUp)
        cnode.addSolid(planeDown)
        cnode.addSolid(planeLeft)
        cnode.addSolid(planeRight)
        self.planeNP = self.model.attachNewNode(cnode)
        #self.planeNP.show()

        self.model.reparentTo(render)
        self.model.hide()

    def start(self):
        self.model.show()

    def stop(self):
        self.model.hide()

