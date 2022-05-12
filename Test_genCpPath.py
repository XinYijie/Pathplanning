from GenCpPath import *  # 导入GenCpPath 库  轮廓填充路径
from SliceAlgo import *
import time
from Layer import *

interval = 0.4  # 轮廓路径间距
skinThickness = 2.0  # 表皮厚度，即轮廓路径总宽度
pathses = []  # 存储各层已连接的路径
layers = readSlcFile("./model/cylinder at 0.5mm.slc")  # 读取SLC 文件
start = time.perf_counter()  # .clock() # 计时开始
for i in range(len(layers)):  # 逐层生成轮廓填充路径
    print('cp, layer: %d / %d' % (i + 1, len(layers)))
    paths = genCpPath(layers[i].contours, interval, skinThickness, 'path')
    pathses.append(paths)
# print(pathses)
end = time.perf_counter()  # .clock() # 计时结束
print("GenCpPath time: %f CPU seconds" % (end - start))  # 打印路径生成时间
va = VtkAdaptor()  # 显示，使用VTK 库
for layer in layers:  # 显示每层打印区域边界，黑色
    for contour in layer.contours:
        va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
for paths in pathses:  # 显示每层路径，红色
    for path1 in paths:
        for path in path1:
            va.drawPolyline(path).GetProperty().SetColor(1, 0, 0)
va.display()
