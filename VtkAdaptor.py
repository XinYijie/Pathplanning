import vtk
from Segment import *
from Polyline import *
from Triangle import *
class VtkAdaptor:
    def __init__(self,bgClr=(0.95,0.95,0.95)):
        self.renderer=vtk.vtkRenderer()
        self.renderer.SetBackground(bgClr)
        self.window=vtk.vtkRenderWindow()
        self.window.AddRenderer(self.renderer)
        self.window.SetSize(1000,1000)
        self.interactor=vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()
    def display(self):             #显示函数
        self.interactor.Start()
    def setBackgroundColor(self,r,g,b):
        return self.renderer.SetBackground(r,g,b)
    def drawActor(self,actor):       #绘制actor对象
        self.renderer.AddActor(actor)
        return actor
    def drawPdSrc(self,pdSrc):             #绘制PolyData类型的source
        mapper=vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(pdSrc.GetOutputPort())
        actor=vtk.vtkActor()
        actor.SetMapper(mapper)
        return self.drawActor(actor)
    def drawStlModel(self,stlFilePath):          #绘制stl模型
        reader=vtk.vtkSTLReader()
        reader.SetFileName(stlFilePath)
        return self.drawPdSrc(reader)
    def drawAxes(self,length=100.0,shaftType=0,cylinderRadius=0.01,coneRadius=0.2):
        axes=vtk.vtkAxesActor()
        axes.SetTotalLength(length,length,length)
        axes.SetShaftType(shaftType)
        axes.SetCylinderRadius(cylinderRadius)
        axes.SetConeRadius(coneRadius)
        axes.SetAxisLabels(0)
        self.renderer.AddActor(axes)
        return axes

    def removeActor(self,actor):
        self.renderer.RemoveActor(actor)

    def drawPoint(self, point, radius = 2.0): # 绘制一个点，Point3D
        src = vtk.vtkSphereSource()
        src.SetCenter(point.x, point.y, point.z)
        src.SetRadius(radius)
        return self.drawPdSrc(src)

    def drawSegment(self,seg):
        src=vtk.vtkLineSource()
        src.SetPoint1(seg.A.x,seg.A.y,seg.A.z)
        src.SetPoint2(seg.B.x,seg.B.y,seg.B.z)
        return self.drawPdSrc(src)
    def drawPolyline(self,polyline):
        src = vtk.vtkLineSource()
        points=vtk.vtkPoints()
        for i in range(polyline.count()):
            pt=polyline.point(i)
            points.InsertNextPoint((pt.x,pt.y,pt.z))
        src.SetPoints(points)
        return self.drawPdSrc(src)
    def drawTriangle(self,tri):
        colors = vtk.vtkNamedColors()

        # Create a triangle
        points = vtk.vtkPoints()
        points.InsertNextPoint(tri.A.x, tri.A.y, tri.A.z)
        points.InsertNextPoint(tri.B.x, tri.B.y,tri.B.z)
        points.InsertNextPoint(tri.C.x, tri.C.y,tri.C.z)

        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, 0)
        triangle.GetPointIds().SetId(1, 1)
        triangle.GetPointIds().SetId(2, 2)

        triangles = vtk.vtkCellArray()
        triangles.InsertNextCell(triangle)

        # Create a polydata object
        trianglePolyData = vtk.vtkPolyData()

        # Add the geometry and topology to the polydata
        trianglePolyData.SetPoints(points)
        trianglePolyData.SetPolys(triangles)

        # Create mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(trianglePolyData)
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(colors.GetColor3d("Cyan"))
        actor.SetMapper(mapper)
        return self.drawActor(actor)

        # Create a renderer, render window, and an interactor




    