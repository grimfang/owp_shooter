from panda3d.core import CollisionSphere, CollisionNode
from direct.showbase.DirectObject import DirectObject

from panda3d.ai import AICharacter

class Enemy(DirectObject):
    def __init__(self, _main):
        self.main = _main
        self.id = id(self)
        self.model = loader.loadModel("Enemy")
        self.model.setP(-90)
        self.model.setH(180)
        self.model.hide()
        cs = CollisionSphere(0, 0, 0, 0.5)
        cnode = CollisionNode('colEnemy' + str(self.id))
        cnode.addSolid(cs)
        self.colNP = self.model.attachNewNode(cnode)
        #self.colNP.show()

        # Game state
        self.health = 100.0
        self.damageDone = 5

    def start(self, startPos, enemyParent):
        self.model.show()
        self.model.reparentTo(enemyParent)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.accept("into-" + "colEnemy" + str(self.id), self.hit)

    def stop(self):
        self.model.remove_node()
        self.ignore("into-" + "colEnemy" + str(self.id))

    def hit(self, _dmg):
        if self.health == 0:
            base.messenger.send("killEnemy", [self.id])
        else:
            self.health -= _dmg

    def makeAi(self):
        # Make some ai character for each
        self.aiChar = AICharacter("Enemy" + str(self.id), self.model, -15, 0.05, 0.5)
        self.main.AiWorld.addAiChar(self.aiChar)
        self.AIbehaviors = self.aiChar.getAiBehaviors()

        self.AIbehaviors.pursue(self.main.player.model)
        return self.aiChar
