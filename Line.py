from GemoBase import *
class Line:
    def __init__(self,P,V):
        self.P=P.clone()     #直线经过的点，类型为Point3D
        self.V=V.clone().normalized()
    def __str__(self):
        return"Line\nP:%s\nV:%s\n"%(str(self.P),str(self.V))
        