from pyclipper import *
from VtkAdaptor import *
from GemoBase import Point3D
from GenCpPath import *
import PolyPrcSeeker
import Polyline


def tuplesToPoly(tuples):
    poly = Polyline.Polyline()
    for pt in tuples:
        poly.addPoint(Point3D(pt[0], pt[1], 0))
    poly.addPoint(poly.startPoint())
    return poly


if __name__ == '__main__':
    # subject=[(0,0),(100,0),(100,70),(0,70)]
    # clip=[(30,50),(70,50),(70,100),(30,100)]
    # clipper=Pyclipper()
    # clipper.AddPath(subject,PT_SUBJECT,True)
    # clipper.AddPath(clip,PT_CLIP,True)
    # sln=clipper.Execute(CT_UNION,PET_NEGITIVE)
    polys = []
    outerPoly = [(0, 0), (100, 0), (100, 100), (0, 100)]
    innerPoly = [(30, 30), (30, 70), (70, 70), (70, 30)]
    innerPoly1 = [(40, 40), (40, 60), (60, 60), (60, 40)]
    poly2 = tuplesToPoly(innerPoly)
    poly1 = tuplesToPoly(outerPoly)
    poly3 = tuplesToPoly(innerPoly1)
    polys.append(poly1)
    polys.append(poly2)
    polys.append(poly3)
    poly1s = PolyPrcSeeker.seekPolyPrc(polys)
    parents = []
    for poly3 in poly1s:
        parent = poly3.parent
        if parent is not None:
            newPoly = linktoParent(poly3)
            parent.points = newPoly.points
            parents.append(parent)
    # pco=PyclipperOffset()
    # pco.AddPath(outerPoly,JT_SQUARE,ET_CLOSEDPOLYGON)
    # pco.AddPath(innerPoly,JT_SQUARE,ET_CLOSEDPOLYGON)
    # sln=pco.Execute(-10)
    vtkAdaptor = VtkAdaptor()

    for parent1 in parents:
        vtkAdaptor.drawPolyline(parent1).GetProperty().SetColor(0, 0, 0)
    # for poly in polys:
    #     vtkAdaptor.drawPolyline(poly).GetProperty().SetColor(0, 0, 0)
    # for tuples in sln:
    #     poly=tuplesToPoly(tuples)
    #     vtkAdaptor.drawPolyline(poly).GetProperty().SetColor(0,0,0)
    # poly1=tuplesToPoly(outerPoly)
    # vtkAdaptor.drawPolyline(poly1).GetProperty().SetColor(0, 0, 0)
    # poly2 = tuplesToPoly(innerPoly)
    # vtkAdaptor.drawPolyline(poly2).GetProperty().SetColor(0, 0, 0)
    vtkAdaptor.display()
