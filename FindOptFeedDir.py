from SliceAlgo import *
from Utility import *
def _findAnglePairs(polygons, adjustPolyDirs): # 定义凹顶点夹角对计算函数
    if adjustPolyDirs: # 如有必要，调整多边形方向
        adjustPolygonDirs(polygons) # 使其符合“外逆内顺”的规定
    anglePairs = [] # 用于保存夹角对列表
    for poly in polygons: # 遍历多边形
        for i in range(poly.count()-1): # 遍历多边形顶点
            pts = poly.points
            v1 = pts[-2 if (i==0) else (i-1)].pointTo(pts[i]) # 当前顶点前边方向向量v1
            v2 = pts[i].pointTo(pts[i + 1]) # 当前顶点后面方向向量v2
            if v1.crossProduct(v2).dz < 0: # 判断当前顶点是否是凹顶点
                a = radToDeg(v1.getAngle2D()) # 向量v1 和X 轴夹角a，0~360 度
                b = radToDeg(v2.getAngle2D()) # 向量v2 和X 轴夹角b，0~360 度
                a, b = min(a, b), max(a, b) # 强制使：a < b
                anglePairs.append((a, b)) # 添加夹角对(a, b)到anglePairs
    return anglePairs

def _initAngleTable(digit): # 角度表构建函数，digit 为小数位数
    angleTable = {} # 角度字典
    delta = math.pow(10, -digit) # 角度增量
    angle = 0.0
    while angle < 180: # 在0~180 度范围内，创建字典键
        angleTable[angle] = 0 # 初始化每个角度下的交点数为0
        angle = round(angle + delta, digit) # 保证角度小数位数为指定值
    return angleTable # 返回角度表    

def findOptFeedDir(polygons, digit = 0, adjustPolyDirs = False): # 定义函数
    anglePairs = _findAnglePairs(polygons, adjustPolyDirs) # 获取凹顶点角度对列表
    angleTable = _initAngleTable(digit) # 获取扫描角度表（字典）
    delta = math.pow(10, -digit) # 扫描角度增量
    for a, b in anglePairs: # 遍历角度对，获取切线角度
        if b <= 180: # 情况1：[a, b]
            key = round(a + delta, digit) # 从切线角度上限开始
            while key <= round(b - delta, digit): # 遍历直至切线角度下限
                angleTable[key] += 1 # 当前角度上的交点个数累加1
                key = round(key + delta, digit) # 角度自增delta
        elif a >= 180: # 情况2：[a-180, b-180]
            key = round(a - 180 + delta, digit) # 同情况1
            while key <= round(b - 180 - delta, digit):
                angleTable[key] += 1
                key = round(key + delta, digit)
        elif a <= 180 and b >= 180: # 情况3：[0, a']∪[b', 180)
            b = b - 180 # 先对a、b 值进行调整
            a, b = min(a, b), max(a, b)
            key = round(delta, digit) # 前半段 [0, a']
            while key < a:
                angleTable[key] += 1
                key = round(key + delta, digit)
            key = round(b + delta, digit) # 后半段 [b', 180)
            while key < 180:
                angleTable[key] += 1
                key = round(key + delta, digit)
    return angleTable # 返回角度表