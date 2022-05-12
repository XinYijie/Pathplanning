from LinkPoint import *
from GemoBase import *
import Polyline
import functools
def cmp_pntSmaller(lp1,lp2):
    if(lp1.x<lp2.x):
        return -1
    elif(lp1.x==lp2.x and lp1.y<lp2.y):
        return -1
    elif lp1.x==lp2.x and lp1.y==lp2.y and lp1.z<lp2.z:
        return -1
    elif lp1.x==lp2.x and lp1.y==lp2.y and lp1.z==lp2.z:
        return 0
    else:return 1
class LinkSeg_dorder:
    def __init__(self,segs):
        self.segs=segs
        self.contours=[]
        self.polys=[]
        self.link()
    def createLpList(self):     #根据输入线段构建链接点列表
        lpnts=[]
        for seg in self.segs:
            lp1,lp2=LinkPoint(seg.A),LinkPoint(seg.B)
            lp1.other,lp2.other=lp2,lp1
            lpnts.append(lp1)
            lpnts.append(lp2)
        lpnts.sort(key=functools.cmp_to_key(cmp_pntSmaller))
        for i in range(len(lpnts)):
            lpnts[i].index=i
        return lpnts
    def findUnusedPnt(self,lpnts):
        startIndex=-1
        for lpnt in lpnts:
            if lpnt.used==False:
                startIndex=lpnt.index
                break
        return startIndex
    def link(self):    #定义线段字典核心拼接函数
        lpnts=self.createLpList()
        cnt=len(lpnts)
        while True:
            startIndex=self.findUnusedPnt(lpnts)
            if startIndex==-1:
                break
            p=lpnts[startIndex]
            poly=Polyline.Polyline()
            while True:
                poly.addPoint(p.toPoint3D())
                p.used,p.other.used=True,True
                if poly.isClosed():
                    self.contours.append(poly)
                    break
                index=p.other.index
                if index-1>=0 and p.other.toPoint3D().isCoincide(lpnts[index-1].toPoint3D()):
                    p=lpnts[index-1]
                elif index+1<cnt and p.other.toPoint3D().isCoincide(lpnts[index+1].toPoint3D()):
                    p=lpnts[index+1]
                else:
                    self.polys.append(poly)
                    break     #未封闭 不正常的退出
