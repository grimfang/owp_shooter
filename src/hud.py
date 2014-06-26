from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import DirectFrame


class Hud():
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

    def show(self):
        self.frameCharStatus.show()

    def hide(self):
        self.frameCharStatus.hide()
