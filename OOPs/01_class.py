class Student:
    college = "IIT Bombay" #class variable

    def __init__(self, name, roll):
        self.name = name #instance variable
        self.roll = roll

    def display(self):#instance method
        print(self.name, self.roll, self.college)

s1=Student("Rahul", 101)
s2=Student("Rohit", 102)
s3=Student("Raj", 103)

s1.display()
s2.display()
print(s3.college)
