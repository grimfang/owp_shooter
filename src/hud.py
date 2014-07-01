from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode


class Hud(DirectObject):
    def __init__(self):
        self.frameCharStatus = DirectFrame(
            # size of the frame
            frameSize = (0, .8,
                         -.20, 0),
            # bg color Transparent
            frameColor = (0, 0, 0, 0))
        self.frameCharStatus.reparentTo(base.a2dTopLeft)

        self.statusHealth = OnscreenImage(
            image = "HUD_Life100.png",
            scale = (0.1, 1, 0.1),
            pos = (0.085, 0, -0.085))
        self.statusHealth.setTransparency(True)
        self.statusHealth.reparentTo(self.frameCharStatus)

        self.statusWeapon = OnscreenImage(
            image = "WeaponMG.png",
            scale = (0.1, 1, 0.1),
            pos = (0.285, 0, -0.085))
        self.statusWeapon.setTransparency(True)
        self.statusWeapon.reparentTo(self.frameCharStatus)

        self.highscore = DirectLabel(
            text = "0",
            text_fg = (0,0,0,1),
            text_align = TextNode.ALeft,
            frameColor = (0,0,0,0),
            pos = (0.4,0,-0.12),
            scale = 0.15)
        self.highscore.setTransparency(True)
        self.highscore.reparentTo(self.frameCharStatus)

    def show(self):
        self.frameCharStatus.show()
        self.accept("setHighscore", self.setHighscore)
        self.accept("setHealth", self.setHealth)

    def hide(self):
        self.frameCharStatus.hide()
        self.ignore("setHighscore")
        self.ignore("setHealth")

    def setHighscore(self, score):
        self.highscore["text"] = str(score)

    def setHealth(self, hp):
        if hp > 75.0:
            self.statusHealth.setImage("HUD_Life100.png")
        elif hp > 50.0:
            self.statusHealth.setImage("HUD_Life75.png")
        elif hp > 25.0:
            self.statusHealth.setImage("HUD_Life50.png")
        elif hp > 0:
            self.statusHealth.setImage("HUD_Life25.png")
        else:
            print "Your dead!"
            self.statusHealth.setImage("HUD_Life0.png")
        self.statusHealth.setTransparency(True)

    def setWeapon(self, weaponType):
        if weaponType == "Pistol":
            self.statusWeapon.setImage("WeaponPistol.png")
        else:
            self.statusWeapon.setImage("WeaponMG.png")
        self.statusWeapon.setTransparency(True)
