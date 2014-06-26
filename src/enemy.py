from panda3d.core import CollisionSphere, CollisionNode
from direct.showbase.DirectObject import DirectObject

class Enemy(DirectObject):
    def __init__(self):
        self.id = id(self)
        self.model = loader.loadModel("Enemy")
        self.model.setP(-25)
        self.model.hide()
        cs = CollisionSphere(0, 0, 0, 1)
        cnode = CollisionNode('colEnemy' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)
        self.colNP.show()

    def start(self, startPos):
        self.model.show()
        self.model.reparentTo(render)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.accept("into-" + "colEnemy" + str(self.id), self.hit)
        taskMgr.add(self.move, "enemyMoveTask"+str(self.id))

    def stop(self):
        taskMgr.remove("enemyMoveTask"+str(self.id))
        self.model.remove_node()
        self.ignore("into-" + "colEnemy" + str(self.id))

    def hit(self, arg):
        #print "hitArg:", arg
        print "I'm hit", self.id
        base.messenger.send("killEnemy", [self.id])

    def move(self, task):
        elapsed = globalClock.getDt()
        #if self.keyMap["up"]:
        #    self.model.setY(self.model.getY() + elapsed)
        #elif self.keyMap["down"]:
        #    self.model.setY(self.model.getY() - elapsed)

        #if self.keyMap["left"]:
        #    self.model.setX(self.model.getX() - elapsed)
        #elif self.keyMap["right"]:
        #    self.model.setX(self.model.getX() + elapsed)
        return task.cont


