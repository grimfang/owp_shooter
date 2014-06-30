from panda3d.core import CollisionSphere, CollisionNode
from direct.showbase.DirectObject import DirectObject
class Heal(DirectObject):
    def __init__(self, _main, _value=25):
        self.main = _main
        self.id = id(self)
        self.type = "heal"
        self.healValue = _value
        self.model = loader.loadModel("ItemHeal")
        cs = CollisionSphere(0, 0, 0, 0.5)
        cnode = CollisionNode('itemHeal' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)
        #self.colNP.show()

    def start(self, pos):
        self.model.reparentTo(self.main.itemParent)
        self.model.setPos(pos.x, pos.y, 0.0)
        self.model.setP(-90)

        # Game
        self.accept("into-" + "itemHeal" + str(self.id), self.pickup)

    def stop(self):
        self.model.remove_node()
        self.ignore("into-" + "itemHeal" + str(self.id))

    def pickup(self):
        base.messenger.send("pickedUpHealth", [self.id])

class MachineGun(DirectObject):
    def __init__(self, _main):
        self.main = _main
        self.type = "gun"
        self.id = id(self)
        self.model = loader.loadModel("ItemMG")
        cs = CollisionSphere(0, 0, 0, 0.5)
        cnode = CollisionNode('itemWeapon' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)

    def start(self, pos):
        self.model.reparentTo(self.main.itemParent)
        self.model.setPos(pos.x, pos.y, 0.0)
        self.model.setP(-90)

        # Game
        self.accept("into-" + "itemWeapon" + str(self.id), self.pickup)

    def stop(self):
        self.model.remove_node()
        self.ignore("into-" + "itemWeapon" + str(self.id))

    def pickup(self):
        base.messenger.send("pickedUpWeapon", [self.id])

