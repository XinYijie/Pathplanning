import ClipperAdaptor
from pyclipper import *
import pyclipper
import math
from Polyline import *
from PolyPrcSeeker import *


class GenCpPath:
    def __init__(self, boundaries, interval, skinThickness, label):
        self.label = label
        self.boundaries = boundaries
        self.interval = interval  # 工艺参数，偏置距离
        self.skinThickness = skinThickness
        self.arcTolerance = 0.005
        self.jointType = pyclipper.JT_SQUARE
        self.offsetPolyses = []  # 临时存储的中间偏置曲线列表
        self.paths = []  # 最终输出的轮廓平行路径列表
        self.offset()
        self.linkLocalOffsets()

    def offset(self):  # 定义连续偏置路径生成函数
        ca = ClipperAdaptor.ClipperAdaptor()
        ca.arcTolerance = self.arcTolerance
        delta = self.interval / 2  # 首次偏置距离
        polys = ca.offsetPolygons(self.boundaries, -delta, self.jointType)
        self.offsetPolyses.append(polys)  # 偏置曲线存放在offsetPolys中
        while math.fabs(delta) < self.skinThickness:  # 循环直至偏置距离大于线宽
            delta += self.interval
            polys = ca.offsetPolygons(self.boundaries, -delta, self.jointType)
            if polys is None or len(polys) == 0:
                break
            self.offsetPolyses.append(polys)
        if self.label == 'path':
            # ---------------------------------
            for poly1s in self.offsetPolyses:
                self.paths.append(poly1s)
            # ---------------------------------

    def linkToParent(self, child):
        parent = child.parent
        pt = child.startPoint()
        dMin, iAtdMin = float('inf'), 0
        for i in range(parent.count()):
            d = pt.distanceSquare(parent.point(i))
            if d < dMin:
                dMin, iAtdMin = d, i
        newPoly = Polyline()
        for i in range(iAtdMin + 1):
            newPoly.addPoint(parent.point(i).clone())
        newPoly.endPoint().w = 1
        for i in range(child.count()):
            newPoly.addPoint(child.point(i).clone())
        newPoly.endPoint().w = 1
        for i in range(iAtdMin, parent.count(), 1):
            newPoly.addPoint(parent.point(i).clone())
        return newPoly

    def linkLocalOffsets(self):
        if self.label == 'code':
            offsetPolys = seekPolyPrc(self.offsetPolyses)
            for i in range(len(offsetPolys) - 1, 0, -1):
                child = offsetPolys[i]
                if child.parent is not None:
                    newPoly = self.linkToParent(child)
                    parent = child.parent
                    parent.points = newPoly.points
                    del offsetPolys[i]
            for path in offsetPolys:
                self.paths.append(path)
            self.offsetPolyses.clear()
            # for path in self.offsetPolyses[0]:
            #     self.paths.append(path)
            # self.offsetPolyses.clear()
        else:
            pass


def genCpPath(boundaries, interval, skinThickness, label):
    return GenCpPath(boundaries, interval, skinThickness, label).paths  # .offsetPolyses


def linktoParent(child):
    parent = child.parent
    pt = child.startPoint()
    dMin, iAtdMin = float('inf'), 0
    for i in range(parent.count()):
        d = pt.distanceSquare(parent.point(i))
        if d < dMin:
            dMin, iAtdMin = d, i
    newPoly = Polyline()
    for i in range(iAtdMin + 1):
        newPoly.addPoint(parent.point(i).clone())
    newPoly.endPoint().w = 1
    for i in range(child.count()):
        newPoly.addPoint(child.point(i).clone())
    newPoly.endPoint().w = 1
    for i in range(iAtdMin, parent.count(), 1):
        newPoly.addPoint(parent.point(i).clone())
    return newPoly
