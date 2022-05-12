PI=3.1415926
class Circle:
    def __init__(self,radius):
        self.radius=radius
    def __str__(self):
        return "Circles"
    def area(self):
        return self.radius*self.radius*PI
    def rad(self,btr):
        return  2*btr
