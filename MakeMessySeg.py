Segment import * # 导入Segment 模块
from random import * # 导入随机数生成模块
import math # 导入math 模块
def makeMessySegs(circleNum = 10, segNumPerCircle = 100000, radius = 100.0): # 函数定义
    segs = [] # 定义线段列表
    r = radius # 以半径递增的方式生成同心圆
    for i in range(circleNum): # 遍历，生成指定cirlceNum 个同心圆
        pnts = [] # 点列表，用于收集圆上的点
        for j in range(segNumPerCircle): # 按细分份数细分圆
            theta = j / segNumPerCircle * 2 * math.pi # 角度theta
            x = r * math.cos(theta) # 圆上点x、y 坐标，圆心在原点
            y = r * math.sin(theta)
            pnt = Point3D(x, y)
            pnts.append(pnt) # 将点添加到pnts
        pnts.append(pnts[0]) # 在pnts 添加起点，以封闭轮廓
        for j in range(len(pnts) - 1): # 将点依次整理为线段，添加至segs
            seg = Segment(pnts[j], pnts[j+1])
            segs.append(seg)
        r += 10.0 # 同心圆半径递增
    print('segment count:', len(segs)) # 打印segs 中线段总数
    print('min segment length:', segs[0].A.distance(segs[0].B)) # 打印segs 中最短的线段
    for i in range(len(segs)): # 对segs 中线段散乱化处理
        rd = randint(0, len(segs) - 1) # 生成一个随机序号
        segs[i], segs[rd] = segs[rd], segs[i] # 当前线段和随机序号线段交换
    return segs