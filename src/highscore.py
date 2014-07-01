#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from panda3d.core import TextNode
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectScrolledList
from direct.gui import DirectGuiGlobals as DGG

class Highscore():
    def __init__(self):

        home = os.path.expanduser("~")
        quickJNRDir = os.path.join(home, ".quickShooter")
        if not os.path.exists(quickJNRDir): os.makedirs(quickJNRDir)
        self.highscorefile = os.path.join(quickJNRDir, "highscore.txt")

        self.highscore = []

        if not os.path.exists(self.highscorefile):
            with open(self.highscorefile, "w") as f:
                f.write("""Foxy;4000
Wolf;3500
Coon;3000
Kitty;2020
Ferret;2000
Lynx;1700
Lion;1280
Tiger;800
Birdy;450
Fishy;250""")


        with open(self.highscorefile, "r+") as f:
            data = f.readlines()
            for line in data:
                name = line.split(";")[0]
                pts = line.split(";")[1]
                self.highscore.append([name, pts])


        self.lstHighscore = DirectScrolledList(
            frameSize = (-1, 1, -0.6, 0.6),
            frameColor = (0,0,0,0.5),
            pos = (0, 0, 0),
            numItemsVisible = 10,
            itemMakeFunction = self.__makeListItem,
            itemFrame_frameSize = (-0.9, 0.9, 0.0, -1),
            itemFrame_color = (1, 1, 1, 0),
            itemFrame_pos = (0, 0, 0.5))

        self.btnBack = DirectButton(
            # size of the button
            scale = (0.15, 0.15, 0.15),
            text = "Back",
            # set no relief
            relief = None,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (0.2, 0, 0.1),
            # the event which is thrown on clickSound
            command = self.btnBack_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(base.a2dBottomLeft)

        self.refreshList()
        self.hide()

    def show(self):
        self.lstHighscore.show()
        self.btnBack.show()

    def hide(self):
        self.lstHighscore.hide()
        self.btnBack.hide()

    def writeHighscore(self):
        self.__sortHigscore()
        with open(self.highscorefile, "w") as f:
            for entry in self.highscore:
                f.write("{0};{1}".format(entry[0], entry[1]))

    def refreshList(self):
        self.__sortHigscore()
        self.lstHighscore.removeAllItems()
        for entry in self.highscore:
            self.lstHighscore.addItem("{0};{1}".format(entry[0], entry[1]))

    def __makeListItem(self, highscoreItem, stuff, morestuff):
        name = highscoreItem.split(";")[0]
        pts = highscoreItem.split(";")[1]
        # left
        l = -0.9
        # right
        r = 0.9
        itemFrame = DirectFrame(
            frameColor=(1, 1, 1, 0.5),
            frameSize=(l, r, -0.1, 0),
            relief=DGG.SUNKEN,
            borderWidth=(0.01, 0.01),
            pos=(0, 0, 0))
        lblName = DirectLabel(
            pos=(l + 0.01, 0, -0.07),
            text=name,
            text_align=TextNode.ALeft,
            scale=0.07,
            frameColor=(0, 0, 0, 0))
        lblPts = DirectLabel(
            pos=(r - 0.01, 0, -0.07),
            text=pts,
            text_align=TextNode.ARight,
            scale=0.07,
            frameColor=(0, 0, 0, 0))
        lblName.reparentTo(itemFrame)
        lblPts.reparentTo(itemFrame)
        return itemFrame


    def __sortHigscore(self):
        self.highscore = sorted(
            self.highscore,
            key=lambda score: int(score[1]),
            reverse=True)[:10]

    def setPoints(self, name, points):
        self.highscore.append([name, str(points) + "\n"])
        self.refreshList()
        self.writeHighscore()

    def btnBack_Click(self):
        self.hide()
        base.messenger.send("Highscore_back")
