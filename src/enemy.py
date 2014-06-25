class Enemy():
    def __init__(self):
        self.id = id(self)
        self.model = loader.loadModel("Enemy")
        self.model.setP(-90)
        self.model.hide()


    def start(self, startPos):
        self.model.show()
        self.model.reparentTo(render)
        self.model.setPos(startPos.x,
                          startPos.y,
                          0)
        taskMgr.add(self.move, "moveTask")

    def stop(self):
        taskMgr.remove("moveTask")
        self.model.remove_node()

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


