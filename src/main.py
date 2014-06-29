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
from panda3d.ai import *

from player import Player
from enemy import Enemy
from level import Level
from items import Heal, MachineGun
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
        self.enemyParent = render.attachNewNode("EnemyParent")
        self.itemParent = render.attachNewNode("ItemParent")
        self.mouse = Mouse(self.level.planeNP)
        random.seed()

        self.gameStarted = False

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
        self.accept("pickedUpHealth", self.removeHealItem)

    def start(self):
        self.gameStarted = True
        self.level.start()
        self.player.start(self.level.startPos, self.mainMenu.getPlayername())
        self.taskMgr.add(self.world, "MAIN TASK")
        self.accept("escape", self.stop)
        self.AiWorld = AIWorld(render)
        self.taskMgr.add(self.AIUpdate, "UPDATEAI")

        # Create a basic weapon
        self.player.mountSlot.append(Weapon(self, "rayGun", 0.25, 50,weaponType="MG"))
        # Also mount the weapon on the player
        self.player.mountWeapon(self.player.mountSlot[0])

    def stop(self):
        self.level.stop()
        self.highscore.setPoints(self.player.name, self.player.points)
        self.player.stop()
        tempIDList = []
        for enemy in self.enemyList:
            tempIDList.append(enemy.id)
        for enemyID in tempIDList:
            self.removeEnemy(enemyID)
        self.taskMgr.remove("MAIN TASK")
        self.mainMenu.show()
        self.accept("escape", self.quit)

    def quit(self):
        if self.appRunner:
            self.appRunner.stop()
        else:
            exit(0)

    def spawnEnemy(self):
        if len(self.enemyList) > self.maxEnemyCount: return False
        enemy = Enemy(self)

        x = self.player.model.getX()
        y = self.player.model.getY()
        while (x > self.player.model.getX() - 4.5 and x < self.player.model.getX() + 4.5):
            x = random.uniform(-9, 9)
        while (y > self.player.model.getY() - 4.5 and y < self.player.model.getY() + 4.5):
            y = random.uniform(-9, 9)
        position = VBase2(x, y)

        enemy.start(position, self.enemyParent)
        enemy.makeAi()
        self.player.addEnemyDmgEvent(enemy.id)
        self.enemyList.append(enemy)
        return True

    def removeEnemy(self, enemyID):
        for enemy in self.enemyList:
            if enemy.id == enemyID:
                enemy.stop()
                self.AiWorld.removeAiChar("Enemy"+str(enemyID))
                self.enemyList.remove(enemy)
                return True
        return False

    def removeHealItem(self, itemId):
        for item in self.itemList:
            if item.id == itemId:
                item.stop()
                self.itemList.remove(item)
                return True
        return False

    def spawnItem(self):
        if len(self.itemList) > self.maxItemCount: return False
        item = random.choice([Heal(self), MachineGun(self)])

        x = self.player.model.getX()
        y = self.player.model.getY()
        while (x > self.player.model.getX() - 4.5 and x < self.player.model.getX() + 4.5):
            x = random.uniform(-9, 9)
        while (y > self.player.model.getY() - 4.5 and y < self.player.model.getY() + 4.5):
            y = random.uniform(-9, 9)
        position = VBase2(x, y)

        item.start(position)
        self.itemList.append(item)

        if item.type == "heal":
            self.player.addHealItemEvent(item.id)

        return True

    def world(self, task):
        """MAIN TASK"""
        self.spawnEnemy()
        self.spawnItem()
        return task.cont

    def AIUpdate(self, task):
        if len(self.enemyList) <= 0:
            return False
        else:
            self.AiWorld.update()
            for enemy in self.enemyList:
                enemy.model.setP(-90)
                enemy.model.setH(enemy.model.getH() + 180)
        return task.cont

APP = Main()
APP.run()
