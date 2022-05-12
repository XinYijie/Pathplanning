from GemoBase import *
class Ray:
    def __init__(self,P,V):
        self.P=P.clone()
        self.V=V.clone().normalized()
    def __str__(self):
        return 'Ray\nP:%s\nV:%s\n'%(str(self.P),str(self.V))