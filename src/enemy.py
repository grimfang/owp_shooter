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
        self.damageDone = 0.1
        self.lastShot = 0.0
        self.attackRate = 2.0

    def start(self, startPos, enemyParent):
        self.model.show()
        self.model.reparentTo(enemyParent)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.accept("into-" + "colEnemy" + str(self.id), self.hit)
        self.accept("inRange-" + "colEnemy" + str(self.id), self.startAttack)

    def stop(self):
        self.model.remove_node()
        self.ignore("into-" + "colEnemy" + str(self.id))
        self.ignore("inRange-" + "colEnemy" + str(self.id))

    def hit(self, _dmg):
        if self.health == 0:
            base.messenger.send("killEnemy", [self.id])
        else:
            self.health -= _dmg

    def makeAi(self):
        # Make some ai character for each
        self.aiChar = AICharacter("Enemy" + str(self.id), self.model, -100, 0.05, 5)
        self.main.AiWorld.addAiChar(self.aiChar)
        self.AIbehaviors = self.aiChar.getAiBehaviors()

        self.AIbehaviors.pursue(self.main.player.model)
        return self.aiChar

    def startAttack(self, _inRange=False):

        if _inRange:
            self.isAttacking = True
            taskMgr.add(self.attack, "StartAttack")
        else:
            taskMgr.remove("StartAttack")

    def attack(self, task):
        dt = globalClock.getDt()
        self.lastShot += dt
        if self.lastShot >= self.attackRate:
            self.lastShot -= self.attackRate
            base.messenger.send("doDamageToPlayer", [self.damageDone])
        return task.again
