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

from panda3d.core import VBase2
from panda3d.core import Vec4
from panda3d.core import CollisionTraverser, CollisionHandlerEvent, CollisionHandlerQueue

from player import Player
from enemy import Enemy
from level import Level
from items import Heal, Weapon
from mainScreen import MainScreen
from highscore import Highscore
from weapon import Weapon
from mouse import Mouse
import random

class Main(ShowBase, DirectObject):
    def __init__(self):
        ShowBase.__init__(self)
        self.win.setClearColor(Vec4(0.12,0.43,0.18,1))
        self.disableMouse()
        self.player = Player(self)
        self.enemyList = []
        self.maxEnemyCount = 15
        self.itemList = []
        self.maxItemCount = 4
        self.level = Level()
        self.mouse = Mouse(self.level.planeNP)
        random.seed()

        # Create Traverser and eventHandler
        cTrav = CollisionTraverser('Main Trav')
        base.cTrav = cTrav
        #self.eventHandler = CollisionHandlerQueue()#CollisionHandlerEvent()
        #elf.eventHandler.addInPattern('into-%in')
        #self.eventHandler.addOutPattern('outof-%in')

        # Setup Gui
        self.mainMenu = MainScreen()
        self.mainMenu.show()
        self.highscore = Highscore()

        # Menu events
        self.accept("escape", self.quit)
        self.accept("MainMenu_start", self.start)
        self.accept("Highscore_show", self.highscore.show)
        self.accept("MainMenu_quit", self.quit)
        self.accept("Highscore_back", self.mainMenu.show)

        # ingame events
        self.accept("killEnemy", self.removeEnemy)

    def start(self):
        self.level.start()
        self.player.start(self.level.startPos, self.mainMenu.getPlayername())
        self.taskMgr.add(self.world, "MAIN TASK")
        self.accept("escape", self.stop)

        # Create a basic weapon
        self.player.mountSlot.append(Weapon(self, "rayGun", 4))
        # Also mount the weapon on the player
        self.player.mountWeapon(self.player.mountSlot[0])

    def stop(self):
        self.level.stop()
        print "player points:", self.player.points
        self.highscore.setPoints(self.player.name, self.player.points)
        self.player.stop()
        tempIDList = []
        for enemy in self.enemyList:
            tempIDList.append(enemy.id)
        for enemyID in tempIDList:
            self.removeEnemy(enemyID)
        self.taskMgr.remove("MAIN TASK")
        self.mainMenu.show()

    def quit(self):
        if self.appRunner:
            self.appRunner.stop()
        else:
            exit(0)

    def spawnEnemy(self):
        if len(self.enemyList) > self.maxEnemyCount: return False
        enemy = Enemy()
        x = 0.0
        y = 0.0
        while (x > self.player.model.getX() - 1.0 and x < self.player.model.getX() + 1.0):
            x = random.uniform(-9, 9)
        while (y > self.player.model.getY() - 1.0 and y < self.player.model.getY() + 1.0):
            y = random.uniform(-9, 9)
        position = VBase2(x, y)

        enemy.start(position)
        self.enemyList.append(enemy)
        return True

    def removeEnemy(self, enemyID):
        for enemy in self.enemyList:
            if enemy.id == enemyID:
                enemy.stop()
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
        self.spawnEnemy()
        return task.cont

    def addToTrav(self, _object):
        pass
        #base.cTrav.addCollider(_object, self.eventHandler)

APP = Main()
APP.run()
