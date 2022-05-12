from GemoBase import *
from Line import *
from  Segment import *
from  Plane import *
import Ray
import Polyline
def nearZero(x):     #判断是否接近0
    if math.fabs(x)<epsilon:
        return True
    return False
def distance(obj1,obj2):    #实体距离计算  未写完
    if isinstance(obj1,Point3D) and isinstance(obj2,Line): # 情况1：点和直线距离计算
        P,Q,V=obj2.P,obj1,obj2.V
        t=P.pointTo(Q).dotProduct(V)
        R=P+V.amplified(t)
        return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Ray): # 情况2：点和射线距离计算
        P, Q, V = obj2.P, obj1, obj2.V
        t = P.pointTo(Q).dotProduct(V)
        if t >= 0:
            R = P + V.amplified(t)
            return Q.distance(R)
        return Q.distance(P)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Segment): # 情况3、点和线段距离计算
        Q, P, P1, V = obj1, obj2.A, obj2.B, obj2.direction().normalized()
        L = obj2.length()
        t = P.pointTo(Q).dotProduct(V)
        if t <= 0:
            return Q.distance(P)
        elif t >= L:
            return Q.distance(P1)
        else:
            R = P + V.amplified(t)
            return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Plane): # 情况4、点和平面距离计算
        P, Q, N = obj2.P, obj1, obj2.N
        angle = N.getAngle(P.pointTo(Q))
        return P.distance(Q)*math.cos(angle)
    elif isinstance(obj1, Line) and isinstance(obj2, Line): # 情况5、直线和直线距离计算
        P1, V1, P2, V2 = obj1.P, obj1.V, obj2.P, obj2.V
        N = V1.crossProduct(V2)
        if N.isZeroVector():
            return distance(P1, obj2)
        return distance(P1, Plane(P2, N))
    elif isinstance(obj1, Line) and isinstance(obj2, Plane): # 情况6：直线和平面距离计算
        if obj1.V.dotProduct(obj2.N):
            return distance(obj1.P, obj2)# if obj1.V.dotProduct(obj2.N)==0
        return 0
    pass #其他情况
def intersectLineLine(line1:Line,line2:Line):
    P1,V1,P2,V2=line1.P,line1.V,line2.P,line2.V
    P1P2=P1.pointTo(P2)
    deno=V1.dy*V2.dx-V1.dx*V2.dy
    if deno !=0:
        t1=-(-P1P2.dy*V2.dx+P1P2.dx*V2.dy)/deno
        t2=-(-P1P2.dy*V1.dx+P1P2.dx*V1.dy)/deno
        return P1+V1.amplified(t1),t1,t2
    else:
        deno=V1.dz*V2.dy-V1.dy*V2.dz
        if deno !=0:
            t1=-(-P1P2.dz*V2.dy+P1P2.dy*V2.dz)/deno
            t2=-(-P1P2.dz*V1.dy+P1P2.dy*V1.dz)/deno
            return P1+V1.amplified(t1),t1,t2
    return None,0,0
def intersectSegmentPlane(seg:Segment,plane:Plane):
    A,B,P,N=seg.A,seg.B,plane.P,plane.N
    V=A.pointTo(B)
    PA=P.pointTo(A)
    if V.dotProduct(N)==0:
        return None
    else:
        t=-(PA.dotProduct(N))/V.dotProduct(N)
        if t>=0 and t<=1:
            return A+(V.amplified(t))
    return None
def intersect(obj1,obj2):
    if isinstance(obj1,Line) and isinstance(obj2,Line):       #1、直线和直线求交
        P,t1,t2=intersectLineLine(obj1,obj2)
        return P
    elif isinstance(obj1,Segment) and isinstance(obj2,Segment): #2 线段和线段求交
        line1,line2=Line(obj1.A,obj1.direction()),Line(obj2.A,obj2.direction())
        P,t1,t2=intersectLineLine(line1,line2)
        if P is not None:
            if t1>=0 and t1<=obj1.length() and t2>=0 and t2<=obj2.length():
                return P
        return None
    elif isinstance(obj1,Line) and isinstance(obj2,Segment):    #3直线和线段求交
        line1,line2=obj1,Line(obj2.A,obj2.direction())
        P,t1,t2=intersectLineLine(line1,line2)
        if P is not None and t2>=0 and t2<=obj2.length():
            return P
        return None
    pass  #其他情况
