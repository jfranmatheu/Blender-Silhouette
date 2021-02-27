from bgl import *


def SetPoint(ps):glPointSize(ps)
def RstPoint():glPointSize(4.0)
def SetBlend():glEnable(GL_BLEND)
def RstBlend():glDisable(GL_BLEND)
def GenBuffer(w,h):return Buffer(GL_BYTE, w*h*4)
def GetPixel(x,y):b=GenBuffer(1,1);glReadPixels(int(x),int(y),1,1,GL_RGBA,GL_UNSIGNED_BYTE,b);return b
