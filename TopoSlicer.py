import GemoBase
from Segment import *
from IntersectStl_sweep import *
from Polyline import *
import StlModel
from StlModel import *
from Layer import *


# class Layer:
#     def __init__(self,z):
#         self.z=z
#         self.segments=[]
#         self.contours=[]
#         self.shellContours = []
#         self.ffContours = []
#         self.sfContours = []
class TVertex:  # 定义Tvertex类，顶点拓扑类
    def __init__(self, pnt3d, digits=7):
        self.x = round(pnt3d.x, digits)
        self.y = round(pnt3d.y, digits)
        self.z = round(pnt3d.z, digits)
        self.faces = []  # 和顶点相接触的面片的引用

    def toTuple(self):  # 将顶点转化为元组
        return (self.x, self.y, self.z)

    def toPoint3D(self):
        return GemoBase.Point3D(self.x, self.y, self.z)

    def isSmaller(self, other):  # 比较两个顶点的大小
        if self.x < other.x:
            return True
        elif self.x == other.x and self.y < other.y:
            return True
        elif self.x == other.x and self.y == other.y and self.z < other.z:
            return True
        return False


class TEdge:  # 定义棱边拓扑类
    def __init__(self, tA, tB):
        self.A, self.B = tA, tB
        self.F = None  # 所从属的面片引用
        self.OE = None  # 对边引用

    def toTuple(self):  # 将边转化为元组
        if self.A.isSmaller(self.B):
            return (self.A.x, self.A.y, self.A.z, self.B.x, self.B.y, self.B.z)
        else:
            return (self.B.x, self.B.y, self.B.z, self.A.x, self.A.y, self.A.z)

    def intersect(self, z):
        if min(self.A.z, self.B.z) > z or max(self.A.z, self.B.z) < z:
            return None
        elif self.A.z == self.B.z == z:
            return None
        else:
            if z == self.A.z:
                self.A.toPoint3D()
            else:
                ratio = (z - self.A.z) / (self.B.z - self.A.z)
                vec = self.A.toPoint3D().pointTo(self.B.toPoint3D()).amplified(ratio)
                pnt = self.A.toPoint3D() + vec
                return pnt

    def intersect_v1(self, z):  # 定义intersect_v1，返回交点
        seg = Segment(self.A.toPoint3D(), self.B.toPoint3D())  # 线段构造
        pln = Plane.zPlane(z)  # 截平面构造
        return intersectSegmentPlane(seg, pln)  # 返回截交点


class TFace:  # 定义TFace类
    def __init__(self, tA, tB, tC, te1, te2, te3):  # 关联3个顶点，三条线段
        self.A, self.B, self.C = tA, tB, tC
        self.E1, self.E2, self.E3 = te1, te2, te3
        self.used = False  # 面片是否被使用过

    def zMin(self):
        return min(self.A.z, self.B.z, self.C.z)

    def zMax(self):
        return max(self.A.z, self.B.z, self.C.z)

    def intersect(self, z):  # 面片和z平面截交
        if self.zMin() > z or self.zMax() < z:
            return None, None, None
        elif self.A.z == self.B.z == self.C.z == z:
            return None, None, None
        else:  # 求截交
            c1 = self.E1.intersect(z)
            c2 = self.E2.intersect(z)
            c3 = self.E3.intersect(z)
            if c1 is None:
                if c2 is not None and c3 is not None:
                    if c2.distance(c3) != 0.0:
                        return Segment(c2, c3), [self.E2, self.E3], None
            elif c2 is None:
                if c1 is not None and c3 is not None:
                    if c1.distance(c3) != 0.0:
                        return Segment(c1, c3), [self.E1, self.E3], None
            elif c3 is None:
                if c2 is not None and c1 is not None:
                    if c2.distance(c1) != 0.0:
                        return Segment(c1, c2), [self.E1, self.E2], None
            elif c1 is not None and c2 is not None and c3 is not None:
                if c1.isIdentical(c2):
                    return Segment(c1, c3), [self.E3], self.B
                elif c2.isIdentical(c3):
                    return Segment(c1, c2), [self.E1], self.C
                elif c3.isIdentical(c1):
                    return Segment(c2, c3), [self.E2], self.A
            return None, None, None


