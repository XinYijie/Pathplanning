import vtk  # 导入vtk 库

renderer = vtk.vtkRenderer()  # 创建三维场景
renderer.SetBackground(0.95, 0.95, 0.95)
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(900, 600)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
interactor.Initialize()
stlReader = vtk.vtkSTLReader()  # 从文件加载STL 模型数据源
stlReader.SetFileName("./model/ironman.stl")
filter = vtk.vtkOutlineFilter()  # 创建模型边框显示filter-mapper-actor
filter.SetInputConnection(stlReader.GetOutputPort())
outLineMapper = vtk.vtkPolyDataMapper()
outLineMapper.SetInputConnection(filter.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outLineMapper)
outlineActor.GetProperty().SetColor(0.1, 0.1, 0.1)
renderer.AddActor(outlineActor)
stlMapper = vtk.vtkPolyDataMapper()  # 创建模型显示mapper-actor
stlMapper.SetInputConnection(stlReader.GetOutputPort())
stlActor = vtk.vtkActor()
stlActor.SetMapper(stlMapper)
renderer.AddActor(stlActor)
interactor.Start()  # 运行程序
