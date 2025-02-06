"""
methord i want to use but user press enter after entring first number
num1,num2=input("enter two number with space:").split()
print(num1)
print(num2)
"""
num1=input("enter first number:")
num2=input("enter second number:")
#converting type
a=int(num1)
b=int(num2)

print(f"Sun of {a} and {b} is {a+b}")
print(f"Difference of {a} and {b} is {a-b}")
print(f"Product of {a} and {b} is {a*b}")
print(f"Division of {a} and {b} is {a//b}")

#converting in to float
c=float(num1)
d=float(num2)
print(f"Sun of {c} and {d} is {c+d}")
print(f"Difference of {c} and {d} is {c-d}")
print(f"Product of {c} and {d} is {c*d}")
print(f"Division of {c} and {d} is {c/d}")




