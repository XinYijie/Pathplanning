import vtk
from GemoBase import *
import ClipperAdaptor
import math
import Polyline
import Segment

from pyclipper import *
from GemoAlgo import *


class SweepLine:
    def __init__(self):
        self.segs = []  # 属性segs，Segment类型列表

    def intersect(self, y):  # 定义segs和y线的求交列表
        ips = []  # 交点列表
        yLine = Line(Point3D(0, y, self.segs[0].A.z), Vector3D(1, 0, 0))  # 创建和X轴平行的y线
        for seg in self.segs:
            if seg.A.y == y:
                ips.append(seg.A.clone())
            elif seg.B.y == y:
                ips.append(seg.B.clone())
            else:
                ip = intersect(yLine, seg)
                if ip is not None:
                    ips.append(ip)
        ips.sort(key=lambda p: p.x)  # 对交点按x值从小到大排列
        i = len(ips) - 1
        while i > 0:  # 移除交点中重合的点
            if ips[i].distanceSquare(ips[i - 1]) == 0:
                del ips[i]
                del ips[i - 1]
                i = i - 2
            else:
                i = i - 1
        return ips  # 返回处理后的交点列表


def genClipHatches(polygons, interval, angle):
    xMin, xMax = float('inf'), float('-inf')
    yMin, yMax = float('inf'), float('-inf')
    z = polygons[0].points[0].z
    for poly in polygons:
        for pt in poly.points:
            xMin, xMax = min(xMin, pt.x), max(xMax, pt.x)
            yMin, yMax = min(xMin, pt.y), max(yMax, pt.y)
    v = Vector3D(math.cos(angle), math.sin(angle))  # 填充方向向量
    n = Vector3D(math.cos(angle + math.pi / 2), math.sin(angle + math.pi / 2))  # 填充方向法向量
    O = Point3D((xMin + xMax) / 2, (yMin + yMax) / 2, z)  # 多边形包络矩形的圆中心
    R = math.sqrt((xMax - xMin) ** 2 + (yMax - yMin) ** 2) / 2  # 外接圆半径
    P1 = O - n.amplified(R)
    parallels = []  # 保存生成的平行线段
    for i in range(0, int(2 * R / interval) + 1, 1):
        Q = P1 + n.amplified(interval * i)
        seg = Polyline.Polyline()
        seg.addPoint(Q - v.amplified(R))
        seg.addPoint(Q + v.amplified(R))
        parallels.append(seg)
    hatchSegs = []
    ca = ClipperAdaptor.ClipperAdaptor()
    clipper = Pyclipper()
    clipper.AddPaths(ca.PolyToPaths(polygons), PT_CLIP, True)
    clipper.AddPaths(ca.PolyToPaths(parallels), PT_SUBJECT, False)
    sln = clipper.Execute2(CT_INTERSECTION)
    for child in sln.Childs:
        if len(child.Contour) > 0:
            poly = ca.PathToPoly(child.Contour, z, False)
            seg = Segment(poly.startPoint(), poly.endPoint())
            hatchSegs.append(seg)
    return hatchSegs


def calcHatchPoints(polygons, ys):  # 输入多边形和扫描线高度ys
    segs = []  # 存放多边形的线段列表
    for poly in polygons:
        for i in range(poly.count() - 1):
            seg = Segment(poly.point(i), poly.point(i + 1))
            seg.yMin, seg.yMax = min(seg.A.y, seg.B.y), max(seg.A.y, seg.B.y)
            segs.append(seg)
    segs.sort(key=lambda p: p.yMin)
    k = 0
    sweep = SweepLine()
    ipses = []
    for y in ys:
        for i in range(len(sweep.segs) - 1, -1, -1):  # 移除不再和扫描线相交的线段
            if sweep.segs[i].yMax < y:
                del sweep.segs[i]
        for i in range(k, len(segs)):  # 从segs添加和扫描线相交的线段
            if segs[i].yMin < y and segs[i].yMax >= y:
                sweep.segs.append(segs[i])
            elif segs[i].yMin >= y:
                k = i
                break
        if len(sweep.segs) > 0:
            ips = sweep.intersect(y)
            ipses.append(ips)
    return ipses


def genSweepHatches(polygons, interval, angle):
    mt = Matrix3D.createRotateMatrix('Z', -angle)  # 旋转矩阵，取
    mb = Matrix3D.createRotateMatrix('Z', angle)  # 旋转矩阵，回
    rotPolys = []  # 存储旋转后的多边形
    for poly in polygons:
        rotPolys.append(poly.multiplied(mt))
    yMin, yMax = float('inf'), float('-inf')
    for poly in rotPolys:
        for pt in poly.points:
            yMin = min(yMin, pt.y)
            yMax = max(yMax, pt.y)
    ys = []
    y = yMin + interval
    while y < yMax:
        ys.append(y)
        y += interval
    segs = genHatches(rotPolys, ys)
    for seg in segs:
        seg.multiply(mb)
    return segs


def genHatches(polygons, ys):
    segs = []
    ipses = calcHatchPoints(polygons, ys)
    for ips in ipses:
        if len(ips) < 2:
            continue
        for i in range(0, len(ips), 2):
            seg = Segment(ips[i], ips[i + 1])
            segs.append(seg)
    return segs
