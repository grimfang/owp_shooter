from panda3d.core import VBase2, CollisionPlane, Vec3, Point3, Plane, CollisionNode

class Level():
    def __init__(self):
        self.startPos = VBase2(0,0)
        self.levelfile = "level.egg"
        self.model = loader.loadModel(self.levelfile)
        self.model.setPos(0,0,-1)
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        self.planeNP = self.model.attachNewNode(CollisionNode('cnode'))
        self.planeNP.node().addSolid(plane)
        self.planeNP.show()

    def start(self):
        self.model.reparentTo(render)

    def stop(self):
        self.model.remove()

