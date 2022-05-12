from GenDpPath import *  # 导入GenDpPath 模块  平行填充路径
import time
from Utility import *

interval = 3  # 设置填充路径间距
angle = 0  # 设置填充角度，单位：度
pathses = []  # 存放各切片层平行路径
layers = readSlcFile("./model/ironman at 1.0mm.slc")  # 读取SLC 文件
start = time.perf_counter()  # .clock() # 计时开始
for i in range(len(layers)):  # 遍历各切片层轮廓
    print('dp, layer: %d / %d' % (i + 1, len(layers)))  # 打印当前切片层信息
    theta = degToRad(angle) if (i % 2 == 1) else degToRad(angle + 90)  # 正交填充角度
    paths = genDpPath(layers[i].contours, interval, theta)  # 生成平行路径
    pathses.append(paths)
end = time.perf_counter()  # .clock() # 计时结束
print("GenDpPath time: %f CPU seconds" % (end - start))  # 打印平行路径生成所需时间
va = VtkAdaptor()  # 调用VTK 绘图
for layer in layers:  # 绘制切片轮廓，黑色
    for contour in layer.contours:
        va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
for paths in pathses:  # 绘制平行填充路径，红色
    for path in paths:
        va.drawPolyline(path).GetProperty().SetColor(1, 0, 0)
va.display()
