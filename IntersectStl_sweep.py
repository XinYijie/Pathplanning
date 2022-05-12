from StlModel import *
from  GemoAlgo import *
import Layer
class SweepPlane:
    def __init__(self):
        self.triangles=[]
class IntersectStl_sweep:
    def __init__(self,stlModel,layerThickness):
        self.stlModel=stlModel
        self.layerThickness=layerThickness
        self.layers=[]
        self.intersect()
    def intersect(self):
        triangles=self.stlModel.triangles
        triangles.sort(key=lambda t:t.zMinPnt())
        zs=self.getLayerHeights()
        k=0
        sweepPlane=SweepPlane()
        for z in zs:
            for i in range(len(sweepPlane.triangles)-1,-1,-1):
                if z>sweepPlane.triangles[i].zMaxPnt():
                    del sweepPlane.triangles[i]
            for i in range(k,len(triangles)):
                if z>=triangles[i].zMinPnt() and z<=triangles[i].zMaxPnt():
                    sweepPlane.triangles.append(triangles[i])
                elif z<triangles[i].zMinPnt():
                    k=i
                    break
            layer=Layer.Layer(z)
            for triangle in triangles:
                seg=intersectTriangleZPlane(triangle,z)
                if seg is not None:
                    layer.segments.append(seg)
            self.layers.append(layer)
    def getLayerHeights(self):
        xMin,xMax,yMin,yMax,zMin,zMax=self.stlModel.getBounds()
        zs=[]
        z=zMin+self.layerThickness
        while z <zMax:
            zs.append(z)
            z+=self.layerThickness
        return zs
