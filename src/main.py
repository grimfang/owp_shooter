#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title GrimFang OWP - Shooter
    cursor-hidden 0
    show-frame-rate-meter 1
    model-path $MAIN_DIR/assets/
"""
)

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

from panda3d.core import Vec4

from player import Player
from enemy import Enemy
from level import Level
from items import Heal, Weapon
import random

class Main(ShowBase, DirectObject):
    def __init__(self):
        ShowBase.__init__(self)
        self.win.setClearColor(Vec4(0.12,0.43,0.18,1))
        self.disableMouse()
        self.player = Player()
        self.enemyList = []
        self.maxEnemyCount = 15
        self.itemList = []
        self.maxItemCount = 4
        self.level = Level()
        random.seed()

        self.accept("escape", self.stop)

    def start(self):
        #TODO: start the main loop for spawning enemies and items...
        self.level.start()
        self.player.start(self.level.startPos)
        self.taskMgr.add(self.world, "MAIN TASK")

    def stop(self):
        self.player.stop()
        self.level.stop()
        if self.appRunner:
            self.appRunner.stop()
        else:
            exit(0)

    def spawnEnemy(self):
        if len(self.enemyList) > self.maxEnemyCount: return False
        enemy = Enemy()
        #TODO: set enemy position, ID and other necessary things
        self.enemyList.append(enemy)
        return True

    def removeEnemy(self, enemyID):
        for enemy in self.enemyList:
            if enemy.id == enemyID:
                # TODO: Check if that really works
                self.enemyList.remove(enemy)
                return True
        return False

    def spawnItem(self):
        if len(self.itemList) > self.maxItemCount: return False
        item = random.choice([Heal(), Weapon()])
        #TODO: set item position, ID and other necessary things
        self.itemList.append(item)
        return True

    def world(self, task):
        """MAIN TASK"""
        return task.cont

APP = Main()
APP.start()
APP.run()
