from GemoBase import *
class Triangle:
    def __init__(self,A,B,C,N=Vector3D(0,0,0)):
        self.A,self.B,self.C,self.N=A.clone(),B.clone(),C.clone(),N.clone()
        self.zs=[]
    def __str__(self):
        return "Triangle:\nA:%s\nB:%s\nC:%s\n"%(self.A,self.B,self.C)
    def zMinPnt(self):
        z1=self.A.z
        z2=self.B.z
        z3=self.C.z
        return min(z1,z2,z3)
    def zMaxPnt(self):
        z1 = self.A.z
        z2 = self.B.z
        z3 = self.C.z
        return max(z1, z2, z3)
