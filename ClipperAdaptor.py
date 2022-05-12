import math
import Polyline
from GemoBase import Point3D
from pyclipper import *
import pyclipper
# class ClipperAdaptor:
#     def __init__(self,digits=7):
#         self.f=math.pow(10,digits)     #数值精度，默认为7位小数
#         self.arcTolerance=0.005       #圆弧精度，默认为0.005
#     def PolylineToPath(self,poly):    #将polyline转化为PATH
#         path=[]
#         for pt in poly.points:
#             path.append((pt.x*self.f,pt.y*self.f))
#         return path
#     def PolyToPaths(self,polys):
#         paths=[]
#         for poly in polys:
#             paths.append(self.PolylineToPath(poly))
#         return paths
#     def PathToPoly(self,path,z=0,closed=True):
#         poly=Polyline.Polyline()
#         for tp in path:
#             poly.addPoint(Point3D(tp[0]/self.f,tp[1]/self.f,z))
#         if len(path)>0 and closed:
#             poly.addPoint(poly.startPoint())
#         return poly
#     def PathToPolys(self,paths,z=0,closed=True):
#         polys=[]
#         for path in paths:
#             polys.append(self.PathToPoly(path, z, closed))
#         return polys
#     def offsetPolygons(self,polys,delta,jt=JT_SQUARE):
#         pco=PyclipperOffset()
#         pco.ArcTolerance=self.arcTolerance*self.f
#         pco.AddPaths(self.PolyToPaths(polys), jt, ET_CLOSEDPOLYGON)
#         sln=pco.Execute(delta * self.f)
#         return self.PathToPolys(sln,polys[0].point(0).z)
#     def offsetPolygon(self,poly,delta,jt=JT_SQUARE):
#         pco = PyclipperOffset()
#         pco.ArcTolerance = self.arcTolerance * self.f
#         path = self.PolylineToPath(poly)
#         pco.AddPath(path,jt,ET_CLOSEDPOLYGON)
#         sln=pco.Execute(delta*self.f)
#         return self.PathToPolys(sln, poly.point(0).z)
class ClipperAdaptor: # 定义Clipper 适配器类
    def __init__(self, digits = 7): # 初始化函数
        self.f = math.pow(10, digits) # 数值精度，默认为7 位小数
        self.arcTolerance = 0.005

    def toPath(self, poly): # 将Polyline 转化为Path
        path = []
        for pt in poly.points:
            path.append((pt.x * self.f, pt.y * self.f)) # 放大点坐标
        return path
    def toPaths(self, polys): # 函数toPath 的复数形式
        paths = []
        for poly in polys:
            paths.append(self.toPath(poly))
        return paths
    def toPoly(self, path, z = 0, closed = True): # 将Path 转化为Polyline
        poly = Polyline.Polyline()
        for tp in path:
            poly.addPoint(Point3D(tp[0] / self.f, tp[1] / self.f, z)) # 缩小点坐标
        if len(path) > 0 and closed: # 如果封闭，则将起点添加到轮廓
            poly.addPoint(poly.startPoint()) # 最后一点
        return poly
    def toPolys(self, paths, z = 0, closed = True): # 函数toPoly 的复数形式
        polys = []
        for path in paths:
            polys.append(self.toPoly(path, z, closed))
        return polys
    def offsetPolygons(self, polys, delta, jt = pyclipper.JT_SQUARE): # 偏函数，输入Polyline 列表
        pco = pyclipper.PyclipperOffset()
        pco.ArcTolerance = self.arcTolerance * self.f # 指定pco 的圆弧精度，放大
        pco.AddPaths(self.toPaths(polys), jt, pyclipper.ET_CLOSEDPOLYGON)
        sln = pco.Execute(delta * self.f) # 偏置距离也须同时放大
        return self.toPolys(sln, polys[0].point(0).z) # 返回Polyline

    def clip(self, subjPolys, clipPolys, clipType, z = 0, minArea = 0.01):
        clipper = pyclipper.Pyclipper()
        clipper.AddPaths(self.toPaths(subjPolys), pyclipper.PT_SUBJECT)
        clipper.AddPaths(self.toPaths(clipPolys), pyclipper.PT_CLIP)
        sln = clipper.Execute(clipType)
        slnPolys = self.toPolys(sln, z)
        for i in range(len(slnPolys)-1, -1, -1):
            if math.fabs(slnPolys[i].getArea()) < minArea:
                del slnPolys[i]
        return slnPolys
        
    def PolylineToPath(self,poly):    #将polyline转化为PATH
            path=[]
            for pt in poly.points:
                path.append((pt.x*self.f,pt.y*self.f))
            return path
    def PolyToPaths(self,polys):
        paths=[]
        for poly in polys:
            paths.append(self.PolylineToPath(poly))
        return paths
    def PathToPoly(self,path,z=0,closed=True):
        poly=Polyline.Polyline()
        for tp in path:
            poly.addPoint(Point3D(tp[0]/self.f,tp[1]/self.f,z))
        if len(path)>0 and closed:
            poly.addPoint(poly.startPoint())
        return poly
    def PathToPolys(self,paths,z=0,closed=True):
        polys=[]
        for path in paths:
            polys.append(self.PathToPoly(path, z, closed))
        return polys
    def offsetPolygons(self,polys,delta,jt=JT_SQUARE):
        pco=PyclipperOffset()
        pco.ArcTolerance=self.arcTolerance*self.f
        pco.AddPaths(self.PolyToPaths(polys), jt, ET_CLOSEDPOLYGON)
        sln=pco.Execute(delta * self.f)
        return self.PathToPolys(sln,polys[0].point(0).z)
    def offsetPolygon(self,poly,delta,jt=JT_SQUARE):
        pco = PyclipperOffset()
        pco.ArcTolerance = self.arcTolerance * self.f
        path = self.PolylineToPath(poly)
        pco.AddPath(path,jt,ET_CLOSEDPOLYGON)
        sln=pco.Execute(delta*self.f)
        return self.PathToPolys(sln, poly.point(0).z)