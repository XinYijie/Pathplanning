import Utility
import math
from Polyline import *
from GemoAlgo import pointInPolygon
class PolyPrcSeeker:
    def __init__(self,polys):
        self.polys=Utility.makeListLinear(polys)
        self.seek()
    def seek(self):
        polys=self.polys
        for poly in polys:
            poly.area=math.fabs(poly.getArea())
            poly.parent=None
            poly.childs=[]
            poly.depth=0
        polys.sort(key=lambda t:t.area)      #根据面积对曲线排序
        for i in range(0,len(polys)-1,1):        #第一重循环，i从0开始
            for j in range(i+1,len(polys),1):    #第2重循环，j从i+1开始
                pt=polys[i].startPoint()         #取第一条曲线的起点为测试点
                if pointInPolygon(pt,polys[j]):
                    polys[i].parent=polys[j]     #指定父曲线
                    polys[j].childs.append(polys[i])     #指定子曲线
                    break
        for poly in polys:
            self.findPolyDepth(poly)      #计算曲线深度值
        polys.sort(key=lambda t:t.depth)    #根据曲线深度值进行排序
    def findPolyDepth(self,poly):
        crtPoly=poly
        while crtPoly.parent is not None:
            crtPoly=crtPoly.parent
            poly.depth+=1
def seekPolyPrc(polys):         #定义类使用的全局接口函数
    return PolyPrcSeeker(polys).polys

