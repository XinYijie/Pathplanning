from VtkAdaptor import *
from SliceAlgo import *
from GenCpPath import *
from GenHatch import *
import StlModel

if __name__ == '__main__':
    vtkAdaptor = VtkAdaptor()
    vtkstlReader = vtk.vtkSTLReader()
    vtkstlReader.SetFileName('./model/monkg.stl')
    vtkAdaptor.drawPdSrc(vtkstlReader).GetProperty().SetOpacity(0.5)
    stlModel = StlModel.StlModel()
    stlModel.readStlFile('./model/monkg.stl')
    # layers=intersectStl_brutal(stlModel,10.0)
    interval = 0.4
    skinThickness = 2.0
    pathses = []
    layers = intersectStl_sweep(stlModel, 20)
    polyInner = []  #

    for layer in layers:
        layer.contours = linkSegs_dorder(layer.segments)
        # layer.contours=linkSegs_brutal(layer.segments)
        # for i in range(len(layer.contours)):
        #     segs = genSweepHatches([layer.contours[i]], 2, math.pi / 2)
        #     poly1 = Polyline.Polyline()
        #     for i, seg in enumerate(segs):
        #         poly1.addPoint(seg.A if (i % 2 == 0) else seg.B)
        #         poly1.addPoint(seg.B if (i % 2 == 0) else seg.A)
        #         poly1.endPoint().w = 1
        # # va.drawPolyline(poly).GetProperty().SetColor(0,0,0)
        #     vtkAdaptor.drawPolyline(poly1).GetProperty().SetColor(0, 0, 0)

        for contour in layer.contours:
            vtkAdaptor.drawPolyline(contour).GetProperty().SetLineWidth(2)

    for i in range(len(layers)):
        paths = genCpPath(layers[i].contours, interval, skinThickness)
        polyInner.append(paths[len(paths) - 1])  # 内轮廓
        pathses.append(paths)

    for paths in pathses:
        for path in paths:
            for ph in path:
                vtkAdaptor.drawPolyline(ph).GetProperty().SetColor(1, 0, 0)

    for i, polyIn in enumerate(polyInner):
        if i % 2 == 0:
            for poly in polyIn:
                segs = genSweepHatches([poly], 2, math.pi / 2)
                poly1 = Polyline.Polyline()
                for i, seg in enumerate(segs):
                    poly1.addPoint(seg.A if (i % 2 == 0) else seg.B)
                    poly1.addPoint(seg.B if (i % 2 == 0) else seg.A)
                    poly1.endPoint().w = 1
                vtkAdaptor.drawPolyline(poly1).GetProperty().SetColor(1, 0, 0)
        else:
            for poly in polyIn:
                segs = genSweepHatches([poly], 2, 0)
                poly1 = Polyline.Polyline()
                for i, seg in enumerate(segs):
                    poly1.addPoint(seg.A if (i % 2 == 0) else seg.B)
                    poly1.addPoint(seg.B if (i % 2 == 0) else seg.A)
                    poly1.endPoint().w = 1
                # va.drawPolyline(poly).GetProperty().SetColor(0,0,0)
                vtkAdaptor.drawPolyline(poly1).GetProperty().SetColor(1, 0, 0)

    vtkAdaptor.display()

    vtkAdaptor.display()
