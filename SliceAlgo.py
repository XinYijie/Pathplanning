# from Layer import *
# import Layer
from LinkSegs_dorder import *
from IntersectStl_sweep import *
import Polyline
from Polyline import *
from TopoSlicer import *
import struct


class Layer:
    def __init__(self, z):
        self.z = z
        self.segments = []
        self.contours = []
        self.shellContours = []
        self.ffContours = []
        self.sfContours = []


def intersectStl_brutal(stlModel, layerThickness):
    layers = []
    xMin, xMax, yMin, yMax, zMin, zMax = stlModel.getBounds()
    z = zMin + layerThickness
    while z < zMax:
        layer = Layer(z)
        for tri in stlModel.triangles:
            seg = intersectTriangleZPlane(tri, z)
            if seg is not None:
                layer.segments.append(seg)
        layers.append(layer)
        z += layerThickness
    return layers


def linkSegs_brutal(segs):
    segs = list(segs)
    contours = []
    while len(segs) > 0:
        contour = Polyline()
        contours.append(contour)
        while len(segs) > 0:
            for seg in segs:
                if contour.appendSegment(seg):
                    segs.remove(seg)
                    break
            if contour.isClosed():
                break
    return contours


def intersectStl_sweep(stlModel, layerThickness):
    return IntersectStl_sweep(stlModel, layerThickness).layers


def linkSegs_dorder(segs):
    return LinkSeg_dorder(segs).contours


def adjustPolygonDirs(polygons):  # 调整多边形方向的函数，输入为轮廓列表
    for i in range(len(polygons)):  # 第一个循环，取出多边形的起点
        pt = polygons[i].startPoint()
        insideCount = 0
        for j in range(len(polygons)):  # 第二个循环
            if j == i: continue
            restPoly = polygons[j]
            if 1 == pointInPolygon(pt, restPoly):
                insideCount += 1
        if insideCount % 2 == 0:
            polygons[i].makeCCW()
        else:
            polygons[i].makeCW()


def writeSlcFile(layers, path):
    f = None
    try:
        f = open(path, 'w+b')  # 打开或创建一个二进制文件
        f.write(bytes("-SLCVER 2.0 -UNIT MM", encoding='utf-8'))
        f.write(bytes([0x0d, 0x0a, 0x1a]))
        f.write(bytes([0x00] * 256))
        f.write(struct.pack('b', 1))
        f.write(struct.pack('4f', 0, 0, 0, 0))
        for layer in layers:
            f.write(struct.pack('fI', layer.z, len(layer.contours)))
            for contour in layer.contours:
                f.write(struct.pack('2I', contour.count(), 0))
                for pt in contour.points:
                    f.write(struct.pack('2f', pt.x, pt.y))
        f.write(struct.pack('fI', layers[-1].z, 0xFFFFFFFF))
    except Exception as ex:
        print("writeSlcFile exception:", ex)
    finally:
        if f: f.close()
        # return layers


def readSlcFile(path):  # 输入需要读取的SLC 文件名
    f = None
    layers = []
    try:
        f = open(path, 'rb')  # 以二进制读取的方式打开文件
        data = f.read()  # 将文件所有数据读取到data
        i = 0
        while True:  # 读取到Header 文件结尾
            if data[i] == 0x0d and data[i + 1] == 0x0a and data[i + 2] == 0x1a:
                break
            i += 1
        i += (3 + 256)  # 跳过Reserved 区的256 个字节
        channelCount = data[i]  # 获取Sampling Table 区通道数
        i += (1 + channelCount * 16)
        while True:  # 获取Contour Data 区数据
            z, = struct.unpack('f', data[i: i + 4])  # 获取当前层高
            i += 4
            contourCount, = struct.unpack('I', data[i: i + 4])  # 获取当前层上轮廓数
            i += 4
            if contourCount == 0xFFFFFFFF:  # 如果碰到结尾标识，则退出
                break
            layer = Layer(z)  # 新建Layer 对象
            for j in range(contourCount):
                pointCount, = struct.unpack('I', data[i: i + 4])  # 获取当前轮廓点数
                i += 4
                gapCount, = struct.unpack('I', data[i: i + 4])
                i += 4
                contour = Polyline()  # 新建轮廓
                for k in range(pointCount):
                    x, y = struct.unpack('2f', data[i: i + 8])
                    i += 8
                    contour.addPoint(Point3D(x, y, z))  # 向轮廓添加坐标
                layer.contours.append(contour)
            layers.append(layer)
    except Exception as ex:
        print("readSlcFile exception:", ex)  # 打印异常
    finally:
        if f: f.close()
        return layers  # 返回Layer 对象列表


def slice_topo(stlModel, layerThickness):  # 定义函数
    return TopoSlicer(stlModel, layerThickness).layers

# def readSlcFile(path):
