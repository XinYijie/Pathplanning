from GemoBase import *
class Segment:
    def __init__(self,A,B):
        self.A,self.B=A.clone(),B.clone()
    def __str__(self):
        return "Segment:A%s\nB %s\n"%(str(self.A),str(self.B))
    def length(self):
        return self.A.distance(self.B)
    def direction(self):
        return self.A.pointTo(self.B)
    def swap(self):
        self.A,self.B=self.B,self.A
    def multiply(self,m):    #对对象本身变换，作用一个矩阵
        self.A=self.A.multiplied(m)
        self.B=self.B.multiplied(m)
    def multiplied(self,m):    #作用一个矩阵，产生一个新的线段对象
        seg=Segment(self.A,self.B)
        seg.multiply(m)
        return seg