def intersectTrianglePlane(triangle,plane):  #三角形与平面
    AB=Segment(triangle.A,triangle.B)
    AC=Segment(triangle.A,triangle.C)
    BC=Segment(triangle.B,triangle.C)
    c1=intersectSegmentPlane(AB,plane)
    c2=intersectSegmentPlane(AC,plane)
    c3=intersectSegmentPlane(BC,plane)
    if c1 is None:
        if c2 is not None and c3 is not None:
            if c2.distance(c3) !=0.0:
                return Segment(c2,c3)
    elif c2 is None:
        if c1 is not None and c3 is not None:
            if c1.distance(c3) !=0.0:
                return Segment(c1,c3)
    elif c3 is None:
        if c1 is not None and c2 is not None:
            if c1.distance(c2) !=0.0:
                return Segment(c1,c2)
    elif c1 is not None and c2 is not None and c3 is not None:
        if c1.isIdentical(c2):
            return Segment(c1,c3)
        else:
            return Segment(c1,c2)
    return None
def intersectTriangleZPlane(triangle,z):
    if triangle.zMinPnt()>z:
        return None
    if triangle.zMaxPnt()<z:
        return None
    return intersectTrianglePlane(triangle,Plane.zPlane(z))
def pointOnRay(p:Point3D,ray:Ray):
    v=ray.P.pointTo(p)
    if v.dotProduct(ray.V) >=0 and v.crossProduct(ray.V).isZeroVector():
        return True
    return False
def pointInPolygon(p:Point3D,polygon:Polyline):   #判断点是否在多边形内部
    passCount=0
    ray=Ray.Ray(p,Vector3D(1,0,0))
    segments=[]
    for i in range(polygon.count()-1):
        seg=Segment(polygon.point(i),polygon.point(i+1))
        segments.append(seg)
    for seg in segments:
        line1,line2=Line(ray.P,ray.V),Line(seg.A,seg.direction())
        P,t1,t2=intersectLineLine(line1,line2)
        if P is not None:
            if nearZero(t1):
                return -1
            elif seg.A.y !=P.y and seg.B.y !=p.y and t1>0 and t2>0 and t2<seg.length():
                passCount+=1
    upSegments,downSegments=[],[]
    for seg in segments:
        if seg.A.isIdentical(ray.P) or seg.B.isIdentical(ray.P):
            return -1
        elif pointOnRay(seg.A,ray)^pointOnRay(seg.B,ray):
            if seg.A.y>=p.y and seg.B.y>=p.y:
                upSegments.append(seg)
            elif seg.A.y<=p.y and seg.B.y<=p.y:
                downSegments.append(seg)
    passCount+=min(len(upSegments),len(downSegments))
    if passCount %2==1:
        return 1
    return 0

def rotatePolygons(polygons, angle, center = None): # 定义旋转多边形函数
    dx = 0 if center is None else center.x # 旋转中心X 坐标，默认为0
    dy = 0 if center is None else center.y # 旋转中心Y 坐标，默认为0
    mt = Matrix3D.createTranslateMatrix(-dx, -dy, 0) # 构造平移矩阵，matrix to
    mr = Matrix3D.createRotateMatrix('Z', angle) # 构造旋转矩阵，旋转轴为Z 轴
    mb = Matrix3D.createTranslateMatrix(dx, dy, 0) # 构造反向平移矩阵，matrix back
    m = mt * mr * mb # 变换矩阵乘积
    newPolys = []
    for poly in polygons: # 遍历，对每个多边形变换
        newPolys.append(poly.multiplied(m))
    return newPolys




