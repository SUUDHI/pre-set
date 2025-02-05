#this file creater on 2021/07/07 at 9:20
# This file is a simple calculator that can do addition, subtraction, multiplication, and division.


class calculator:
    def __init__(self, num1, num2):# this is a constructor
        self.num1 = num1
        self.num2 = num2

    def add(self):#add method
        return self.num1 + self.num2

    def subtract(self):#subtract method
        return self.num1 - self.num2

    def multiply(self):#multiply method
        return self.num1 * self.num2

    def divide(self):#divide method
        return self.num1 / self.num2

print("enter numbet 1")
num1 = int(input())
print("enter numbet 2")
num2 = int(input())

cal = calculator(num1, num2)# object creation

print("addition is ", cal.add())
print("subtraction is ", cal.subtract())
print("multiplication is ", cal.multiply())
print("division is ", cal.divide())

        