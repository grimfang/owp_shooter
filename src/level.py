from panda3d.core import VBase2, CollisionPlane, Vec3, Point3, Plane
class Level():
    def __init__(self):
        self.startPos = VBase2(0,0)
        self.levelfile = "level.egg"

    def start(self):
        self.model = loader.loadModel(self.levelfile)
        self.model.setPos(0,0,-1)
        self.model.reparentTo(render)
        self.plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))

    def stop(self):
        self.model.remove()

