from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3, CollisionNode, CollisionRay, GeomNode

class Mouse(DirectObject):
    def __init__(self, _main):
        self.main = _main

        # Setup mouse ray
        pickerNode = CollisionNode('MouseRay')
        self.pickerNP = base.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.main.addToTrav(self.pickerNP)


    def getMousePos(self):

    	if base.mouseWatcherNode.hasMouse():
    		mpos = base.mouseWatcherNode.getMouse()
    		self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
    		print mpos

