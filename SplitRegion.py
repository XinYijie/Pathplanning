from GemoBase import *
from SliceAlgo import *
from GenHatch import *
from pyclipper import *
import pyclipper
from Polyline import *
from ClipperAdaptor import *


class SplitRegion:
    def __init__(self, polygons, adjustPolyDirs=False):  # 初始化函数
        self.polygons = polygons  # 在类中保存多边形
        if adjustPolyDirs:  # 如果需要调整多边形方向，则
            adjustPolygonDirs(self.polygons)  # 将其调整成外逆内顺的方向
        self.splitPolygons = self.split()  # 分区结果存储在splitPolygons 中

    def split(self):  # 定义核心切分流程控制函数
        turnPts = self.findTurnPoints()  # 获取轮廓上的所有凹峰点
        if len(turnPts) != 0:  # 如果凹峰点个数不为0，则继续
            ys = []
            for pt in turnPts:  # 收集扫描高度，并对其排序
                ys.append(pt.y)
            ys.sort()
            hatchPtses = calcHatchPoints(self.polygons, ys)  # 计算扫描线和轮廓交点
            splitters = []  # 定义切分矩形列表
            for turnPt in turnPts:  # 根据凹峰点构造切分矩形
                lPt, rPt = self.findLRPoints(turnPt, hatchPtses)  # 寻找凹峰点两侧最近点
                if lPt is not None and rPt is not None:
                    splitter = self.createSplitter(lPt, rPt)  # 根据两侧最近点构造切分矩形
                    splitters.append(splitter)
            if len(splitters) != 0:  # 如果切分矩形个数不为0，继续
                clipper, ca = pyclipper.Pyclipper(), ClipperAdaptor()  # 构造Clipper 对象
                clipper.AddPaths(ca.toPaths(self.polygons), pyclipper.PT_SUBJECT)
                clipper.AddPaths(ca.toPaths(splitters), pyclipper.PT_CLIP)
                sln = clipper.Execute(pyclipper.CT_DIFFERENCE)  # 布尔差运算
                return ca.toPolys(sln, turnPts[0].z)  # 返回裁剪结果
        return self.polygons  # 对单连通区域，则直接返回输入

    def findTurnPoints(self):  # 凹峰点寻找函数
        vx = Vector3D(1, 0, 0)  # 定义和X 轴平行的向量vx
        turnPts = []  # 定义凹峰点列表turnPts
        for poly in self.polygons:  # 遍历多边形列表
            for i in range(poly.count() - 1):  # 遍历多边形中的每个点
                pts = poly.points
                v1 = pts[-2 if (i == 0) else (i - 1)].pointTo(pts[i])  # 前一点到当前点向量
                v2 = pts[i].pointTo(pts[i + 1])  # 当前点到下一点向量
                if v1.crossProduct(vx).dz * v2.crossProduct(vx).dz <= 0:  # 满足式(9-12)，峰点
                    if v1.crossProduct(v2).dz < 0:  # 是否满足式(9-9)，凹点
                        turnPts.append(pts[i])  # 同时满足，则添加至凹峰点列表
        return turnPts  # 返回凹峰点列表

    def findLRPoints(self, pt, ptses):  # 寻找凹峰点两侧交点函数
        for pts in ptses:  # 遍历二维点列表第一个维度
            if pts == []:
                continue
            if pts[0].y == pt.y:  # 定位高度相等的层
                for i in range(len(pts) - 1):  # 遍历列表第二个维度
                    if pt.x > pts[i].x and pt.x < pts[i + 1].x:  # 通过x 坐标定位凹峰点两侧点
                        return pts[i], pts[i + 1]  # 返回找到的两侧点
        return None, None

    def createSplitter(self, p1, p2, delta=1.0e-4):  # 创建切分矩形
        vx, vy = Vector3D(1, 0, 0), Vector3D(0, 1, 0)  # 创建沿X、Y 轴的单位向量
        splitter = Polyline.Polyline()  # 切分矩形实际为封闭多段线
        splitter.addPoint(p1 - vx.amplified(delta) - vy.amplified(delta))
        splitter.addPoint(p2 + vx.amplified(delta) - vy.amplified(delta))
        splitter.addPoint(p2 + vx.amplified(delta) + vy.amplified(delta))
        splitter.addPoint(p1 - vx.amplified(delta) + vy.amplified(delta))
        splitter.addPoint(splitter.startPoint())  # 封闭多段线
        return splitter


def splitRegion(polygons, adjustPolyDirs=False):  # 定义SplitRegion 类的接口函数
    return SplitRegion(polygons, adjustPolyDirs).splitPolygons
