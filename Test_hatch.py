from VtkAdaptor import *
from ClipperAdaptor import *
import ClipperAdaptor
# import vtk
import math
from GenHatch import *

if __name__ == '__main__':
    va = VtkAdaptor()
    path = [(0, 0), (100, 0), (100, 100), (50, 60), (0, 100)]
    poly = ClipperAdaptor.ClipperAdaptor(0).PathToPoly(path)
    # segs=genClipHatches([poly],6,math.pi/2)
    segs = genSweepHatches([poly], 6, math.pi / 2)
    poly1 = Polyline.Polyline()
    for i, seg in enumerate(segs):
        poly1.addPoint(seg.A if (i % 2 == 0) else seg.B)
        poly1.addPoint(seg.B if (i % 2 == 0) else seg.A)
        poly1.endPoint().w = 1
    va.drawPolyline(poly).GetProperty().SetColor(0, 0, 0)
    va.drawPolyline(poly1).GetProperty().SetColor(0, 0, 0)
    # for i in range(len(segs)):
    #     va.drawSegment(segs[i]).GetProperty().SetColor(1,0,0)
    #     textSrc=vtk.vtkVectorText()
    #     textSrc.SetText('%d'%i)
    #     textActor=va.drawPdSrc(textSrc)
    #     textActor.SetPosition(segs[i].B.x,segs[i].B.y,segs[i].B.z)
    #     textActor.SetScale(3)
    #     textActor.GetProperty().SetColor(0,0,0)
    va.display()


def linkLocalHatches(self, segs):
    poly = Polyline()
    for i, seg in enumerate(segs):
        poly.addPoint(seg.A if (i % 2 == 0) else seg.B)
        poly.addPoint(seg.B if (i % 2 == 0) else seg.A)
        poly.endPoint().w = 1
    return poly
