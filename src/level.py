from panda3d.core import VBase2
class Level():
    def __init__(self):
        self.startPos = VBase2(0,0)
        self.levelfile = "level.egg"

    def start(self):
        self.model = loader.loadModel(self.levelfile)
        self.model.setPos(0,0,-1)
        self.model.reparentTo(render)

    def stop(self):
        self.model.remove()

