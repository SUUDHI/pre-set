#Multilevel Inheritances
class school:
  school="k.V"

class Grade(school):
  def __init__(self,grade):
    self.grade=grade

class Sub(Grade):
  def __init__(self,subject):
    self.subject=subject

student=Sub("Science")

print(student.subject)
print(student.school)

student.subject="Maths"#changing the value of subject

print(student.subject)