class TModel:  # 定义 TModel，拓扑模型
    def __init__(self, stlModel):  # 根据输入 STL模型初始化
        self.vxDic = {}  # 顶点字典
        self.egDic = {}  # 半边字典
        self.faces = []  # 面片列表
        self.stlModel = stlModel  # 保存 STL模型
        self.createTModel()  # 调用模型拓扑重建函数

    def createTModel(self):  # 核心函数：模型拓扑重建
        for t in self.stlModel.triangles:  # 遍历 STL模型中面片 t
            A, B, C = TVertex(t.A), TVertex(t.B), TVertex(t.C)  # 根据 Point3D创建 TVertex
            if A.toTuple() not in self.vxDic.keys():  # 检查顶点 A是否在 vxDic中
                self.vxDic[A.toTuple()] = A  # 如果不在，则添加
            if B.toTuple() not in self.vxDic.keys():  # 检查顶点 B
                self.vxDic[B.toTuple()] = B
            if C.toTuple() not in self.vxDic.keys():  # 检查顶点 C
                self.vxDic[C.toTuple()] = C
            tA = self.vxDic[A.toTuple()]  # 从 vxDic中根据 A坐标查询
            tB = self.vxDic[B.toTuple()]  # 保存的顶点引用 tA、 tB、 tC
            tC = self.vxDic[C.toTuple()]
            e1, e2, e3 = TEdge(tA, tB), TEdge(tB, tC), TEdge(tC, tA)  # 创建半边 e1、 e2、 e3
            f = TFace(tA, tB, tC, e1, e2, e3)  # 创建面 f
            self.faces.append(f)  # 将面 f 添加至列表 faces
            tA.faces.append(f)  # 将面 f 分别添加至
            tB.faces.append(f)  # 顶点 tA、 tB、 tC的 faces
            tC.faces.append(f)
            e1.F = e2.F = e3.F = f  # 对半边的 F属性赋值
            e1tp, e2tp, e3tp = e1.toTuple(), e2.toTuple(), e3.toTuple()  # 保存 半边 6维坐标
            if e1tp not in self.egDic.keys():  # 如果半边坐标不在 egDic中，
                self.egDic[e1tp] = []  # 则将半边列表添加到 egDic
            self.egDic[e1tp].append(e1)  # 中，然后添加半边到列表
            if e2tp not in self.egDic.keys():
                self.egDic[e2tp] = []
            self.egDic[e2tp].append(e2)
            if e3tp not in self.egDic.keys():
                self.egDic[e3tp] = []
            self.egDic[e3tp].append(e3)
        for edges in self.egDic.values():  # 遍历 egDic，建立成对半边
            if len(edges) == 2:  # 之间的索引关系
                edges[0].OE = edges[1]
                edges[1].OE = edges[0]
            else:  # 对落单的半边，暂不做处理
                print('Single edge')


class TopoSlicer:  # 定义 TopoSlicer类
    def __init__(self, stlModel, layerThickness):  # 根据 STL模型和切片层高初始化
        self.stlModel = stlModel  # 保存 STL模型
        self.layerThickness = layerThickness  # 保存切片层高
        self.topoModel = TModel(stlModel)  # 将 STL转化为拓扑模型
        self.layers = []  # 用于保存生成的切片轮廓
        self.slice()  # 调用切片函数

    def slice(self):  # 定义 slice函数
        self.topoModel.faces.sort(key=lambda t: t.zMin())  # 对面片最低点从低到高排序
        zs = self.genLayerHeights()  # 生成层高列表 zs
        k = 0  # 扫描平面法
        sweep = SweepPlane()  # 定义扫描平面 sweep
        for z in zs:
            for i in range(len(sweep.triangles) - 1, -1, -1):  # 从 sweep上移除不相交面片
                if z > sweep.triangles[i].zMax():
                    del sweep.triangles[i]
            for i in range(k, len(self.topoModel.faces)):  # 往 sweep上添加新面片
                face = self.topoModel.faces[i]
                if z >= face.zMin() and z <= face.zMax():
                    sweep.triangles.append(face)
                elif face.zMin() > z:
                    k = i
                    break
            layer = self.createLayerContours(z, sweep.triangles)  # 生成切片轮廓
            self.layers.append(layer)

    def findSeedFace(self, faces):  # 定义 种子面片 寻找函数
        for face in faces:
            if face.used == False:
                return face
        return None

    def findNextFace(self, edges, node):  # 定义目标邻面寻找函数
        nextFace = None  # 记返回面片 为 nextFace
        if node is None:  # 情形 1. 交点在两半边
            e0, e1 = edges[0], edges[1]
            if e1.OE is not None and e1.OE.F.used == False:  # 检查 e1对边的面是否已用
                nextFace = e1.OE.F  # 我们是有意先检查 e1的
            elif e0.OE is not None and e0.OE.F.used == False:  # 检查 e0对边的面是否已用
                nextFace = e0.OE.F
        else:  # 情形 2. 交点 在半边和顶点
            e = edges[0]
            if e.OE is not None and e.OE.F.used == False:  # 检查 e对边的面是否已用
                nextFace = e.OE.F  # 如果未用，则目标邻面为该面
            else:  # 否则检查和 node相接的面
                for f in node.faces:  # 遍历 node相接面
                    if f is not e.F:  # 待检查面不能是当前面
                        seg, egs, n = e.F.intersect(node.z)  # 计算待检查面和 z平面交线
                        if seg is not None:  # 存在交线，则目标邻面为该面
                            nextFace = f
                            break
        return nextFace  # 返回目标邻面

    def createLayerContours(self, z, faces):  # 定义切片轮廓创建函数
        layer = Layer(z)  # 切片数据 layer
        for f in faces:  # 清洗 faces，置未使用
            f.used = False
        while True:  # 第 1层循环
            f = self.findSeedFace(faces)  # 寻找种子面片 f
            if f is None:  # 找不到种子，退出循环 1
                break
            contour = Polyline()  # 新建 contour
            while True:  # 第 2层循环
                seg, edges, node = f.intersect(z)  # 计算面片和截平面交线
                f.used = True  # 设置面片为已用
                if seg is None:  # 退出条件 1：无交线
                    break
                contour.appendSegment(seg)  # 将交线添加至 contour
                if contour.isClosed():  # 退出条件 2：轮廓封闭
                    break
                f = self.findNextFace(edges, node)  # 寻找下一面片
                if f is None:  # 退出条件 3：无邻面
                    break
            if contour.count() > 0:  # 判断轮廓顶点数是否大于 0
                layer.contours.append(contour)  # 大于 0则将其添加至 layer
        return layer

    def genLayerHeights(self):  # 定义层高列表生成函数
        xMin, xMax, yMin, yMax, zMin, zMax = self.stlModel.getBounds()
        zs = []
        z = zMin + self.layerThickness
        while z < zMax:
            zs.append(z)
            z += self.layerThickness
        return zs
