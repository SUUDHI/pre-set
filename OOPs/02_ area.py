class squre :
    def __init__(self,side):
        self.side=side
    
    def area(self):
        return self.side*self.side
    
    def perimeter(self):
        return 4*self.side
    
class circle:
    def __init__ (self,radius):
        self.radius=radius

    def area(self):
        return (22/7)*self.radius*self.radius
    
    def perimeter(self):
        return 2*(22/7)*self.radius
    
s=squre(5)
print(s.area())
print(s.perimeter())

r=circle(7)
print(r.area())
print(r.perimeter())