#single level Inheritance 

class Animal:
    def animal(self):
        print("Animal class")

class Dog(Animal,):
    def __init__(self,name,age):
        self.name=name
        self.age=age
        
    def dog(self):
        print("Dog class")

d=Dog("bug" , 2)
d.animal()
d.dog()
print(d.name)
print(d.age)
