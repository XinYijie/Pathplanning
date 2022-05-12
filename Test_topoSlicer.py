from SliceAlgo import * # 导入SliceAlgo 库
import time
src = vtk.vtkSTLReader() # 通过VTK 库加载STL 模型
src.SetFileName("E:\\3dp.stl")
stlModel = StlModel()
stlModel.extractFromVtkStlReader(src)
layerThicknesses = [1.0, 0.5, 0.2, 0.1, 0.05]
for layerThickness in layerThicknesses: # 循环，一次性完成2 种方法、5 种层高切片
    print('layerThickness:', layerThickness) # 打印当前层高
    start = time.perf_counter()
    layers1 = slice_topo(stlModel, layerThickness) # 对拓扑切片计时
    end = time.perf_counter()
    print("slice_topo: %f CPU seconds" % (end - start))
    start = time.perf_counter()
    # layers2 = slice_combine(stlModel, layerThickness) # 对组合切片计时
    # end = time.perf_counter()
    # print("slice_combine: %f CPU seconds" % (end - start))