from GemoBase import Point3D
class LinkPoint:
    def __init__(self,pnt3d,digits=7):
        self.x=round(pnt3d.x,digits)
        self.y=round(pnt3d.y,digits)
        self.z=round(pnt3d.z,digits)
        self.other=None
        self.used=False
        self.index=0
    def __str__(self):
        return 'LinkPoint:\nused:%s\nself(%s,%s,%s)\nother(%s,%s,%s)\nlinked to:%s'%(self.used,self.x,self.y,self.z,self.other.x,self.other.y,self.other.z,self.other.index)
    def toPoint3D(self):
        return Point3D(self.x,self.y,self.z)