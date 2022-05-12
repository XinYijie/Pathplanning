from GemoAlgo import *
import GemoAlgo
from SplitRegion import *
from Polyline import *


class GenDpPath:  # 定义GenDpPath 类
    def __init__(self, polygons, interval, angle):  # 输入多边形列表、间距、角度
        self.polygons, self.interval, self.angle = polygons, interval, angle
        self.splitPolys = []  # 保存分区得到的单连通多边形

    def generate(self):  # 定义平行路径核心函数
        rotPolys = GemoAlgo.rotatePolygons(self.polygons, -self.angle)  # 旋转输入多边形
        self.splitPolys = splitRegion(rotPolys)  # 分区生成单连通区域
        ys = self.genScanYs(rotPolys)  # 生成扫描高度
        paths = []  # 保存临时已连接路径
        for poly in self.splitPolys:  # 遍历每个单连通区域
            segs = genHatches([poly], ys)  # 在单连通区域内生成填充线
            if len(segs) > 0:
                path = self.linkLocalHatches(segs)  # 连接单连通区域内填充线段
                paths.append(path)
        return GemoAlgo.rotatePolygons(paths, self.angle)  # 旋转生成的连接路径列表

    def genScanYs(self, polygons):  # 定义扫描高度生成函数
        ys, yMin, yMax = [], float('inf'), float('-inf')
        for poly in polygons:  # 首先找出所有多边形的最低点
            for pt in poly.points:  # 和最高点
                yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
        y = yMin + self.interval  # 然后根据填充间距生成高度
        while y < yMax:  # 列表
            ys.append(y)
            y += self.interval
        return ys

    def linkLocalHatches(self, segs):  # 定义链接单连通区域内的
        poly = Polyline()  # 填充线函数
        for i, seg in enumerate(segs):  # 遍历列表，获取序号和元素
            poly.addPoint(seg.A if (i % 2 == 0) else seg.B)  # 采用zig-zag 的连接方式，
            poly.addPoint(seg.B if (i % 2 == 0) else seg.A)  # 头和头连，尾和尾连
            poly.endPoint().w = 1  # 标记连接线起点w 为1
        return poly


def genDpPath(polygons, interval, angle):  # 定义GenDpPath 类的全局接口
    return GenDpPath(polygons, interval, angle).generate()  #
