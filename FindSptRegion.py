from StlModel import *
from SliceAlgo import *
import pyclipper
from Utility import *

class FindSptRegion:
    def __init__(self, stlModel, layers, gridSize, crAngle, xyGap = 1): # 类初始化
        self.digit = 3 # 计算精度，默认保留3 位小数
        self.stlModel = stlModel # 保存三维模型引用
        self.layers = layers # 保存切片数据引用
        self.gridSize = gridSize # 预设正方形网格边长，即a 值
        self.ax, self.ay = 0, 0 # 存储调整后的网格边长ax、ay
        self.crAngle= crAngle # 支撑临界角，即θ0
        self.xyGap = xyGap # 支撑到模型的横向间隙

    def initGrids(self): # 定义网格生成函数
        xMin, xMax, yMin, yMax, zMin, zMax = self.stlModel.getBounds() # 模型各方向极限
        self.ax = (xMax - xMin) / ((int)((xMax - xMin)/self.gridSize) + 1) # 网格X 方向边长
        self.ay = (yMax - yMin) / ((int)((yMax - yMin)/self.gridSize) + 1) # 网格Y 方向边长
        xs, ys, gridDic, x, y = [], [], {}, xMin, yMin # 定义临时列表、字典变量等
        while x <= xMax: # 生成X 方向网格坐标序列
            xs.append(round(x, self.digit))
            x += self.ax
        while y <= yMax: # 生成Y 方向网格坐标序列
            ys.append(round(y, self.digit))
            y += self.ay
        for x in xs: # 生成网格字典
            for y in ys:
                gridDic[(x, y)] = [(round(zMin, self.digit), 0)]
        return xs, ys, gridDic # 返回X、Y 序列和网格字典


    def pointInTriangle(self, pt, tri, err = 1.0e-7): # 报告点是否在三角形投影内部
        A, B, C = tri.A, tri.B, tri.C
        S = self.area(A, B, C) # 大三角形面积
        S1 = self.area(pt, A, B) # 小三角形面积
        S2 = self.area(pt, B, C)
        S3 = self.area(pt, A, C)
        if math.fabs(S1 + S2 + S3 - S) < err: # 判断面积是否相等
            return True # 如果相等，则返回True
        return False # 否则返回False
    def area(self, A, B, C): # 计算由三点确定的三角形面积
        x1, x2, x3, y1, y2, y3 = A.x, B.x, C.x, A.y, B.y, C.y
        return 0.5* math.fabs(x1*y2+x2*y3+x3*y1-x1*y3-x2*y1-x3*y2)        

    def getValidGrids(self, tri, xs, ys): # 定义寻找有效网格节点函数
        A, B, C = tri.A, tri.B, tri.C
        xMin, xMax = min(A.x, B.x, C.x), max(A.x, B.x, C.x) # 面片在X 方向极值
        yMin, yMax = min(A.y, B.y, C.y), max(A.y, B.y, C.y) # 面片在Y 方向极值
        sub_xs, sub_ys = [], [] # 定义子序列
        for x in xs: # 寻找落在[xMin, xMax]的子序列
            if x >= xMin and x <= xMax:
                sub_xs.append(x)
            elif x > xMax:
                break    
        for y in ys: # 寻找落在[yMin, yMax]的子序列
            if y >= yMin and y <= yMax:
                sub_ys.append(y)
            elif y > yMax:
                break
        grids = [] # 用于保存有效节点
        for x in sub_xs: # 从子序列中筛选落在面片投影内
            for y in sub_ys: # 的有效网格节点
                if self.pointInTriangle(Point3D(x, y), tri): # 判断点在三角形
                    grids.append((x, y)) # 每个网格节点为(x, y)元组
        return grids

    def calcModelSptPoints(self): # 定义计算模型支撑点函数
        xs, ys, gridDic = self.initGrids() # 初始化网格，返回网格字典
        for tri in self.stlModel.triangles: # 遍历STL 模型中每个三角面片
            validGrids = self.getValidGrids(tri, xs, ys) # 获取当前面片有效网格节点
            for vg in validGrids: # 遍历每个有效节点
                ln = Line(Point3D(vg[0], vg[1]), Vector3D(0, 0, 1)) # 构造过节点竖线
                pln = Plane(tri.A, tri.N) # 构造三角面片所在平面
                pt = intersect(ln, pln) # 线面求交，    
                if pt is not None: # 如果pt 不为空
                    z = round(pt.z, self.digit) # 获取交点z 坐标
                    a = self.getFacetAngle(tri) # 获取面片倾角a
                    gridDic[vg].append((z, a)) # 构造(z, a)，并将其添加至字典
        for k in gridDic: # 遍历字典
            gridDic[k].sort(key = lambda t : t[0]) # 对每组交点按z 值从小到大排序
        return gridDic # 返回网格节点
    def getFacetAngle(self, tri): # 定义计算面片倾角函数
        angle = tri.N.getAngle(Vector3D(0, 0, 1)) # 角度单位为度
        angle = round(angle, self.digit) # 角度保留指定小数位数
        return (math.pi - angle) if angle > math.pi/2 else angle # 保证倾角

    def calcLayerSptPoints(self, gridDic, z): # 定义计算切片支撑点函数
        pts = [] # 定义切片支撑点序列
        for key in gridDic.keys(): # 遍历网格字典
            zas = gridDic[key] # 获取指定网格上的交点序列
            if self.hasSptPoint(zas, z): # 如果网格节点上有切片支撑点
                pts.append(Point3D(key[0], key[1], z)) # 则构造支撑点并存储在pts 中
        return pts # 返回切片支撑点序列
    def hasSptPoint(self, zas, z): # 判断网格上是否有切片支撑点
        for i in range(0, len(zas), 2): # 逐对遍历序列中相邻交点
            if i + 1 <= len(zas) - 1: # 保证数组索引不越界
                za0, za1 = zas[i], zas[i+1]
                if za1[1] < self.crAngle and z >= za0[0] and z<= za1[0]: # 如果满足式
                    return True # (10-3)、(10-4)条件，则返回True
        return False # 否则返    

    def genRawSptRegions(self, pts): # 支撑点转化为初始支撑区域函数
        rects = [] # 支撑点影响范围矩形序列
        for pt in pts: # 逐个将支撑点转化为矩形
            rects.append(self.pointToRect(pt, 1.1*self.gridSize, 1.1*self.gridSize))
        clipper, ca = Pyclipper(), ClipperAdaptor() # 裁剪对象clipper，适配器对象ca
        clipper.AddPaths(ca.toPaths(rects), PT_SUBJECT) # 逐个将矩形添加至clipper
        sln = clipper.Execute(CT_UNION, PFT_POSITIVE) # 执行布尔并运算
        return ca.toPolys(sln, pts[0].z) # 返回布尔并运算后区域
    def pointToRect(self, pt, lx, ly): # 定义将点转化为平面矩形函数
        vx, vy = Vector3D(lx/2, 0), Vector3D(0, ly/2) # 矩形沿X、Y 方向半边向量
        rect = Polyline() # 定义一个矩形，实为多边形
        rect.addPoint(pt - vx - vy) # 根据矩形中心点和半边向量
        rect.addPoint(pt + vx - vy) # 逐个添加矩形各个顶点
        rect.addPoint(pt + vx + vy)
        rect.addPoint(pt - vx + vy)
        rect.addPoint(pt - vx - vy)
        return rect

    def genSptRegions(self, pts, layer): # 定义支撑区域生成函数
        rawRegions = self.genRawSptRegions(pts) # 根据支撑点生成初始支撑区域
        clipper, ca = Pyclipper(), ClipperAdaptor() # 定义裁剪及适配器对象
        contours = ca.offsetPolygons(layer.contours, self.xyGap) # 生成模型轮廓的偏置轮廓
        clipper.AddPaths(ca.toPaths(rawRegions), PT_SUBJECT) # 裁剪对象，初始支撑区域
        clipper.AddPaths(ca.toPaths(contours), PT_CLIP) # 裁剪对象，偏置轮廓
        sln = clipper.Execute(CT_DIFFERENCE) # 执行布尔减操作
        return ca.toPolys(sln, layer.z) # 返回修正后的支撑区域
    def execute(self): # 实现类的核心流程控制函数
        gridDic = self.calcModelSptPoints() # 生成模型支撑点
        for layer in self.layers: # 遍历模型切片数据
            layer.sptContours = [] # 在每个切片上定义支撑轮廓序列
            pts = self.calcLayerSptPoints(gridDic, layer.z) # 计算切片支撑点
            if len(pts) > 0: # 如果支撑点数不为0，
                layer.sptContours = self.genSptRegions(pts, layer) # 则生成支撑轮廓
