import vtk # 导入vtk 库，字母均为小写
source = vtk.vtkCubeSource() # 创建一个长方体源，默认边长为1,1,1
mapper = vtk.vtkPolyDataMapper() # 创建mapper
mapper.SetInputConnection(source.GetOutputPort()) # 设置mapper 数据源
actor = vtk.vtkActor() # 创建actor
actor.SetMapper(mapper) # 设置actor 数据源
actor.GetProperty().SetColor(0.7, 0.7, 0.7) # 设置actor 显示颜色
renderer = vtk.vtkRenderer() # 创建渲染器
renderer.AddActor(actor) # 将actor 添加到渲染器
renderer.SetBackground(0.9, 0.9, 0.9) # 设置渲染器背景颜色
window = vtk.vtkRenderWindow() # 创建渲染窗口
window.AddRenderer(renderer) # 将渲染器添加到渲染窗口
window.SetSize(900, 600) # 设置窗口尺寸，单位为像素
interactor = vtk.vtkRenderWindowInteractor() # 创建渲染窗口交互器
interactor.SetRenderWindow(window) # 提供鼠标、键盘和时钟事件的交互机制
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera()) # 设置交互方式
interactor.Initialize() # 初始化交互器
interactor.Start() # 窗口程序开始运行