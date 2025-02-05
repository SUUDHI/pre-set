class squre_calc:
    def __init__(self, n):
        self.n = n

    def squre(self):
        return self.n * self.n
    
    def cube(self):
        return self.n * self.n * self.n
    
print("enter number")
num = int(input())
cal= squre_calc(num)
print("square is ", cal.squre())
print("cube is ", cal.cube())
