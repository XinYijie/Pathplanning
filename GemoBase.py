import math
epsilon=1e-7
epsilonSquare=epsilon*epsilon
class Point3D:
    def __init__(self,x=0.0,y=0.0,z=0.0,w=1.0):
        self.x,self.y,self.z,self.w=x,y,z,w
    def __str__(self):
        return "Point3D:X:%s Y:%s Z:%s"%(self.x,self.y,self.z)
    def clone(self):
        return Point3D(self.x,self.y,self.z,self.w)
    def pointTo(self,other):
        return Vector3D(other.x-self.x,other.y-self.y,other.z-self.z)
    def translate(self,vec):
        self.x+vec.dx,self.y+vec.dy,self.z+vec.dz
    def translated(self,vec):
        return Point3D(self.x+vec.dx,self.y+vec.dy,self.z+vec.dz)
    def multiplied(self,m):
        x = self.x * m.a[0][0] + self.y * m.a[1][0] + self.z * m.a[2][0] + self.w * m.a[3][0]
        y = self.x * m.a[0][1] + self.y * m.a[1][1] + self.z * m.a[2][1] + self.w * m.a[3][1]
        z = self.x * m.a[0][2] + self.y * m.a[1][2] + self.z * m.a[2][2] + self.w * m.a[3][2]
        return Point3D(x,y,z)
    def distance(self,other):
        return self.pointTo(other).length()
    def distanceSquare(self,other):
        return self.pointTo(other).lengthSquare()
    def middle(self,other):    #计算两个点的中点
        return Point3D((self.x+other.x)/2,(self.y+other.y)/2,(self.z+other.z)/2)
    def isCoincide(self,other,dis2=epsilonSquare):    #判断两点是否重合
        d2=self.pointTo(other).lengthSquare()
        if d2<=dis2: return True
        else: return False
    def isIdentical(self,other):
        if self.x==other.x and self.y==other.y and self.z==other.z:
            return True
        else: return False
    def __add__(self, other):
        return self.translated(other)
    def __sub__(self, other):
        if isinstance(other,Point3D):
            return other.pointTo(self)
        else:return self.translated(other.reversed())
    def __mul__(self, other):
        return self.multiplied(other)

#____________________________定义向量类_______________________________
class Vector3D:
    def __init__(self,dx=0.0,dy=0.0,dz=0.0,dw=0.0):
        self.dx,self.dy,self.dz,self.dw=dx,dy,dz,dw
    def __str__(self):
        return "Vector3D:%s,%s,%s,%s"%(self.dx,self.dy,self.dz,self.dw)
    def clone(self):
        return Vector3D(self.dx,self.dy,self.dz,self.dw)
    def reverse(self):    #对当前向量取反
        self.dx,self.dy,self.dz=-self.dx,-self.dy,-self.dz
    def reversed(self):    #返回取反向量
        return Vector3D(-self.dx,-self.dy,-self.dz)
    def dotProduct(self,vec):
        return self.dx*vec.dx+self.dy*vec.dy+self.dz*vec.dz
    def crossProduct(self,vec):
        dx=self.dy*vec.dz-self.dz*vec.dy
        dy=self.dz*vec.dx-self.dx*vec.dz
        dz=self.dx*vec.dy-self.dy*vec.dx
        return Vector3D(dx,dy,dz)
    def amplify(self,f):
        self.dx,self.dy,self.dz=self.dx*f,self.dy*f,self.dz*f
    def amplified(self,f):
        return Vector3D(self.dx*f,self.dy*f,self.dz*f)
    def lengthSquare(self):
        return self.dx*self.dx+self.dy*self.dy+self.dz*self.dz
    def length(self):
        return math.sqrt(self.lengthSquare())
    def normalize(self):
        len=self.length()
        self.dx,self.dy,self.dz=self.dx/len,self.dy/len,self.dz/len
    def normalized(self): #向量单位化
        len=self.length()
        return Vector3D(self.dx/len,self.dy/len,self.dz/len)
    def isZeroVector(self):   #判断是否为0向量
        return self.lengthSquare()==0.0
    def multiplied(self,m):   #向量乘矩阵
        dx=self.dx*m.a[0][0]+self.dy*m.a[1][0]+self.dz*m.a[2][0]+self.dw*m.a[3][0]
        dy=self.dx*m.a[0][1]+self.dy*m.a[1][1]+self.dz*m.a[2][1]+self.dw*m.a[3][1]
        dz=self.dx*m.a[0][2]+self.dy*m.a[1][2]+self.dz*m.a[2][2]+self.dw*m.a[3][2]
        return Vector3D(dx,dy,dz)
    def isParallel(self,other): #判断两向量是否平行
        v=self.crossProduct(other)
        return v.isZeroVector()
    def getAngle(self,vec):  #计算两个向量夹角，返回值范围0-Pi
        v1=self.normalized()
        v2=vec.normalized()
        dotPro=v1.dotProduct(v2)
        if dotPro>1:dotPro=1
        elif dotPro<-1:dotPro=-1
        return math.acos(dotPro)
    def getCroVec2D(self):      #在XY平面生成当前向量的正交向量
        if self.dx==0:return Vector3D(1,0,0).normalized()
        else:return Vector3D(-self.dy/self.dx,1,0).normalized()
    def getAngle2D(self):      #在XY平面计算当前向量和X轴夹角，返回值范围0-2Pi
        rad=self.getAngle(Vector3D(1,0,0))
        if self.dy<0:
            rad=math.pi*2.0-rad
        return rad
    def __add__(self, other):
        return Vector3D(self.dx+other.dx,self.dy+other.dy,self.dz+other.dz)
    def __sub__(self, other):
        return self+other.reversed()
    def __mul__(self, other):
        return self.multiplied(other)





