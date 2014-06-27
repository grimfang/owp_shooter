from panda3d.core import CollisionSphere, CollisionNode
class Heal():
    def __init__(self, _main):
        self.main = _main
        self.id = id(self)
        self.type = "heal"
        self.model = loader.loadModel("ItemHeal")
        cs = CollisionSphere(0, 0, 0, 1)
        cnode = CollisionNode('itemHeal' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)

    def start(self, pos):
        self.model.reparentTo(render)
        self.model.setPos(pos.x, pos.y, 0.0)
        self.model.setP(-90)

    def stop(self):
        self.model.remove_node()

class MachineGun():
    def __init__(self, _main):
        self.main = _main
        self.type = "gun"
        self.id = id(self)
        self.model = loader.loadModel("ItemMG")
        cs = CollisionSphere(0, 0, 0, 1)
        cnode = CollisionNode('itemMG' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)

    def start(self, pos):
        self.model.reparentTo(render)
        self.model.setPos(pos.x, pos.y, 0.0)
        self.model.setP(-90)

    def stop(self):
        self.model.remove_node()

