from Utility import *
from IdEndLayers import *
from GenCpPath import *
from GenDpPath import *


class PrintParams:
    def __init__(self, stlModel, ffFlag=1, sfFlag=0):
        self.stlModel = stlModel
        # self.layerThk, self.shellThk, self.endThk = 0.2, 2.0, 2.0
        self.layerThk, self.shellThk, self.endThk = 0.2, 2.0, 2.0
        self.sfRate, self.fillAngle = 0.2, 0.0
        self.sptOn = False
        self.sptCrAngle = degToRad(60.0)
        self.sptGridSize = 2.0
        self.sptSfRate, self.sptFillAngle = 0.15, 0.0
        # self.sptFillType = SptFillType.cross
        self.sptXyGap = 1.0
        self.g0Speed, self.g1Speed = 5000, 1000
        self.startCode = " ; Start code...\n"
        self.endCode = " ; End code...\n"
        self.nozzleSize, self.filamentSize = 0.5, 1.75
        self.ffFlag = ffFlag
        self.sfFlag = sfFlag


def genAllPaths(pp: PrintParams):
    sfInvl = pp.nozzleSize / pp.sfRate
    # sptSfInvl = pp.nozzleSize / pp.sptSfRate
    layers = slice_topo(pp.stlModel, pp.layerThk)
    # for layer in layers:  # 重要：调整每层轮廓方向
    #     adjustPolygonDirs(layer.contours)
    idEndLayers(layers, pp.shellThk, int(pp.endThk / pp.layerThk) + 1)
    for i, layer in enumerate(layers):
        layer.cpPaths, layer.ffPaths, layer.sfPaths = [], [], []
        layer.cpPaths = genCpPath(layer.contours, pp.nozzleSize, pp.shellThk, 'path')
        delta = 0 if i % 2 == 0 else math.pi / 2
        if pp.ffFlag == 1:
            layer.ffPaths = genDpPath(layer.contours, pp.nozzleSize, pp.fillAngle + delta)
        elif pp.sfFlag == 1:
            layer.sfPaths = genDpPath(layer.contours, sfInvl, pp.fillAngle + delta)
    # if pp.sptOn:
    #     genSptPath(pp.stlModel, layers, sptSfInvl, pp.sptGridSize, pp.sptCrAngle, \
    #         pp.sptFillType, pp.sptFillAngle, pp.sptXyGap)
    return layers


def pathToCode(path, pp, e, nf2):
    code = ""
    for i, p in enumerate(path.points):
        print(i, p)
        if i == 0:
            code += "G0 F%d X%.3f Y%.3f Z%.3f\n" % (pp.g0Speed, p.x, p.y, p.z)
        else:
            e += p.distance(path.points[i - 1]) * nf2
            code += "G1 F%d X%.3f Y%.3f Z%.3f E%.3f\n" % (pp.g1Speed, p.x, p.y, p.z, e)
    return code, e


def postProceess(layers, pp):
    # print(layers)
    code, e = pp.startCode, 0
    nf2 = (pp.nozzleSize / pp.filamentSize) ** 2
    for i, layer in enumerate(layers):
        code += "; Layer %d\n" % i
        # for path in layer.sptCpPaths: code += pathToCode(path, pp, e, nf2)
        # for path in layer.sptDpPaths: code += pathToCode(path, pp, e, nf2) #支撑
        for path in layer.cpPaths:
            if path == []:
                continue
            code_tmp, e = pathToCode(path[0], pp, e, nf2)
            code += code_tmp
        for path in layer.ffPaths:
            if path == []:
                continue
            code_tmp, e = pathToCode(path, pp, e, nf2)
            code += code_tmp
        for path in layer.sfPaths:
            if path == []:
                continue
            code_tmp, e = pathToCode(path, pp, e, nf2)
            code += code_tmp
    return code + pp.endCode


def genNcCode(pp: PrintParams):
    layers = genAllPaths(pp)
    nccode = postProceess(layers, pp)
    return nccode