#————————————————————————————定义矩阵类————————————————————————————————
class Matrix3D:
    def __init__(self):
        self.a=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    def __str__(self):
        return 'Matrix3D:\n%s\n%s\n%s\n%s'%(self.a[0],self.a[1],self.a[2],self.a[3])
    def makeIdentical(self):    #矩阵单位化
        self.a=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    def multiplied(self,other):     #当前矩阵乘以另一个矩阵
        res=Matrix3D()
        for i in range(4):
            for j in range(4):
                res.a[i][j]=self.a[i][0]*other.a[0][j]+self.a[i][1]*other.a[1][j]+self.a[i][2]*other.a[2][j]+self.a[i][3]*other.a[3][j]
        return res
    def getDeterminant(self):  #获取矩阵行列式
        pass
    def getReverseMatrix(self): # 获取当前矩阵的逆矩阵
        pass
    @staticmethod
    def createTranslateMatrix(dx,dy,dz):   #静态函数，生成平移矩阵
        m=Matrix3D()
        m.a[3][0],m.a[3][1],m.a[3][2]=dx,dy,dz
        return m
    @staticmethod
    def createScalMatrix(sx,sy,sz):    #生成缩放矩阵
        m=Matrix3D()
        m.a[0][0], m.a[1][1], m.a[2][2] = sx, sy, sz
        return m
    @staticmethod
    def createRotateMatrix(axis,angle):    #生成旋转矩阵
        m=Matrix3D()
        sin,cos=math.sin(angle),math.cos(angle)
        if math.fabs(cos)<0.001:
            cos=0
        if axis=="X" or axis=="x":
            m.a[1][1], m.a[1][2], m.a[2][1],m.a[2][2]= cos,sin,-sin,cos
        elif axis=="Y" or axis=="y":
            m.a[0][0], m.a[0][2], m.a[2][0],m.a[2][2]= cos,-sin,sin,cos
        elif axis=="Z" or axis=="z":
            m.a[0][0]=cos
            m.a[0][1]=sin
            m.a[1][0]=-sin
            m.a[1][1]= cos
        return m
    @staticmethod
    def createMirrorMatrix(point, normal): # 静态函数，生成镜像矩阵
        pass
    def __mul__(self, other): # 矩阵相乘，调用multiplied 函数
        return self.multiplied(other)
    def __add__(self, other): # 矩阵相加
        res = Matrix3D()
        for i in range(4):
            for j in range(4):
                res.a[i][j] = self.a[i][j] + other.a[i][j]
        return res
    def __sub__(self, other): # 矩阵相减
        res = Matrix3D()
        for i in range(4):
            for j in range(4):
                res.a[i][j] = self.a[i][j] - other.a[i][j]
        return res


    # p1 = Point3D(1, 1, 1) # 创建第1 个点
    # p2 = Point3D(2, 3, 4) # 创建第2 个点
    # v = p1.pointTo(p2) # 通过pointTo 函数构造向量v
    # print(v)