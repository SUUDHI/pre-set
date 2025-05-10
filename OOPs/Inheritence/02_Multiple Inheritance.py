#Multiple Inheritance
class dog:
  def animal(self):
    print("this is a dog")

class Friendly:
  def about(self):
    print("this dog is Friendly")

class labra(dog,Friendly):
  def __init__ (self,name,age):
    self.name=name
    self.age=age

d=labra("buddy",2)
d.animal()
d.about()
print(d.name)
