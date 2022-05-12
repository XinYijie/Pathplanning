from GemoBase import *
from Line import *
class Plane:
    def __init__(self,P,N):    #P为平面经过的一点，N为平面法向量
        self.P=P.clone()
        self.N=N.clone().normalized()
    def __str__(self):
        return "Plane\n%s\n%s\n"%(str(self.P),str(self.N))
    def toFormula(self):   #获取标准直线方程Ax+By+Cz+D=0中参数A、B、C、D的值
        A,B,C=self.N.dx,self.N.dy,self.N.dz
        D=-self.N.dx*self.P.x-self.N.dy*self.P.y-self.N.dz*self.P.z
        return A,B,C,D
    @staticmethod
    def zPlane(z):     #静态函数，返回一个Z平面
        return Plane(Point3D(0,0,z),Vector3D(0,0,1.0))
    def intersect(self,other):
        dir=self.N.crossProduct(other.N)
        if dir.isZeroVector():
            return None
        else:
            x,y,z=0,0,0
            A1,B1,C1,D1=self.toFormula()
            A2,B2,C2,D2=other.toFormula()
            if B2*C1-B1*C2 !=0:
                y=-(-C2*D1+C1*D2)/(B2*C1-B1*C2)
                z=-(B2*D1-B1*D2)/(B2*C1-B1*C2)
            elif A2*C1-A1*C2 !=0:
                x=-(-C2*D1+C1*D2)/(A2*C1-A1*C2)
                z=-(A2*D1-A1*D2)/(A2*C1-A1*C2)
            elif A2*B1-A1*B2 !=0:
                x=-(-B2*D1+B1*D2)/(A2*B1-A1*B2)
                y=-(A2*D1-A1*D2)/(A2*B1-A1*B2)
            else:
                return None
            return Line(Point3D(x,y,z),dir.normalized())

