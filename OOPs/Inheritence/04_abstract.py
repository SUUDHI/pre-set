from abc import ABC, abstractmethod

class Shap(ABC):

    @abstractmethod
    def area (self):
        pass

    @abstractmethod
    def perimeter (self):
         pass

class Circle(Shap):
    def __init__(self, radious):
        self.radious = radious

    def area(self):
        return(22/7 )* self.radious*self.radious
    
    def perimeter(self):
        return 2*(22/7)*self.radious

class Squre(Shap):
    def __init__(self,side):
        self.sides = side

    def area(self):
        return(self.sides**2)

    def perimeter(self):
        pass

c1=Circle(10)
print(c1.area())
print(c1.perimeter())

s2=Squre(5)
print(s2.area())
        