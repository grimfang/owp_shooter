from panda3d.core import CollisionSphere, CollisionNode
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar

from panda3d.ai import AICharacter

class Enemy(DirectObject):
    def __init__(self, _main):
        self.main = _main
        self.strenght = self.main.enemyStrength
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
        self.health = 100 + (100 * self.strenght)
        self.damageDone = 0.1 + (0.1 * self.strenght)
        self.lastShot = 0.0
        self.attackRate = 10.0


        self.statusHealth = DirectWaitBar(
            text = "",
            value = self.health,
            range = self.health,
            frameSize = (0.12, 0.8, -0.12, 0.0),
            pos = (-0.5, 0, -0.5),
            barColor = (1, 0, 0, 1))
        self.statusHealth.reparentTo(self.model)
        self.statusHealth.setDepthWrite(False)
        self.statusHealth.setBin('fixed', 0)
        self.statusHealth.setBillboardAxis()

    def start(self, startPos, enemyParent):
        self.model.show()
        self.model.reparentTo(enemyParent)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        self.accept("into-" + "colEnemy" + str(self.id), self.hit)
        self.accept("inRange-" + "colEnemy" + str(self.id), self.startAttack)
        self.statusHealth.update(self.health)

    def stop(self):
        self.model.remove_node()
        self.ignore("into-" + "colEnemy" + str(self.id))
        self.ignore("inRange-" + "colEnemy" + str(self.id))

    def hit(self, _dmg):
        if self.health == 0:
            base.messenger.send("killEnemy", [self.id])
        else:
            self.health -= _dmg
            self.statusHealth.update(self.health)

    def makeAi(self):
        # Make some ai character for each
        self.aiChar = AICharacter("Enemy" + str(self.id), self.model, -100, 0.05 + (0.05 * self.strenght), 6 + (1 * self.strenght))
        self.main.AiWorld.addAiChar(self.aiChar)
        self.AIbehaviors = self.aiChar.getAiBehaviors()

        self.AIbehaviors.pursue(self.main.player.model)
        return self.aiChar

    def startAttack(self, _inRange=False):

        if _inRange:
            self.isAttacking = True
            self.simpleAttack()
            #taskMgr.remove("StartAttack")
        #elif _inRange:
        #    pass
        #    taskMgr.add(self.attack, "StartAttack")

    def attack(self, task):
        dt = globalClock.getDt()
        self.lastShot += dt
        if self.lastShot >= self.attackRate:
            self.lastShot -= self.attackRate
            base.messenger.send("doDamageToPlayer", [self.damageDone])
        return task.again

    def simpleAttack(self):
        base.messenger.send("doDamageToPlayer", [self.damageDone])
