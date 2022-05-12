from VtkAdaptor import * # 导入VtkAdaptor 模块
if __name__ == '__main__': # 测试main 函数入口
    vtkAdaptor = VtkAdaptor() # 首先创建VtkAdaptor 对象，必不可少
    vtkAdaptor.setBackgroundColor(0.95, 0.95, 0.95) # 设置场景背景颜色
    vtkAdaptor.drawAxes() # 绘制坐标轴
    vtkAdaptor.drawPoint(Point3D(10, 10, 10)).GetProperty().SetColor(1, 0, 0) # 绘制点，设置颜色
    vtkAdaptor.drawPoint(Point3D(50, 50, 50)).GetProperty().SetColor(1, 0, 0)
    polyline = Polyline() # 创建多段线对象
    polyline.addPoint(Point3D(1,1,1)) # 在多段线中添加点
    polyline.addPoint(Point3D(50, 2, 10))
    polyline.addPoint(Point3D(20, 10, 30))
    polyline.addPoint(Point3D(50, 80, 55))
    polylineActor = vtkAdaptor.drawPolyline(polyline) # 绘制多段线
    polylineActor.GetProperty().SetColor(0.1, 0.7, 0.7) # 设置多段线颜色
    polylineActor.GetProperty().SetLineWidth(2) # 设置多段线线宽
    stlActor = vtkAdaptor.drawStlModel("E:\\3DP.STL") # 根据文件路径绘制STL 模型
    stlActor.SetPosition(0, 150, 150) # 设置模型位置
    vtkAdaptor.display() # 调用display 函数，这一步必不可少