#Take three numbers as input and find the largest number

x = int(input())
y = int(input())
z = int(input())

def gratest(a,b,c):
    if a > b and a > c:
        return a
    if b > a and b > c:
        return b
    else:
        return c

z = gratest(x,y,z,)
print("greatest is",z) 