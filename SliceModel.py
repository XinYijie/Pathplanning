import SliceAlgo # 导入SliceAlgo 模块
from VtkAdaptor import *
from StlModel import *
import Layer
class SliceModel:
    def __init__(self, stlModel, layerThickness, sliceAlgo = "brutal"): # 初始化函数，输入模型、
        self.stlModel = stlModel # 层高以及切片方式
        self.layerThickness = layerThickness
        if sliceAlgo == 'brutal': self.slice_brutal()
        elif sliceAlgo == 'optimal': self.slice_smart()
    def slice_brutal(self): # 切片函数，brutal
        self.layers = SliceAlgo.intersectStl_brutal(self.stlModel, self.layerThickness)
        for layer in self.layers:
            layer.contours = SliceAlgo.linkSegs_brutal(layer.segments)
            SliceAlgo.adjustPolygonDirs(layer.contours)
    def slice_optimal(self): # 切片函数，优化，暂时未实现
        pass
    def writeSlcFile(self, path): # 写SLC 文件
        SliceAlgo.writeSlcFile(self.layers, path)
    def readSlcFile(self, path): # 读SLC 文件
        self.layers = SliceAlgo.readSlcFile(path)
    def drawLayerContours(self, va, start = 0, stop = 0xFFFF, step = 1, clr = (0, 0, 0), lineWidth = 1):
        for i in range(max(0, start), min(stop, len(self.layers)), step): # 在VTK 中绘制切片轮廓
            layer = self.layers[i]
            for contour in layer.contours:
                contourActor = va.drawPolyline(contour)
                contourActor.GetProperty().SetColor(clr)
                contourActor.GetProperty().SetLineWidth(lineWidth)        

if __name__ == '__main__': # SliceModel 类测试main 函数
    vtkAdaptor = VtkAdaptor()
    stlModel = StlModel()
    stlModel.readStlFile("E:\\3DP.STL") # 读取STL 文件
    sliceModel = SliceModel(stlModel, 0.7) # 建立切片模型，输入层高0.7mm
    sliceModel.drawLayerContours(vtkAdaptor) # 绘制切片轮廓
    vtkAdaptor.display()
