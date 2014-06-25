#!/usr/bin/python
# -*- coding: utf-8 -*-

from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectEntry

class MainScreen():
    def __init__(self):

        self.txtPlayerName = DirectEntry(
            text="",
            scale=0.08,
            pos=(-0.15, 0, 0.6),
            initialText="Name",
            numLines = 1,
            width = 4,
            focus=False,
            focusInCommand=self.__clearText,
            focusOutCommand=self.__checkText)

        self.btnStart = DirectButton(
            text = "Start",
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (0, 0, .3),
            # the event which is thrown on clickSound
            command = self.btnStart_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnStart.setTransparency(1)

        self.btnHighscore = DirectButton(
            text = "Highscore",
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (0, 0, 0),
            # the event which is thrown on clickSound
            command = self.btnHighscore_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnHighscore.setTransparency(1)

        self.btnQuit = DirectButton(
            text = "Quit",
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (0, 0, -.3),
            # the event which is thrown on clickSound
            command = self.btnQuit_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnQuit.setTransparency(1)

    def show(self):
        self.txtPlayerName.show()
        self.btnStart.show()
        self.btnHighscore.show()
        self.btnQuit.show()

    def hide(self):
        self.txtPlayerName.hide()
        self.btnStart.hide()
        self.btnHighscore.hide()
        self.btnQuit.hide()


    def __clearText(self):
        if self.txtPlayerName.get() == "" or \
               self.txtPlayerName.get() == "Name":
            self.txtPlayerName.enterText("")

    def __checkText(self):
        if self.txtPlayerName.get() == "":
            self.txtPlayerName.enterText("Name")

    def btnStart_Click(self):
        self.hide()
        base.messenger.send("MainMenu_start")

    def btnHighscore_Click(self):
        self.hide()
        base.messenger.send("Highscore_show")

    def btnQuit_Click(self):
        base.messenger.send("MainMenu_quit")

    def getPlayername(self):
        return self.txtPlayerName.get()
