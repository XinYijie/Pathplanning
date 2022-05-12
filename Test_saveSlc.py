# from VtkAdaptor import *
# from GenCpPath import *
# from GenHatch import *
# from SliceAlgo import * # 导入 SliceAlgo模块
# import StlModel


# vtkAdaptor=VtkAdaptor()
# vtkstlReader=vtk.vtkSTLReader()
# vtkstlReader.SetFileName('e:/3dp.stl')
# vtkAdaptor.drawPdSrc(vtkstlReader).GetProperty().SetOpacity(0.5)
# stlModel = StlModel.StlModel()
# stlModel.readStlFile('e:/3dp.stl')
# layers = intersectStl_sweep(stlModel, 20)

# modelName = "3dp" # 指定 STL模型文件名
# layerThickness = 2.0 # 指定切片层厚 2.0, 1.0, 0.5, 0.2mm 
# # src = vtk.vtkSTLReader() # 通过 VTK加载 STL模型
# # src.SetFileName("e:/3dp.stl") 
# # stlModel = StlModel()
# stlModel.extractFromVtkStlReader(stlModel) 
# layers = slice_topo(stlModel, layerThickness) # 使用拓扑切片获取每层轮廓数据
# for layer in layers: # 重要： 调整 每层轮廓方向
#     adjustPolygonDirs(layer.contours) 
# writeSlcFile(layers, "D:/qq/%s at %smm.slc" % (modelName, layerThickness)) # 写 SLC文件
# print("SLC file has been generated and saved")

from SliceAlgo import * # 导入SliceAlgo 模块
from StlModel import *
modelName = "cube" # 指定STL 模型文件名
layerThickness = 0.2 # 指定切片层厚：2.0, 1.0, 0.5, 0.2mm
src = vtk.vtkSTLReader() # 通过VTK 加载STL 模型
src.SetFileName("./model/%s.stl" % modelName)
stlModel = StlModel()
stlModel.extractFromVtkStlReader(src)
layers = slice_topo(stlModel, layerThickness) # 使用拓扑切片获取每层轮廓数据
for layer in layers: # 重要：调整每层轮廓方向
    adjustPolygonDirs(layer.contours)
writeSlcFile(layers, "./model/%s at %smm.slc" % (modelName, layerThickness))
print("SLC file has been generated and saved")
