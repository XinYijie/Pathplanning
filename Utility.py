
import math
def makeListLinear(lists):
    outList=[]
    _makeListLinear(lists,outList)
    return outList
def _makeListLinear(inList,outList):
    for a in inList:
        if type(a)!=list:
            outList.append(a)
        else:
            _makeListLinear(a,outList)

def degToRad(deg): # 角度转化为弧度
    return deg * math.pi / 180.0
def radToDeg(rad): # 弧度转化为角度
    return rad * 180.0 / math.pi