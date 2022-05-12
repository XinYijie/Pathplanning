from ClipperAdaptor import *
import pyclipper
from StlModel import *
from SliceAlgo import *
from GemoBase import *
from VtkAdaptor import *


def pickFfRegions(layer1, layer2, shellThk):
    c1, c2 = layer1.contours, layer2.contours
    ca = ClipperAdaptor()
    c2oi = ca.offsetPolygons(c2, -shellThk)
    if len(c2oi) == 0: return False
    layer2.shellContours = c2oi
    e = ca.clip(c2oi, c1, pyclipper.CT_DIFFERENCE) if len(c1) > 0 else c2oi
    if len(e) == 0: return False
    d = ca.clip(c2, c1, pyclipper.CT_DIFFERENCE) if len(c1) > 0 else c2
    doo = ca.offsetPolygons(d, shellThk)
    f = ca.clip(doo, c2oi, pyclipper.CT_INTERSECTION, c2[0].point(0).z)
    layer2.ffContours = f
    return True


def splitFfRegions(layers, shellThk, endLayerNum):
    layers.insert(0, Layer(0))
    i, j = 0, 1
    while True:
        if j > len(layers) - 1:
            break
        while pickFfRegions(layers[i], layers[j], shellThk):
            j = j + 1
            if j > len(layers) - 1 or j - i > endLayerNum:
                break
        i = i + 1 if j - i == 1 else j - 1
        j = i + 1
    del layers[0]


def splitSfRegions(layers):
    ca = pyclipper.ClipperAdaptor()
    for layer in layers:
        if len(layer.shellContours) > 0:
            if len(layer.ffContours) == 0:
                layer.sfContours = layer.shellContours
            else:
                s = ca.clip(layer.shellContours, layer.ffContours, pyclipper.CT_DIFFERENCE, layer.z)
                layer.sfContours = s


def idEndLayers(layers, shellThk, endLayerNum):
    splitFfRegions(layers, shellThk, endLayerNum)


if __name__ == '__main__':
    src, stlModel = vtk.vtkSTLReader(), StlModel()
    print('...')
    src.SetFileName("E:\\monk.stl")
    print('....')
    stlModel.extractFromVtkStlReader(src)
    print('.....')
    layerThk, shellThk, endThk = 0.5, 2.0, 3.0
    endLayerNum = int(endThk / layerThk) + 1
    layers = slice_topo(stlModel, layerThk)
    print('......')
    idEndLayers(layers, shellThk, endLayerNum)
    print('.......')
    va = VtkAdaptor()
    print('........')
    for layer in layers:
        print(0)
        for poly in layer.contours:
            print(1)
            va.drawPolyline(poly).GetProperty().SetColor(0, 0, 0)
        for poly in layer.ffContours:
            print(2)
            va.drawPolyline(poly).GetProperty().SetColor(1, 0, 0)
        for poly in layer.sfContours:
            print(3)
            va.drawPolyline(poly).GetProperty().SetColor(0, 1, 0)
    va.display()
