from GemoBase import *
class Polyline:
    def __init__(self):
        self.points=[]
    def __str__(self):
        if self.count()>0:
            return "Polyline\nPoint number:%s\nStart:%s\nEnd:%s\n"%(self.count(),str(self.startPoint()),str(self.endPoint()))
        else:return "Polyline\nPoint number:0\n"
    def clone(self):
        poly=Polyline()
        for pt in self.points:
            poly.addPoint(pt.clone())
        return poly
    def count(self):
        return len(self.points)
    def addPoint(self,pt):
        self.points.append(pt)
    def addTuple(self,tuple):
        self.points.append(Point3D(tuple[0],tuple[1],tuple[2]))
    def raddPoint(self,pt):
        self.points.insert(0,pt)
    def removePoint(self,index):
        return self.points.pop(index)
    def point(self,index):
        return self.points[index]
    # def getPoint(self,index):
    #     return self.points[index]
    def startPoint(self):
        return self.points[0]
    def endPoint(self):
        return self.points[-1]
    def isClosed(self):    #判断线段是否闭合
        if self.count()<=2:return False
        else:return self.startPoint().isCoincide(self.endPoint())
    def reverse(self):   #对多段线的点序进行反向操作
        sz=self.count()
        for i in range(int(sz/2)):
            self.points[i],self.points[sz-1-i]=self.points[sz-1-i],self.points[i]
    def getArea(self):    #当多段线在平面上闭合时  ，求封闭区域面积
        area=0.0
        for i in range(self.count()-1):
            area+=0.5*(self.points[i].x*self.points[i+1].y-self.points[i+1].x*self.points[i].y)
        return area
    def makeCCW(self):  #将多边形调整成逆时针方向
        if self.getArea()<0:self.reverse()
    def makeCW(self):
        if self.getArea()>0:self.reverse()
    def isCCW(self):  #判断多边形是否问逆时针方向
        if self.getArea()>0:return True
        else:return False
    def translate(self,vec):    #根据向量平移多段线
        for i in range(len(self.points)):
            self.points[i].translate(vec)
    def appendSegment(self,seg):    #在多段线的开头和结尾添加一条线段
        if self.count()==0:
            self.points.append(seg.A)
            self.points.append(seg.B)
        else:
            if seg.A.isCoincide(self.endPoint()):self.addPoint(seg.B)
            elif seg.B.isCoincide(self.endPoint()):self.addPoint(seg.A)
            elif seg.A.isCoincide(self.startPoint()):self.raddPoint(seg.B)
            elif seg.B.isCoincide(self.startPoint()):self.raddPoint(seg.A)
            else:return False
        return True
    def multiply(self,m):   #对对象本身变换，作用一个矩阵m
        for pt in self.points:
            pt.multiply(m)
    def multiplied(self,m):    #作用矩阵m，产生一个新的多段线对象
        poly=Polyline()
        for pt in self.points:
            poly.addPoint(pt*m)
        return poly

def writePoluline(path,polyline:Polyline):     #将多段线保存到文本文件
    f=None
    try:
        f=open(path,'w')
        f.write('%s\n'%polyline.count())
        for pt in polyline.points:
            txt='%s,%s,%s\n'%(pt.x,pt.y,pt.z)
            f.write(txt)
    except Exception as ex:
        print(ex)
    finally:
        if f:f.close()

def readPolyline(path):
    f =None
    try:
        f=open(path,'r')
        poly=Polyline()
        number=int(f.readline())
        for i in range(number):
            txt=f.readline()
            txts=txt.split(',')
            x,y,z=float(txts[0]),float(txts[1]),float(txts[2])
            poly.addPoint(Point3D(x,y,z))
        return poly
    except Exception as ex:
        print(ex)
    finally:
        if f:f.close()