def findSptRegion(stlModel, layers, gridSize, crAngle, xyGap = 1): # 定义支撑生成全局函数
    FindSptRegion(stlModel, layers, gridSize, crAngle, xyGap).execute()


if __name__ == '__main__': # 定义main 函数
    src, stlModel = vtk.vtkSTLReader(), StlModel()
    src.SetFileName("E:\\3dp.stl") # 读取monk.stl 文件
    stlModel.extractFromVtkStlReader(src) # 提取VTK 数据源
    layers = readSlcFile("D:\\3dp at 2.0mm.slc") # 读取相应切片文件
    findSptRegion(stlModel, layers, 2, degToRad(60), 1) # 寻找支撑区域
    va = VtkAdaptor() # 调用VTK 显示计算结果
    # va.drawPdSrc(src).GetProperty().SetOpacity(0.5) # 按需显示STL 模型
    for i, layer in enumerate(layers): # 遍历得到的切片序列
        # if i != 22: continue # 按需只显示指定层上轮廓
        for poly in layer.contours: # 显示当前层模型轮廓
            va.drawPolyline(poly).GetProperty().SetColor(0, 0, 0) # 轮廓显示为黑色
        for poly in layer.sptContours: # 显示当前层支撑轮廓
            va.drawPolyline(poly).GetProperty().SetColor(0, 0, 1) # 轮廓显示为蓝色
    va.display()
